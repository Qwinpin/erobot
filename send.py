def send_files(n):
    shelve_name = 'shelve.db'
    chat_id = -0
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
                    bot.send_document(chat_id, data, str(date))
                del storage[item]
            elif frmt == 'jpg' or frmt == 'png':
                with open(f, 'rb') as data:
                    bot.send_photo(chat_id, data, str(date))
                del storage[item]
            else:
                #TODO:add more types
                pass

send_files(1)