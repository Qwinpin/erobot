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

channels = ChannelsManager()


@bot.message_handler(commands=['cron'])
def handle_cron(message):
    channels.create_cron_tasks()
    bot.reply_to(message, 'Cron tasks created.')


@bot.message_handler(commands=['update'])
def handle_update(message):
    updated = channels.update()
    if len(updated) > 4:
        updated = ', '.join(updated)
    else:
        updated = len(updated)
    bot.reply_to(message, 'Updated files: {}.'.format(updated))


@bot.message_handler(commands=['send'])
def handle_send(message):
    channels.send()
    bot.reply_to(message, 'Files sended in all channels')


@bot.message_handler(commands=['stat'])
def handle_remain(message):
    stat = []
    for channel in schannels.schannels:
        all_stat.append('\n'.join(
            '# {}'.format(channel.rule.alias),
            'queue: {}'.format(channel.state.queue),
            'sended: {}'.format(channel.state.sended),
            'failed: {}'.format(channel.state.failed),
        ))
    bot.reply_to(message, '\n\n'.join(stat))


if __name__ == '__main__':
    bot.polling(none_stop=True)
