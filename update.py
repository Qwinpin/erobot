# external
import telebot
# project
import config
from core import context

bot = telebot.AsyncTeleBot(config.TOKEN)


@bot.message_handler(commands=['cron'])
def handle_cron(message):
    with context() as channels:
        channels.create_cron_tasks()
    bot.reply_to(message, 'Cron tasks created.')


@bot.message_handler(commands=['update'])
def handle_update(message):
    with context() as channels:
        updated = channels.update()
    if len(updated) > 4:
        updated = ', '.join(updated)
    else:
        updated = len(updated)
    bot.reply_to(message, 'Updated files: {}.'.format(updated))


@bot.message_handler(commands=['send'])
def handle_send(message):
    with context() as channels:
        channels.send()
    bot.reply_to(message, 'Files sended in all channels')


@bot.message_handler(commands=['stat'])
def handle_remain(message):
    stat = []
    with context() as channels:
        for channel in channels.channels:
            stat.append('\n'.join(
                '# {}'.format(channel.rule.alias),
                'queue: {}'.format(channel.state.queue),
                'sended: {}'.format(channel.state.sended),
                'failed: {}'.format(channel.state.failed),
            ))
    bot.reply_to(message, '\n\n'.join(stat))


if __name__ == '__main__':
    bot.polling(none_stop=True)
