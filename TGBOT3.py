import os
import datetime
import requests
import sys
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
from telepot.delegate import per_chat_id, create_open, pave_event_space


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)


TOKEN = os.environ['token_heroku']
PORT = int(os.environ['port_heroku'])
URL = os.environ['url_heroku']

app = Flask(__name__)

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])


webhook = OrderedWebhook(bot)


@app.route('/webhook', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(port=PORT, debug=True)