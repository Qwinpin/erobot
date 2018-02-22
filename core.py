# built-in
import os
import random
import pickle
import time
# project
import config
from settings import bot, logger


def get_files():
    files = config.IMAGES_PATH.iterdir()
    return [f for f in files if f[-4:] not in ('.gif', '.png', '.jpg')]


def start():
    """
    Create all config and storage files
    """
    data = {
        'queue': get_files(),
        'sended': [],
    }
    # shuffle
    random.shuffle(data['queue'])
    # write
    with open(config.STORAGE_FILE, 'wb') as f:
        pickle.dump(data, f)


def check_update(new_list):
    """
    check list of files in the dir and compare with existing list
    Args:
        new_list (list): list of files in the dir
    """
    # read
    with open(config.STORAGE_FILE, 'rb') as f:
        data = pickle.load(f)
    # compare
    files = get_files()
    diff_files = list(set(files) ^ set(data['sended']))
    data['queue'] = list(set(files) - set(data['sended']))
    # shuffle
    random.shuffle(data['queue'])
    # write
    with open(config.STORAGE_FILE, 'wb') as f:
        pickle.dump(data, f)
    return diff_files


def send_files(count):
    """
    Get files description from key-value storage, send to chat

    Args:
        n (int): number of files to send
    """
    with open(config.STORAGE_FILE, 'rb') as f:
        data = pickle.load(f)

    for _i in range(count):
        fname = data['queue'].pop()
        fpath = config.IMAGES_PATH / fname
        date = time.ctime(os.path.getmtime(str(fpath)))
        with fpath.open('rb') as data:
            if fname.endswith('.gif'):
                sender = bot.send_document
            else:
                sender = bot.send_photo
            try:
                sender(config.CHAT_ID, data, caption=str(date))
            except Exception as e:
                logger.exception('Photo send error: ' + fname)
            else:
                # TODO: add more types
                ...
