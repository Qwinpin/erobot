# built-in
import random
import time
import os
import shelve
# project
import config
from settings import bot, logger


def send_files(n):
    """
    Get files description from key-value storage, send to chat

    Args:
        n (int): number of files to send
    """
    with shelve.open('github/erobot/' + config.SHELVE_NAME) as storage:
        keys = [x for x in storage.keys()]
        random.shuffle(keys)
        chosen = keys[:n]
        for item in chosen:
            f = 'github/erobot/data/' + storage[item]
            date = time.ctime(os.path.getmtime(f))
            frmt = f[(f.rfind('.') + 1):]
            if frmt == 'gif':
                with open(f, 'rb') as data:
                    try:
                        bot.send_document(config.CHAT_ID, data, caption=str(date))
                    except:
                        logger.error('Photo send error: ' + f)
                    else:
                        del storage[item]
            elif frmt == 'jpg' or frmt == 'png':
                with open(f, 'rb') as data:
                    try:
                        bot.send_photo(config.CHAT_ID, data, caption=str(date))
                    except:
                        logger.error('Photo send error: ' + f)
                    else:
                        del storage[item]
            else:
                # TODO: add more types
                ...
