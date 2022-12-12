import time
import telebot
import random

from datetime import datetime
from parsing import pars

TOKEN = '981924934:AAHX4IrHiyQfZayxi9zEGomHSJx9rdT_cDs'
# URL = 'https://dzen.ru/news/rubric/personal_feed?issue_tld=ru'
URL = 'https://dzen.ru/news/rubric/computers?issue_tld=ru'
CHANNEL_NAME = '@dompizduna'

bot = telebot.TeleBot(TOKEN)
phrase = ['Я тут.', 'Пора мне пиздануть что-то...', 'Ща чёнить пиздану...', 'Щас спою..', 'Здарова', 'Ну че, слушай',
          'Внимание!!!', 'Остановиська', 'Чё как?']

# Сообщение при включении бота.
# msg = 'Pizdun tut.'
# bot.send_message(CHANNEL_NAME, msg)


class LastNews:

    def __init__(self):
        # последняя новость
        self.last_news = ''

    def show(self):
        return self.last_news

    def add(self, nws):
        self.last_news = nws


def send_news():
    lastn = None
    while True:
        # получаем новость
        news = ''
        # приветственная фраза - убрано
        # bot.send_message(CHANNEL_NAME, random.choice(phrase))
        print('Start Parsing')
        # засекаем ремя парсинга
        now = datetime.now()
        # парсим новости
        try:
            news = pars(URL)
            print('news_telegr')
            print(news)
        except Exception as _ex:
            print(_ex)
        # finally:
        #     # news = 'Reloading...'
        current = datetime.now()
        # bot.send_message(CHANNEL_NAME, 'Stop Parsing')
        print('Stop Parsing')
        t = current - now
        # bot.send_message(CHANNEL_NAME, 'Time: ' + str(t))
        print('Time: ' + str(t))
        print('Длина новости = ' + str(len(news[0])))
        print(str(news))
        if lastn == news[0][:10]:
            print("Дубликат")
            # парсим мемас
        else:
            # сообщение с картинкой - длина его 1024 символа
            bot.send_photo(CHANNEL_NAME, news[1], caption=news[0], parse_mode='Markdown')
        lastn = news[0][:10]
        # print(ln)
        # last_news(lastn)

        # сообщение без картинки
        # bot.send_message(CHANNEL_NAME, news[0], parse_mode='Markdown', disable_web_page_preview=True)
        time.sleep(100)


send_news()





# Handle '/start' and '/help'
# @bot.message_handler(commands=['news'])
# def send_news(message):
#     # получаем новость
#     print('Start Parsing')
#     now = datetime.now()
#     d = pars(URL)
#     current = datetime.now()
#     print('Stop Parsing')
#     t = current - now
#     print('Time: ' + str(t))
#     bot.reply_to(message, d)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)


# bot.polling(none_stop=True)
# bot.infinity_polling()

# def send_news():
#     # получаем новость
#     news = ''
#     # приветственная фраза - убрано
#     # bot.send_message(CHANNEL_NAME, random.choice(phrase))
#     print('Start Parsing')
#     # засекаем ремя парсинга
#     now = datetime.now()
#     # парсим новости
#     try:
#         news = pars(URL)
#         print('news_telegr')
#         print(news)
#     except Exception as _ex:
#         print(_ex)
#     # finally:
#     #     # news = 'Reloading...'
#     current = datetime.now()
#     # bot.send_message(CHANNEL_NAME, 'Stop Parsing')
#     print('Stop Parsing')
#     t = current - now
#     # bot.send_message(CHANNEL_NAME, 'Time: ' + str(t))
#     print('Time: ' + str(t))
#     print('Длина новости = ' + str(len(news[0])))
#     print(str(news))
#     #lastn = news[0][:10]
#     # print(ln)
#     #last_news(lastn)
#     # сообщение с картинкой - длина его 1024 символа
#     bot.send_photo(CHANNEL_NAME, news[1], caption=news[0], parse_mode='Markdown')
#     # сообщение без картинки
#     # bot.send_message(CHANNEL_NAME, news[0], parse_mode='Markdown', disable_web_page_preview=True)