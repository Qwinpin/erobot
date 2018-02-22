import os
import shelve
# external
from crontab import CronTab
import telebot
# project
import config
from core import start, check_update, send_files
from settings import logger


bot = telebot.AsyncTeleBot(config.TOKEN)


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

    cron = CronTab(user='gito')
    job = cron.new(command='/usr/bin/python3 /home/gito/github/erobot/send.py')
    job.setall('0 08,13,19,23 * * *')
    cron.write()
    logger.info('New schedule was created')


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
    with shelve.open(config.SHELVE_NAME) as storage:
        count2 = len(storage)
    bot.reply_to(message, str(count) + ' files and ' + str(count2) + 'remain')


if __name__ == '__main__':
    bot.polling(none_stop=True)
