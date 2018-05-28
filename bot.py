from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import time
import xkcd


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def comic(bot, update):
    com = xkcd.getRandomComic()
    bot.send_photo(chat_id=update.message.chat_id, photo=com.getImageLink(), caption=com.getTitle())


def what_if(bot, update):
    whatif = xkcd.getRandomWhatIf()
    bot.send_message(chat_id=update.message.chat_id, text=whatif.getLink())


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=(update.message.text + '... Blah-blah-blah'))


token = '596825364:AAEHkulei9XbtBGlo9DLS3yRCDPqmj0AAVI'

updater = Updater(token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

comic_handler = CommandHandler('comic', comic, pass_args=False)
dispatcher.add_handler(comic_handler)

what_if_handler = CommandHandler('whatif', what_if, pass_args=False)
dispatcher.add_handler(what_if_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
