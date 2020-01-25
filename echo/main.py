from subprocess import Popen
from subprocess import PIPE
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram import Sticker
from telegram.ext import Filters
from echo.config import TG_TOKEN
from echo.config import TG_API_URL


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Отправь что нибудь!',
    )


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет, я учебный бот!\nБуду рад помочь!',
    )


def do_time(bot: Bot, update: Update):
    # Узнать серверное время

    process = Popen('date', stdout=PIPE)
    text, error = process.communicate()
    if error:
        text = 'Произошла ошибка'
    else:
        text=text.decode('utf-8')

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    if update.message.text == 'Привет':
        bot.send_message(chat_id, 'Привет, мой создатель!')
    elif update.message.text == 'Пока':
        bot.send_message(chat_id, 'Прощай, создатель')
    else:
        bot.send_message(chat_id, 'Пиши нормально!')
    text = 'Ваш ID = {}\n\n{}'.format(chat_id, update.message.text)
    # text = update.message.text
    bot.send_message(
        chat_id=chat_id,
        text=text
    )


def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', do_start)
    help_handler = CommandHandler('help', do_help)
    time_handler = CommandHandler('time', do_time)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()