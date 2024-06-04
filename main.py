import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7453226419:AAHa-5qQtGIlt1gnUbDH5ubdEyhoZxFuyS4')

name = None

@bot.message_handler(commands=['start'])
def start(message):
    file = open('../img/Start-icon.jpg', 'rb')
    mess = (f'Приветствую вас: {message.from_user.first_name} в тестовом телеграм канале  для Академии Транспортных технологий.')
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Меню', callback_data='menu')
    btn2 = types.InlineKeyboardButton('Посетить сайт академии', url='http://www.att.edu.ru/')
    markup.add(btn1,btn2)
    bot.send_photo(message.chat.id, file, caption=mess, reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    schedule = types.KeyboardButton('🌌 Расписание')
    news = types.KeyboardButton('🌍 Новости')
    prof= types.KeyboardButton('🌐 Профиль')
    markup.add( schedule, news, prof)
    bot.send_message(message.chat.id, f'Вы попали в главное меню AttTestBot:', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['schedule'])
def schedule(message):
    mess1 = (f'Выбирите вашу группу:')
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn5 = types.InlineKeyboardButton('ДИ-21', callback_data='list')
    btn6 = types.InlineKeyboardButton('KИ-31', callback_data='list')
    btn7 = types.InlineKeyboardButton('ДЭ-01', callback_data='list')
    btn8 = types.InlineKeyboardButton('КИ-32', callback_data='list')
    markup.add(btn5, btn6, btn7, btn8)
    bot.send_message(message.chat.id, mess1, reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['news'])
def news(message):
    file = open('../img/News.jpg', 'rb')
    markup = types.InlineKeyboardMarkup(row_width=1)
    mess1 = (f'ПРИЁМНАЯ КАМПАНИЯ \nПрием документов с 03 июня!!!')
    btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
    markup.add(btn9)
    bot.send_photo(message.chat.id, file, caption=mess1, reply_markup=markup)


@bot.message_handler(commands=['profile'])
def profile(message):
    file = open('../img/Profile-icon.jpg', 'rb')
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    mess2 = (f'Вход в личный кабинет учащегося!')
    btn3 = types.InlineKeyboardButton('Регистрация аккаунта', callback_data='reg')
    btn4 = types.InlineKeyboardButton('Вход в аккаунт', callback_data='exit')
    btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
    markup.add(btn3, btn4, btn9)
    bot.send_photo(message.chat.id, file, caption=mess2, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data == 'menu':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        schedule = types.KeyboardButton('🌌 Расписание')
        news = types.KeyboardButton('🌍 Новости')
        prof = types.KeyboardButton('🌐 Профиль')
        markup_reply.add(schedule, news, prof)
        bot.send_message(call.message.chat.id, f'Вы попали в главное меню AttTestBot:', reply_markup=markup_reply)
        bot.register_next_step_handler(call.message, on_click)
    elif call.data == 'list':
        mess1 = (f'Выбирете день недели:')
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn5 = types.InlineKeyboardButton('Понидельник', callback_data='days1')
        btn6 = types.InlineKeyboardButton('Вторник', callback_data='days2')
        btn7 = types.InlineKeyboardButton('Среда', callback_data='days3')
        btn8 = types.InlineKeyboardButton('Четверг', callback_data='days4')
        btn10 = types.InlineKeyboardButton('Пятница', callback_data='days5')
        btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn5, btn6, btn7, btn8,btn10, btn9)
        bot.send_message(call.message.chat.id, mess1, reply_markup=markup, parse_mode='html')
    elif call.data == 'days1':
        file = open('../schedule/ДИ-21/ДИ-21-Пн.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file)
    elif call.data == 'days2':
        file = open('../schedule/ДИ-21/ДИ-21-Вт.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file)
    elif call.data == 'days3':
        file = open('../schedule/ДИ-21/ДИ-21-Ср.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file)
    elif call.data == 'days4':
        file = open('../schedule/ДИ-21/ДИ-21-Чт.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file)
    elif call.data == 'days5':
        file = open('../schedule/ДИ-21/ДИ-21-Пт.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file)
    elif call.data == 'reg':
        comn = sqlite3.connect('../profile.sql')
        cur = comn.cursor()

        cur.execute(
            'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
        comn.commit()
        cur.close()
        comn.close()

        bot.send_message(call.message.chat.id, 'Введите своё имя')
        bot.register_next_step_handler(call.message, user_name)
    elif call.data == 'users':
        comn = sqlite3.connect('../profile.sql')
        cur = comn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'Имя: {el[1]}, пароль: {el[2]}\n'

        cur.close()
        comn.close()

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn9)
        bot.send_message(call.message.chat.id, info, reply_markup=markup, parse_mode='html')
    elif call.data == 'exit':
        bot.send_message(call.message.chat.id, 'В разработке...')

def on_click(message):
    if message.text == '🌌 Расписание':
        mess1 = (f'Выбирите вашу группу:')
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn5 = types.InlineKeyboardButton('ДИ-21', callback_data='list')
        btn6 = types.InlineKeyboardButton('KИ-31', callback_data='list')
        btn7 = types.InlineKeyboardButton('ДЭ-01', callback_data='list')
        btn8 = types.InlineKeyboardButton('КИ-32', callback_data='list')
        btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn5, btn6, btn7, btn8, btn9)
        bot.send_message(message.chat.id, mess1, reply_markup=markup, parse_mode='html')
    elif message.text == '🌍 Новости':
        file = open('../img/News.jpg', 'rb')
        markup = types.InlineKeyboardMarkup(row_width=1)
        mess1 = (f'ПРИЁМНАЯ КАМПАНИЯ \nПрием документов с 03 июня!!!')
        btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn9)
        bot.send_photo(message.chat.id, file, caption=mess1, reply_markup=markup)
    elif message.text == '🌐 Профиль':
        file = open('../img/Profile-icon.jpg', 'rb')
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        mess2 = (f'Вход в личный кабинет учащегося!')
        btn3 = types.InlineKeyboardButton('Регистрация аккаунта', callback_data='reg')
        btn4 = types.InlineKeyboardButton('Вход в аккаунт', callback_data='exit')
        btn9 = types.InlineKeyboardButton('Вернуться в меню', callback_data='menu')
        markup.add(btn3, btn4, btn9)
        bot.send_photo(message.chat.id, file, caption=mess2, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    comn = sqlite3.connect('../profile.sql')
    cur = comn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    comn.commit()
    cur.close()
    comn.close()

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)


bot.polling(none_stop=True)