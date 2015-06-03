import functools
import time
import subprocess
import os

def _initialise(Handlers, bot=None):
    Handlers.register_user_command(["fortune"])
    return []



def fortune(bot, event, *args):
    """allow users to toggle DND for ALL conversations (i.e. no @mentions)
        /bot dnd"""
    #test  = subprocess.check_output("/usr/games/fortune", shell=false) 
    stream = os.popen('fortune')
    bot.send_message_parsed(event.conv,stream.read())    


def _expire_DNDs(bot):
    _dict = {}
    donotdisturb = bot.memory.get("donotdisturb")
    for user_id in donotdisturb:
        metadata = donotdisturb[user_id]
        time_expiry = metadata["created"] + metadata["expiry"]
        if time.time() < time_expiry:
            _dict[user_id] = metadata

    if len(_dict) < len(donotdisturb):
        # some entries expired
        bot.memory.set_by_path(["donotdisturb"], _dict)
        bot.memory.save()


def _user_has_dnd(bot, user_id):
    user_has_dnd = False
    if bot.memory.exists(["donotdisturb"]):
        _expire_DNDs(bot) # expire records prior to check
        donotdisturb = bot.memory.get('donotdisturb')
        if user_id in donotdisturb:
            user_has_dnd = True
    return user_has_dnd
