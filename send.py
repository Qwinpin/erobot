from config import *

bot = telebot.TeleBot(token)


def send_files(n):
    """
    Get files description from key-value storage, send to chat

    Args:
        n (int): number of files to send
    """
    log = Log()
    with shelve.open('github/erobot/' + shelve_name) as storage:
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
