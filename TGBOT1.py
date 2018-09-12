# Tuodaan tarvittavat osat
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters, logging

#Token on viittaus TG:n palvelimelle. Sitä seurataan.
updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

#Joku loki virheenjäljitystä varten.
logging.basicConfig(format='%(asctime)s - %(name)s - (levelname)s - %(message)s',
                    level=logging.INFO)

#Metodi komennolle start.
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Botti palveluksessanne!")

#Metodi komennolle unknown.
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="En ymmärrä.")

#Metodi komennolle botin_kutsu.
def botin_kutsu(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Niin?")

#Tämä seuraa start-komentoa ja käynnistää start-metodin.
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Tämä seuraa Botti-komentoa ja käynnistää botin_kutsu-metodin.
botin_kutsu_handler = CommandHandler('Botti', botin_kutsu)
dispatcher.add_handler(botin_kutsu_handler)

#Tämä seuraa, tunnetaanko komentoa. Mikäli sitä ei tunneta, unknown-metodi käynnistetään.
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#Tämä käynnistää koko homman.
updater.start_polling()
