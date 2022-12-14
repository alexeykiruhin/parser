import time
import telebot

from datetime import datetime
from parsing import pars

TOKEN = '981924934:AAHX4IrHiyQfZayxi9zEGomHSJx9rdT_cDs'
# URL = 'https://dzen.ru/news/rubric/personal_feed?issue_tld=ru'
URL = 'https://dzen.ru/news/rubric/computers?issue_tld=ru'
CHANNEL_NAME = '@dompizduna'

bot = telebot.TeleBot(TOKEN)
# phrase = ['Я тут.', 'Пора мне пиздануть что-то...', 'Ща чёнить пиздану...', 'Щас спою..', 'Здарова', 'Ну че, слушай',
#           'Внимание!!!', 'Остановиська', 'Чё как?']

# Сообщение при включении бота.
# msg = 'Hello my friends.'
# bot.send_message(CHANNEL_NAME, msg)


def send_news():
    """Отправляем новость в телеграм.
    Бесконечный цикл парсинга новостей."""

    while True:
        # получаем новость
        news = ['', '']
        # приветственная фраза - убрано
        # bot.send_message(CHANNEL_NAME, random.choice(phrase))
        print('Start Parsing')
        # засекаем ремя парсинга
        now = datetime.now()
        # парсим новости
        try:
            news = pars(URL)
            if not news:
                print('Sleep after duplicate')
                time.sleep(100)
                continue
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
        bot.send_photo(CHANNEL_NAME, news[1], caption=news[0], parse_mode='Markdown')
        # сообщение без картинки
        # bot.send_message(CHANNEL_NAME, news[0], parse_mode='Markdown', disable_web_page_preview=True)
        time.sleep(100)


if __name__ == '__main__':
    send_news()
