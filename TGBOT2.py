﻿# Tuodaan tarvittavat osat.
import os
import datetime
try:
    import telegram
except ImportError:
    telegram = None
    print("Failed to import telegram-module.")
try:
    import requests
except ImportError:
    requests = None
    print("Failed to import requests-module.")


# InOut hakee viestipäivitykset sekä lähettää uudet viestit.
class InOut:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=100):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        print(resp.json())
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result

        return last_update


# Greet hoitaa erilaisiin tervehdyksiin reagoimisen.
def greet(last_greet):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    print(hour)
    print(minute)
    if last_greet.lower() == 'hyvää yötä botti':
        return 'Hyvää yötä,'
    elif last_greet.lower() and (4 <= hour < 10):
        return 'Huomenta'

    elif last_greet.lower() and (10 <= hour < 15):
        return 'Iltapäivää'

    elif last_greet.lower() and (15 <= hour < 21):
        return 'Iltaa'

    elif last_greet.lower() and ((21 <= hour < 24) or (0 <= hour < 4)):
        return 'Öitä'
    elif last_greet.lower() == 'hyvää yötä botti':
        return 'Hyvää yötä,'


# Token on botin tunnus. Sitä säilytetään Herokussa sovelluksen muuttujana. Noudetaan se.
token = os.environ['token_heroku']
heroku_port = int(os.environ.get('PORT', '8443'))

# Alustus.
bot = InOut(token)
updater = Updater('token_heroku')
updater.start_webhook(listen="0.0.0.0", port=heroku_port, url_path=token)

# Botti vastaa seuraaviin tervehdyksiin.
greetings = ('terve!', 'hei!', 'morjens!', 'moro!', 'huomenta!', 'päivää!', 'iltaa!', 'hyvää päivää!', 'hei', 'moi!',
             'hyvää yötä', 'hyvää yötä botti')


def main():

    new_offset = None
    sticker_amount = 0
    msgtimeold = 0
    msgpermin = 0

    # Laitetaan botti hakemaan viestipäivityksiä ja reagoimaan niihin.
    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()
        last_update_id = 0

        # Botin täytyy huomioida tilanteet, joissa uusia viestejä ei ole tullut.
        if len(last_update) > 0:
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['from']['first_name']
            msgtimenew = last_update['message']['date']

            # Botin täytyy selviytyä eri sisältöisistä viesteistä.
            try:
                last_chat_text = last_update['message']['text']
            except KeyError:
                last_chat_text = ''
            try:
                last_chat_sticker = last_update['message']['sticker']
            except KeyError:
                last_chat_sticker = []

            # Botin reagointi tervehdyksiin.
            if last_chat_text.lower() in greetings:
                greet_back = greet(last_chat_text)
                bot.send_message(last_chat_id, '{} {}'.format(greet_back, last_chat_name))

            # Kun keskustelu käy kiivaana, botti rauhoittelee.
            if (msgtimenew - msgtimeold) < 30:
                msgpermin += 1
                msgtimeold = msgtimenew
                if msgpermin == 15:
                    bot.send_message(last_chat_id, 'Rauhoittukaa, herranen aika!')
                    msgpermin = 0
            else:
                msgtimeold = msgtimenew
                msgpermin = 0

            # Jos stickereitä lähetetään useampi, botti kannustaa.
            if len(last_chat_sticker) > 2:
                sticker_amount += 1
                if sticker_amount == 10:
                    bot.send_message(last_chat_id, 'Niin hyviä meemitarroja!')
                    sticker_amount = 0

        new_offset = last_update_id + 1


# Ohjelman suoritus pythonissa saaadaan katkaistua painamalla ctrl+c.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()