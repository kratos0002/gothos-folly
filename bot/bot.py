import requests
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json

telegram_bot_token = "5427147088:AAEaXjaWu96vvHug78E3By4jCd3A4G6pXfQ"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def random(update, context):
    # fetch data from the api
    response = requests.get('http://3.6.86.239:49160/random')
    data = response.json()
    # send message
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['text']+' - '+data['title']+ ' - '+data['author']) 



# linking the /random command with the function random() 
quotes_handler = CommandHandler('random', random)
dispatcher.add_handler(quotes_handler)

updater.start_polling()
