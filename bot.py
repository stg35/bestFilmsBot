import telebot
import secret_data
from constants import messages, buttons, markups, booleans
import db
from api import search_film, getNameOfFilm, view_newFilms

bot = telebot.TeleBot(secret_data.telegram_api_token)
counter = 0
film_name = ''
filmId = ''
month = 'DECEMBER'
new_films = []

@bot.message_handler(commands=['start'])
def handler_quiz(message):
    print(message)
    db.addUser(int(message.from_user.id))
    bot.send_message(message.chat.id, messages['start'].format(username=message.from_user.username), reply_markup=markups['main_markup'])

@bot.message_handler(func=lambda msg: msg.text == buttons['search_film'])
def searching1(message):
    bot.send_message(message.chat.id, messages['input_film'])
    booleans['isSearchButton'] = True

@bot.message_handler(func=lambda msg: msg.text == buttons['wish_list'])
def view_wishlist(message):
    try:
        list = db.viewWishlist(message.from_user.id)
        for id in list:
            bot.send_message(message.chat.id, getNameOfFilm(id), reply_markup=markups['choose_markup'])
    except:
        bot.send_message(message.chat.id, messages['none_wishlist'])

@bot.message_handler(content_types=['text'])
def message_handler(message):
    global counter
    global film_name
    global filmId
    global month
    global new_films
    if message.text == buttons['stop']:
        booleans['isSearchButton'] = False
        counter = 0
        film_name = ''
        bot.send_message(message.chat.id, messages['main'], reply_markup=markups['main_markup'])
    if booleans['isSearchButton']:
        if message.text != buttons['next']:
            counter = 0
            film_name = message.text
            try:
                film_data = search_film(film_name)
            except:
                bot.send_message(message.chat.id, messages['not_found'], reply_markup=markups['main_markup'])
                booleans['isSearchButton'] = False
                counter = 0
                film_name = ''
                return
        elif message.text == buttons['next']:
            try:
                film_data = search_film(film_name, counter)
            except:
                bot.send_message(message.chat.id, messages['not_found'], reply_markup=markups['main_markup'])
                booleans['isSearchButton'] = False
                counter = 0
                film_name = ''
                return
        print(film_data)
        filmId = film_data['filmId']
        bot.send_photo(message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(message.chat.id, messages['this_film'], reply_markup=markups['searching_markup'])
        counter+=1

@bot.callback_query_handler(func=lambda call: call.data)
def callback_inline(call):
    global filmId
    if call.data == 'add':
        db.addMovieToWishlist(call.from_user.id, filmId)
        filmId = ''
        bot.edit_message_reply_markup(call.message.json['chat']['id'], call.message.message_id)
    if call.data == 'dislike':
        db.addMovieToBlacklist(call.from_user.id, filmId)
        filmId = ''
        bot.edit_message_reply_markup(call.message.json['chat']['id'], call.message.message_id)
    if call.data == 'choose':
        print(call.message.json['text'])
        print(call.message.json['message_id'])
        print(call)
        film_data = search_film(call.message.json['text'])
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_to_message_id=call.message.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)