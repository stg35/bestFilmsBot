import telebot
import secret_data
from constants import messages, buttons, markups, booleans
from api import search_film

bot = telebot.TeleBot(secret_data.telegram_api_token)
counter = 0
film_name = ''

@bot.message_handler(commands=['start'])
def handler_quiz(message):
    print(message)
    bot.send_message(message.chat.id, messages['start'].format(username=message.from_user.username), reply_markup=markups['start_markup'])

@bot.message_handler(func=lambda msg: msg.text == buttons['search_film'])
def searching1(message):
    bot.send_message(message.chat.id, messages['input_film'])
    booleans['isSearchButton'] = True

@bot.message_handler(content_types=['text'])
def message_handler(message):
    global counter
    global film_name
    if message.text == buttons['stop']:
        booleans['isSearchButton'] = False
        counter = 0
        film_name = ''
    if booleans['isSearchButton']:
        if counter == 0:
            film_name = message.text
            film_data = search_film(film_name)
        else:
            film_data = search_film(film_name, counter)
        print(film_data)
        bot.send_photo(message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['searching_markup'])
        counter+=1

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)