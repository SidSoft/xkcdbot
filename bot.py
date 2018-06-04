from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from imgurpython import ImgurClient
import logging
import time
import xkcd
import config
import random


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Make your choise", reply_markup=markup)


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='''
/comic - Get random Monroe comic
            <code>or use inline Comic button</code>
/whatif - Get random WhatIf page link
            <code>or use inline WhatIf button</code>
/imgur - Get random Imgur picture
            <code>or use inline Imgur button</code>
                     ''',
                     parse_mode='HTML',
                     reply_markup=markup)


def comic(bot, chat_id):
    com = xkcd.getRandomComic()
    bot.send_photo(chat_id, photo=com.getImageLink(), caption=com.getTitle(), reply_markup=markup)



def comic_com(bot, update):
    chat_id = update.message.chat_id
    comic(bot, chat_id)


def what_if(bot, chat_id):
    whatif = xkcd.getRandomWhatIf()
    bot.send_message(chat_id, text=whatif.getLink(), reply_markup=markup)


def what_if_com(bot, update):
    chat_id = update.message.chat_id
    what_if(bot, chat_id)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=(update.message.text + '... Blah-blah-blah'))


def error_callback(bot, update, error):
    try:
        raise error
    except TelegramError:
        time.sleep(5)


def imgur(bot, chat_id):
    client_id = config.IMGUR_ID
    client_secret = config.IMGUR_SECRET

    client = ImgurClient(client_id, client_secret)

    items = []
    for i in range(0, 3):
        items += client.gallery(section='hot', sort='viral', page=i, window='day')

    item = items[random.randrange(0, len(items))]
    bot.send_photo(chat_id, photo=item.link, caption=item.title, reply_markup=markup)


def imgur_com(bot, update):
    chat_id = update.message.chat_id
    imgur(bot, chat_id)


def inlinequery(bot, update):
    query = update.callback_query
    chat_id = query.message.chat.id
    if (query.data == 'comic'):
        comic(bot, chat_id)
    elif (query.data == 'whatif'):
        what_if(bot, chat_id)
    elif (query.data == 'imgur'):
        imgur(bot, chat_id)
    else:
        bot.send_message(chat_id, text="Something wrong. Try again", reply_markup=markup)


token = config.TELE_TOKEN

updater = Updater(token)
dispatcher = updater.dispatcher


kb = [[InlineKeyboardButton("Comic", callback_data='comic'), InlineKeyboardButton("WhatIf", callback_data='whatif'),
       InlineKeyboardButton("Imgur", callback_data='imgur')]]
markup = InlineKeyboardMarkup(kb)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

comic_handler = CommandHandler('comic', comic_com, pass_args=False)
dispatcher.add_handler(comic_handler)

what_if_handler = CommandHandler('whatif', what_if_com, pass_args=False)
dispatcher.add_handler(what_if_handler)

imgur_handler = CommandHandler('imgur', imgur_com, pass_args=False)
dispatcher.add_handler(imgur_handler)

dispatcher.add_handler(CallbackQueryHandler(inlinequery))

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
dispatcher.add_error_handler(error_callback)

updater.start_polling()
