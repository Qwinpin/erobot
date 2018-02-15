from config import *

log = Log()
bot = telebot.TeleBot(token)


def start():
    """
    Create all config and storage files
    """
    init_list = os.listdir('./data')
    count = 0
    with shelve.open(shelve_name) as storage:
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
        #comparing states
        new_files = list(set(new_list) - set(old_list))
        if new_files:
            with shelve.open(shelve_name) as storage:
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
    with shelve.open(shelve_name) as storage:
        keys = [x for x in storage.keys()]
        random.shuffle(keys)
        chosen = keys[:n]
        for item in chosen:
            f = './data/' + storage[item]
            date = time.ctime(os.path.getmtime(f))
            frmt = f[(f.rfind('.') + 1):]
            if frmt == 'gif':
                with open(f, 'rb') as data:
                    try:
                        bot.send_document(chat_id, data, caption=str(date))
                    except:
                        log.error('Photo send error' + data)
                    else:
                        del storage[item]
            elif frmt == 'jpg' or frmt == 'png':
                with open(f, 'rb') as data:
                    try:
                        bot.send_photo(chat_id, data, caption=str(date))
                    except:
                        log.error('Photo send error' + data)
                    else:
                        del storage[item]
            else:
                #TODO:add more types
                pass
