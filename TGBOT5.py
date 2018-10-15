import os

TOKEN = os.environ['token_heroku']
PORT = int(os.environ.get('PORT', '8443'))
URL = os.environ['url_heroku']
updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(URL + TOKEN)
updater.idle()