from imp import bot, connection
from telebot import types
from buttons import download_b, support_b, able_b, reviews_b, comment_b, admin_b, \
    link_ch_b, post_ch_b, able_ch_b, instr_ch_b, back_a, reviews_ch_b, reviews_rch_b, view_reviews_b
from imp import cursor
import logging

logging.basicConfig(filename='log.txt', level = logging.ERROR)

@bot.message_handler(commands=['hf'])
def change_info(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(link_ch_b)
        markup.add(post_ch_b)
        markup.add(able_ch_b)
        markup.add(instr_ch_b)
        markup.add(reviews_ch_b)
        markup.add(reviews_rch_b)
        markup.add(view_reviews_b)
        bot.send_message(message.chat.id, '⬇️Выберите пункт меню  ⬇️', reply_markup=markup)
    except:
        logging.exception('-----------------------------------------------')


@bot.message_handler(commands=['start'])
def main_menu(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(download_b, support_b)
        markup.add(able_b, reviews_b)
        markup.add(comment_b)
        markup.add(admin_b)
        bot.send_message(message.chat.id, '⬇️Выберите пункт меню  ⬇️', reply_markup=markup)
    except:
        logging.exception('-----------------------------------------------')


@bot.message_handler(content_types=["text"])
def admin(message):
    try:
        if message.text == '📱 Связь с администратором':
            inline = types.InlineKeyboardMarkup()
            url = types.InlineKeyboardButton(text='Ссылка', url=select('data', 'const_info', 1))
            inline.add(url)
            bot.send_message(message.chat.id, 'Для свзяи администратором перейдите по ссылке ниже 👇', reply_markup=inline)

        elif message.text == '✅ Скачать приложение':
            inline = types.InlineKeyboardMarkup()
            url = types.InlineKeyboardButton(text='Ссылка', url=select('data', 'const_info', 2))
            inline.add(url)
            bot.send_message(message.chat.id, 'Для перехода в маркет нажмите ссылку ниже 👇', reply_markup=inline)

        elif message.text == '🆘 Техподдержка':
            bot.send_message(message.chat.id, 'Если возникли какие-либо вопросы, пожалуйста напишите на почту: 👇\n\n' \
                             + select('data', 'const_info', 3).replace(r"\n", '\n'))

        elif message.text == '💪 Что умеет этот бот!':
            bot.send_message(message.chat.id, select('data', 'const_info', 4).replace(r"\n", '\n'))

        elif message.text == '📝 Отзывы участников':
            bot.send_message(message.chat.id, 'Ниже представлены отзывы 👇\n')
            select_reviews(message)

        elif message.text == '❓ Инструкции по установке и запуску':
            bot.send_message(message.chat.id, select('data', 'const_info', 5).replace(r"\n", '\n'))

        elif message.text == '♻️Изменить ссылку на приложение':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id,
                                   'Сейчас действует эта ссылка:\n\n' + '👉' + select('data', 'const_info', 2) + '👈\n\n' \
                                                                                                                 '❗️Введите новую ссылку на приложение 👇',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, change_link)

        elif message.text == '♻️Изменить адрес почты':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id,
                                   'Сейчас адрес эл.почты такой:\n\n' + '👉' + select('data', 'const_info', 3) + '👈\n\n' \
                                   + '❗️Введите новый адрес почты 👇', reply_markup=markup)
            bot.register_next_step_handler(msg, change_emai)

        elif message.text == "♻️Изменить 'Что умеет этот бот'":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id, "❗️Введите 'Что умеет этот бот' 👇", reply_markup=markup)
            bot.register_next_step_handler(msg, change_able)

        elif message.text == '♻️Изменить инструкцию':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id, "❗️Введите новую инструкцию 👇", reply_markup=markup)
            bot.register_next_step_handler(msg, change_inst)

        elif message.text == '♻️Добавить отзыв':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id, "❗️Введите новый отзыв 👇", reply_markup=markup)
            bot.register_next_step_handler(msg, change_reviews)

        elif message.text == '♻️Удалить отзыв':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            msg = bot.send_message(message.chat.id, "❗️Для удаления введите id отзыва 👇", reply_markup=markup)
            bot.register_next_step_handler(msg, rechange_reviews)

        elif message.text == '♻️Посмотреть отзывы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_a)
            bot.send_message(message.chat.id, '❗️Список текщих отзывов (id+текст) 👇\n', reply_markup=markup)
            select_reviews_ch(message)

        elif message.text == '♻️Назад':
            change_info(message)
    except:
        logging.exception('-----------------------------------------------')


def change_reviews(message):
    try:
        a = []
        cursor.execute('SELECT id from reviews')
        for i in cursor.fetchall():
            a.append(str(i).replace('(', '').replace(')', '').replace(',', ''))
        cursor.execute("INSERT INTO reviews VALUES(%s, %s)", (int(max(a)) + 1, message.text))
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')

def rechange_reviews(message):
    try:
        cursor.execute("DELETE FROM reviews WHERE id = %s", message.text)
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')

def change_link(message):
    try:
        cursor.execute("UPDATE const_info SET data = %s WHERE id = 2", message.text)
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')


def change_emai(message):
    try:
        cursor.execute("UPDATE const_info SET data = %s WHERE id = 3", message.text)
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')


def change_able(message):
    try:
        cursor.execute("UPDATE const_info SET data = %s WHERE id = 4", message.text)
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')


def change_inst(message):
    try:
        cursor.execute("UPDATE const_info SET data = %s WHERE id = 5", message.text)
        connection.commit()
        bot.send_message(message.chat.id, '✅ Успешно.')
    except:
        logging.exception('-----------------------------------------------')


def select_reviews_ch(message):
    try:
        b = []
        cursor.execute("SELECT id, data from reviews")
        for i in cursor.fetchall():
            a = str(i[1]).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace("'", '')
            bot.send_message(message.chat.id, str(i[0]) + '\n' + a)
    except:
        logging.exception('-----------------------------------------------')


def select_reviews(message):
    try:
        b = []
        cursor.execute("SELECT data from reviews")
        for i in cursor.fetchall():
            a = str(i).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace("'", '')
            bot.send_message(message.chat.id, a)
    except:
        logging.exception('-----------------------------------------------')

def select(data, table, id):
    try:
        cursor.execute("SELECT {0} from {1} WHERE id='{2}'".format(data, table, id))
        a = str(cursor.fetchone()).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace("'", '')
        return a
    except:
        logging.exception('-----------------------------------------------')


bot.polling(none_stop=True)
