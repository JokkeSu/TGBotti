# Tuodaan tarvittavat osat.
import os
import datetime
try:
    import telegram
except ImportError:
    print('Failed to import telegram-module.')
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


def greet(msg_greeting):
    hour = now.hour
    if 4 <= hour < 10:
        return 'Huomenta'
    elif 10 <= hour < 15:
        return 'Iltapäivää'
    elif 15 <= hour < 21:
        return 'Iltaa'
    elif (21 <= hour < 24) or (0 <= hour < 4):
        return 'Öitä {}'
    elif msg_greeting == 'hyvää yötä botti':
        return 'Hyvää yötä, '
    greet_back = 'Terve'
    return greet_back


# Token on botin tunnus. Sitä säilytetään Herokussa sovelluksen muuttujana. Noudetaan se.
token = os.environ['token_heroku']

bot = InOut(token)
greetings = ('terve!', 'hei!', 'morjens!', 'moro!', 'huomenta!', 'päivää!', 'iltaa!', 'hyvää päivää!', 'hei', 'moi!',
             'hyvää yötä')
now = datetime.datetime.now()


def main():

    new_offset = None
    sticker_amount = 0
    msgtimeold = 0
    msgpermin = 0

    while True:
        hour = now.hour
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()
        last_update_id = 0

        if len(last_update) > 0:
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['from']['first_name']
            msgtimenew = last_update['message']['date']

            try:
                last_chat_text = last_update['message']['text']
            except KeyError:
                last_chat_text = ''
            try:
                last_chat_sticker = last_update['message']['sticker']
            except KeyError:
                last_chat_sticker = []

            if last_chat_text.lower() in greetings:
                greet(last_chat_text)

#            if last_chat_text.lower() in greetings and (4 <= hour < 10):
#                bot.send_message(last_chat_id, 'Huomenta {}'.format(last_chat_name))

#            elif last_chat_text.lower() in greetings and (10 <= hour < 15):
#                bot.send_message(last_chat_id, 'Iltapäivää {}'.format(last_chat_name))

#           elif last_chat_text.lower() in greetings and (15 <= hour < 21):
#                bot.send_message(last_chat_id, 'Iltaa {}'.format(last_chat_name))

#            elif last_chat_text.lower() in greetings and ((21 <= hour < 24) or (0 <= hour < 4)):
#                bot.send_message(last_chat_id, 'Öitä {}'.format(last_chat_name))
#            elif last_chat_text.lower() == 'hyvää yötä botti':
#                bot.send_message(last_chat_id, 'Hyvää yötä, {}'.format(last_chat_name))

            if (msgtimenew - msgtimeold) < 30:
                msgpermin += 1
                msgtimeold = msgtimenew
                if msgpermin == 15:
                    bot.send_message(last_chat_id, 'Rauhoittukaa, herranen aika!')
                    msgpermin = 0
            else:
                msgtimeold = msgtimenew
                msgpermin = 0

            if len(last_chat_sticker) > 2:
                sticker_amount += 1
                if sticker_amount == 10:
                    bot.send_message(last_chat_id, 'Niin hyviä meemitarroja!')
                    sticker_amount = 0

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
