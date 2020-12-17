import telebot

messages = {
     'start': 'Рады вас видеть, {username}!\n\n' +
              'Что вас сегодня интересует?',
     'input_film': 'Введите фильм, который хотите найти.',
     'caption_text': '🎬{name}({year})🎬\n' + '{description}\n' + 'Рейтинг: {rating}/10',
     'main': 'Что-нибудь ещё?',
     'this_film': 'Этот фильм?(Можете попробовать ввести другое название)',
     'none_wishlist': 'Ваш список пуст.',
     'not_found': 'Увы😢, но ваш фильм не найден.',
     'selection0': 'Предлагаем вашему вниманию следующие подборки:',
     'next': 'Продолжим?',
     'choose_sel': '1.{selection1} или 2.{selection2}?'
}

buttons = {
    'genres': ['боевик', 'военный', 'детектив', 'документальный', 'драма', 'история',
          'комедия', 'криминал', 'мультфильм', 'приключения', 'семейный', 'триллер', 'ужасы',
          'фантастика', 'фэнтези'],
    'quiz': '📝Пройти опрос',
    'new': '🌠Новинки',
    'classic': '🏛Классика',
    'wish_list': '📜Вишлист',
    'recommend_film': '🎬Подборка',
    'search_film': '🔍Найти фильм',
    'stop': 'Да',
    'next': 'Нет',
    'yes': 'Конечно',
    'no': 'Хватит'
}

start_markup = telebot.types.ReplyKeyboardMarkup(True, True)
start_markup.row(buttons['recommend_film'], buttons['search_film'])
start_markup.row(buttons['wish_list'])

genres_markup = telebot.types.ReplyKeyboardMarkup()
for i in range(0, len(buttons['genres'])//3):
    genres_markup.row(buttons['genres'][i*3], buttons['genres'][i*3+1], buttons['genres'][i*3+2])

searching_markup = telebot.types.ReplyKeyboardMarkup(True)
searching_markup.row(buttons['stop'], buttons['next'])

inline_keyboard = telebot.types.InlineKeyboardMarkup()
add_button = telebot.types.InlineKeyboardButton(text='➕Добавить', callback_data='add')
dislike_button = telebot.types.InlineKeyboardButton(text='👎Не интересно', callback_data='dislike')
inline_keyboard.add(add_button, dislike_button)

choose_keyboard = telebot.types.InlineKeyboardMarkup()
choose_butt = telebot.types.InlineKeyboardButton(text='Выбрать', callback_data='choose')
choose_keyboard.add(choose_butt)

selection0_keyboard = telebot.types.InlineKeyboardMarkup()
top_films = telebot.types.InlineKeyboardButton(text='Топ лучших фильмов', callback_data='top_films')
pop_films = telebot.types.InlineKeyboardButton(text='Популярные фильмы', callback_data='pop_films')
more_butt = telebot.types.InlineKeyboardButton(text='Ещё', callback_data='more_selections')
selection0_keyboard.add(top_films, pop_films)
selection0_keyboard.add(more_butt)

yes_no_markup = telebot.types.ReplyKeyboardMarkup(True)
yes_no_markup.row(buttons['yes'], buttons['no'])

markups = {
    'main_markup': start_markup,
    'genres_markup': genres_markup,
    'searching_markup': searching_markup,
    'under_markup': inline_keyboard,
    'choose_markup': choose_keyboard,
    'selection0_markup': selection0_keyboard,
    'yes_no_markup': yes_no_markup
}

booleans = {
    'isSearchButton': False,
    'isNewButton': False,
    'isSelection': False
}