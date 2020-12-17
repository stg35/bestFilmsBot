import telebot
import secret_data
from constants import messages, buttons, markups, booleans
import db
from api import search_film, getNameOfFilm, view_newFilms, getFilmByID
from random import randint

bot = telebot.TeleBot(secret_data.telegram_api_token)
counter = 0
film_name = ''
filmId = ''
month = 'DECEMBER'
new_films = []
current_selection_data = {}
viewed_films = []
selection1 = {}
selection2 = {}
viewed_selections = []

@bot.message_handler(commands=['start'])
def handler_quiz(message):
    print(message)
    db.addUser(int(message.from_user.id))
    bot.send_message(message.chat.id, messages['start'].format(username=message.from_user.username), reply_markup=markups['main_markup'])

@bot.message_handler(func=lambda msg: msg.text == buttons['search_film'])
def searching1(message):
    bot.send_message(message.chat.id, messages['input_film'])
    booleans['isSearchButton'] = True

@bot.message_handler(func=lambda msg: msg.text == buttons['recommend_film'])
def selection(message):
    bot.send_message(message.chat.id, messages['selection0'], reply_markup=markups['selection0_markup'])

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
    global current_selection_data
    global viewed_films
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
        filmId = film_data['filmId']
        bot.send_photo(message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(message.chat.id, messages['this_film'], reply_markup=markups['searching_markup'])
        counter+=1
    if booleans['isSelection']:
        if message.text == buttons['yes']:
            while 1:
                num = randint(0, len(current_selection_data['selection_films']))
                if num not in viewed_films:
                    break
            viewed_films.append(num)
            filmId = current_selection_data['selection_films'][num]
            film_data = getFilmByID(filmId)
            bot.send_photo(message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
                name=film_data['name'], year=film_data['year'], description=film_data['description'],
                rating=film_data['rating']), reply_markup=markups['under_markup'])
            bot.send_message(message.chat.id, messages['next'], reply_markup=markups['yes_no_markup'])
        elif message.text == buttons['no']:
            booleans['isSelection'] = False
            current_selection_data = {}
            viewed_films = []
            bot.send_message(message.chat.id, messages['main'], reply_markup=markups['main_markup'])


@bot.callback_query_handler(func=lambda call: call.data)
def callback_inline(call):
    global filmId
    global current_selection_data
    global viewed_films
    global selection1
    global selection2
    global viewed_selections
    if call.data == 'add':
        db.addMovieToWishlist(call.from_user.id, filmId)
        filmId = ''
        bot.edit_message_reply_markup(call.message.json['chat']['id'], call.message.message_id)
    if call.data == 'dislike':
        db.addMovieToBlacklist(call.from_user.id, filmId)
        filmId = ''
        bot.edit_message_reply_markup(call.message.json['chat']['id'], call.message.message_id)
    if call.data == 'choose':
        film_data = search_film(call.message.json['text'])
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_to_message_id=call.message.message_id)
    if call.data == 'top_films':
        data = db.getSelection(0)
        booleans['isSelection'] = True
        current_selection_data = data
        num = randint(0, len(data['selection_films']))
        viewed_films.append(num)
        filmId = data['selection_films'][num]
        film_data = getFilmByID(filmId)
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(call.message.chat.id, messages['next'], reply_markup=markups['yes_no_markup'])
    if call.data == 'pop_films':
        data = db.getSelection(1)
        booleans['isSelection'] = True
        current_selection_data = data
        num = randint(0, len(data['selection_films']))
        viewed_films.append(num)
        filmId = data['selection_films'][num]
        film_data = getFilmByID(filmId)
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(call.message.chat.id, messages['next'], reply_markup=markups['yes_no_markup'])
    if call.data == 'more_selections':
        while 1:
            num = randint(2, 19)
            if num not in viewed_selections:
                break
        num1 = num
        viewed_selections.append(num)
        while 1:
            num = randint(2, 19)
            if num not in viewed_selections:
                break
        num2 = num
        viewed_selections.append(num)
        selection1 = db.getSelection(num1)
        selection2 = db.getSelection(num2)
        selection1_keyboard = telebot.types.InlineKeyboardMarkup()
        sel1_butt = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
        sel2_butt = telebot.types.InlineKeyboardButton(text='2', callback_data='2')
        more_butt = telebot.types.InlineKeyboardButton(text='Ещё', callback_data='more_selections')
        selection1_keyboard.add(sel1_butt, sel2_butt)
        selection1_keyboard.add(more_butt)
        bot.send_message(call.message.chat.id,
                         messages['choose_sel'].format(selection1=selection1['selection_name'], selection2=selection2['selection_name']),
                         reply_markup=selection1_keyboard)
    if call.data == '1':
        current_selection_data = selection1
        booleans['isSelection'] = True
        num = randint(0, len(current_selection_data['selection_films']))
        viewed_films.append(num)
        filmId = current_selection_data['selection_films'][num]
        film_data = getFilmByID(filmId)
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(call.message.chat.id, messages['next'], reply_markup=markups['yes_no_markup'])
        viewed_selections = []
        selection1 = {}
        selection2 = {}
    if call.data == '2':
        current_selection_data = selection2
        booleans['isSelection'] = True
        num = randint(0, len(current_selection_data['selection_films']))
        viewed_films.append(num)
        filmId = current_selection_data['selection_films'][num]
        film_data = getFilmByID(filmId)
        bot.send_photo(call.message.chat.id, film_data['posterURL'], caption=messages['caption_text'].format(
            name=film_data['name'], year=film_data['year'], description=film_data['description'],
            rating=film_data['rating']), reply_markup=markups['under_markup'])
        bot.send_message(call.message.chat.id, messages['next'], reply_markup=markups['yes_no_markup'])
        viewed_selections = []
        selection1 = {}
        selection2 = {}

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)