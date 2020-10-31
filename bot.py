import telebot
import secret_data
from constants import messages, buttons, markups, booleans
from api import search_film

bot = telebot.TeleBot(secret_data.telegram_api_token)

@bot.message_handler(commands=['start'])
def handler_quiz(message):
    print(message)
    bot.send_message(message.chat.id, messages['start'], reply_markup=markups['start_markup'])

@bot.message_handler(func=lambda msg: msg.text == buttons['search_film'])
def searching1(message):
    bot.send_message(message.chat.id, messages['input_film'])
    booleans['isSearchButton'] = True

@bot.message_handler(content_types=['text'])
def message_handler(message):
     if booleans['isSearchButton']:
        film_data = search_film(message.text)
        bot.send_photo(message.chat.id, film_data['posterURL'], caption=film_data['name'])
        booleans['isSearchButton'] = False

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)