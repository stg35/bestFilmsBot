import telebot

counter = 0

messages = {
     'start': 'Рады вас видеть, {username}!\n\n' +
              'Что вас сегодня интересует?',
     'input_film': 'Введите фильм, который хотите найти.',
     'caption_text': '🎬{name}({year})🎬\n' + '{description}\n' + 'Рейтинг: {rating}/10'
}

buttons = {
    'genres': ['боевик', 'военный', 'детектив', 'документальный', 'драма', 'история',
          'комедия', 'криминал', 'мультфильм', 'приключения', 'семейный', 'триллер', 'ужасы',
          'фантастика', 'фэнтези'],
    'quiz': '📝Пройти опрос',
    'new': '🌠Новинки',
    'classic': '🏛Классика',
    'wish_list': '📜Вишлист',
    'recommend_film': '🎬Подобрать фильм',
    'search_film': '🔍Найти фильм',
    'stop': '🛑Стоп',
    'next': '➡️'
}

start_markup = telebot.types.ReplyKeyboardMarkup(True, True)
start_markup.row(buttons['new'], buttons['classic'])
start_markup.row(buttons['wish_list'], buttons['quiz'])
start_markup.row(buttons['recommend_film'])
start_markup.row(buttons['search_film'])

genres_markup = telebot.types.ReplyKeyboardMarkup()
for i in range(0, len(buttons['genres'])//3):
    genres_markup.row(buttons['genres'][i*3], buttons['genres'][i*3+1], buttons['genres'][i*3+2])

searching_markup = telebot.types.ReplyKeyboardMarkup(True)
searching_markup.row(buttons['stop'], buttons['next'])

markups = {
    'start_markup': start_markup,
    'genres_markup': genres_markup,
    'searching_markup': searching_markup
}

booleans = {
    'isSearchButton': False
}

