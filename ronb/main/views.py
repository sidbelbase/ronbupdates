from ronb.bot import send_message, send_photo, set_webhook, delete_webhook, get_webhook_info
from ronb.tweet.store import add_tweet
from ronb.tweet.show import fetch_tweets, logs
from flask import render_template, Blueprint
from ronb.config import Configuration as creds

main = Blueprint('main', __name__)


base_url = creds.BASE_URL
token = creds.BOT_TOKEN
secret = creds.SECRET_KEY

# Flask Main View


@main.route('/')
def home():
    return render_template('home.html')


# Bot Related Works

@main.route(f'/{secret}', methods=['POST'])
# Sends ronbfeeds to the channel
def send_to_channel():
    add_tweet()
    count = int(logs().tweets_added)
    the_list = fetch_tweets()[:count][::-1]
    for the_tweet in the_list:
        if the_tweet.image_url == "None":
            send_message(the_tweet.tweet)
        else:
            send_photo(the_tweet.image_url, the_tweet.tweet)
    return {"ok": "true"}


@main.route(f'/{token}', methods=['POST'])
# Sends webhook replies to the bot
def send_to_bot():
    return {"ok": "true"}


@main.route('/webhook/set', methods=['GET', 'POST'])
def webhook_set():
    set_webhook(base_url)
    return {"ok": "true"}


@main.route('/webhook/remove', methods=['GET', 'POST'])
def remove_webhook():
    delete_webhook()
    return {"ok": "true"}


@main.route('/webhook/info', methods=['GET', 'POST'])
def webhook_info():
    get_webhook_info()
    return {"ok": "true"}
