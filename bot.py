import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
PORT = int(os.environ.get('PORT', 5000))
url = 'http://bitsindri.ac.in/'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
TOKEN="1495878031:AAGk-J9jPA0RSsIhFVNUO1WHBdHgbE5eC2M"


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # print("\n\n")
    # print(update)
    # print("\n\n")
    # print(context)
    reply = None
    if update.message.text is not None:
        reply = ""
        r = requests.get(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36'}
        r = requests.get(url, headers=headers)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        list_ul = soup.find_all('ul', class_="nav menu menu-treemenu")
        for i in range(1, 11):
            # reply += list_ul[0].contents[i].find('span').getText()+"\n\n"
            reply += list_ul[0].contents[i].find('span').getText(
            ) + "\n"+list_ul[0].contents[i].find('a').get('href')+"\n\n"
        update.message.reply_text(reply)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://obscure-savannah-01072.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
