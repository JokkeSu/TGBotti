import os
import datetime
import requests
from flask import Flask, request
import telegram
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger('my_application')


TOKEN = os.environ['token_heroku']
SECRET = '/bot' + TOKEN
URL = os.environ['url_heroku']


app = Flask(__name__)
app.debug = True

bot = telegram.Bot(token=TOKEN)


@app.route('/%s' % SECRET, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        log.info('post from teleg')
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        # repeat the same message back (echo)
        bot.sendMessage(chat_id=chat_id, text=text)
    else:
        log.info('notpost from teleg')

    return 'ok'


@app.route('/swh', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('%s/%s' % (URL, TOKEN), PORT=8443)
    if s:
        print("webhook setup ok")
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/dwh', methods=['GET', 'POST'])
def delete_webhook():
    s = bot.deleteWebhook()
    if s:
        return "webhook deleted ok"
    else:
        return "webhook delete failed"


@app.route('/')
def index():
    log.info('i made this request')
    return 'home page.'
