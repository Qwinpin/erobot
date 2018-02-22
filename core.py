# built-in
import shelve
import os
import random
import time
# project
import config
from settings import bot, logger


def start():
    """
    Create all config and storage files
    """
    init_list = os.listdir('./data')
    count = 0
    with shelve.open(config.SHELVE_NAME) as storage:
        for fl in init_list:
            storage[str(count)] = fl
            count += 1

    with open('./file_list.txt', 'w') as f:
        for fl in init_list:
            f.write(fl + '\n')


def check_update(new_list):
    """
    check list of files in the dir and compare with existing list
    Args:
        new_list (list): list of files in the dir
    """
    with open('./file_list.txt', 'r') as old_desc:
        old_list = [l.strip() for l in old_desc]
        # compare states
        new_files = list(set(new_list) - set(old_list))
        if new_files:
            with shelve.open(config.SHELVE_NAME) as storage:
                count = len(old_list)
                for fl in new_files:
                    storage[str(count)] = fl
                    count += 1
    with open('./file_list.txt', 'a') as old_desc:
        for fl in new_files:
            old_desc.write(fl + '\n')


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
