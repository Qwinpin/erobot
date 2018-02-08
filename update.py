import shelve
import os
import random
import telebot
import time


shelve_name = 'shelve.db'
token = 'XXX:XXX'
chat_id = -0
"""
str:str:int
variable for key-value path/name
variable for telegram token
variable for your chat id
"""

bot = telebot.AsyncTeleBot(token)

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    """
    Start function - handle start command

    Args:
        message (obj): response from telegram server
    """
    if not os.path.exists('./file_list.txt'):
        start()
    bot.reply_to(message, 'Hi, sexy! We are ready to start!')
    while True:
        #send files every 6 hours
        time.sleep(21600)
        send_files(1)

@bot.message_handler(commands=['update'])
def handle_update(message):
    """
    Update command handler
    Update function - add new files to key-value storage

    Args:
        message (obj): response from telegram server
    """
    check_update(os.listdir('./data'))
    bot.reply_to(message, 'Done, sweetie!')

@bot.message_handler(commands=['send_one'])
def handle_send(message):
    """
    Send one file
    """
    send_files(1)
    bot.reply_to(message, 'Done, honney!')

@bot.message_handler(commands=['remain'])
def handle_remain(message):
    """
    Remain command handler
    Return the number of remaining files
    
    Args:
        message (obj): response from telegram server
    """
    with open('./file_list.txt', 'r') as lst:
        count = len([l.strip() for l in lst])
    with shelve.open(shelve_name) as storage:
        count2 = len(storage)
    bot.reply_to(message, str(count) + ' files and ' + str(count2) + 'remain')


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
                    bot.send_document(chat_id, data, str(date))
                del storage[item]
            elif frmt == 'jpg' or frmt == 'png':
                with open(f, 'rb') as data:
                    bot.send_photo(chat_id, data, str(date))
                del storage[item]
            else:
                #TODO:add more types
                pass
