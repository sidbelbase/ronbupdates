import logging
from os import environ
from dotenv import find_dotenv, load_dotenv
from telegram.ext import CommandHandler, Updater

load_dotenv(find_dotenv())

token = environ.get('BOT_TOKEN')
channel_name = environ.get('CHANNEL')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Everything is working')


def tweet_with_photo(context):
    job = context.job
    context.bot.send_photo(job.context, photo=the_url, caption=the_message)


def tweet_without_photo(context):
    """Send the RONB Updates."""
    job = context.job
    context.bot.send_message(job.context, text=the_message)


def the_tweeter(update, context):

    chat_id = channel_name
    context.job_queue.run_repeating(
        tweet_without_photo, interval=60, context=chat_id, name=str(chat_id))
    update.message.reply_text(the_message)


def start():
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("go", the_tweeter))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()
