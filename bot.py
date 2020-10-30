import telebot
import secret_data

bot = telebot.TeleBot(secret_data.telegram_api_token)

first_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = telebot.types.KeyboardButton('Опрос')
item2 = telebot.types.KeyboardButton('Дальше')
first_markup.add(item1, item2)

genres = ['боевик', 'военный', 'детектив', 'документальный', 'драма', 'история',
          'комедия', 'криминал', 'мультфильм', 'приключения', 'семейный', 'триллер', 'ужасы',
          'фантастика', 'фэнтези']
genres_markup = telebot.types.ReplyKeyboardMarkup()
for i in range(0, len(genres)//3):
    genres_markup.row(genres[i*3], genres[i*3+1], genres[i*3+2])

@bot.message_handler(commands=['start'])
def handler_quiz(message):
    bot.send_message(message.chat.id, 'Советуем пройти опрос.', reply_markup=first_markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'опрос', content_types=['text'])
def handler(message):
    bot.send_message(message.chat.id, 'Любимый жанр', reply_markup=genres_markup)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)