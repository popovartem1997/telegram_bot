import telebot
import pymysql


TOKEN_telegram = '1420405135:AAGFPZO878mZ-tb4401B9YOGFYXeXLNLeZk'
bot=telebot.TeleBot(TOKEN_telegram)

connection=pymysql.connect(host='localhost',user='root',password='root',db='telegram_bot_1')
cursor=connection.cursor()
