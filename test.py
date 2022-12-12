import time
import random
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL_T = 'https://www.deepl.com/translator#en/ru/'
BLACK_LIST = ['quiz']


def pars(url, txt):
    print('Start')
    """метод для парсинга новостей"""

    # service = Service(executable_path=ChromeDriverManager().install())
    # options = Options()
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-blink-features=AutomationControlled')  ## to avoid getting detected
    # options.add_argument('headless')
    # options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(service=service, options=options)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    # out = ['', '']
    out = ''
    try:
        driver.get(url)
        # вставляем текст для перевода
        # textarea = driver.find_element(By.CLASS_NAME, 'lmt__inner_textarea_container')  # lmt__textarea
        # textarea.send_keys(txt)
        textarea = driver.find_element(By.XPATH, '//*[@id="panelTranslateText"]/div[1]/div[2]/section[1]/div[3]/div[2]/textarea')  # lmt__textarea
        textarea.send_keys(txt)
        value = textarea.get_attribute('value')
        # print(value)
        # print(str(textarea))
        # element = driver.find_element(By.ID, 'source-dummydiv')
        # element.send_keys(txt)
        # elements = driver.find_elements(By.TAG_NAME, 'textarea')
        # for e in elements:
        #     print(e.text)
        time.sleep(10)
        # text_translate = driver.find_element(By.ID, 'target-dummydiv')  # lmt__textarea
        # text_translate = driver.find_element(By.ID, 'target-dummydiv')  # lmt__textarea
        # text_translates = driver.find_elements(By.CLASS_NAME, 'lmt__target_textarea')  # lmt__textarea
        # print('textarea:')
        # print(textarea)
        # print(textarea.text)

        # поставить проверку на пустое поле, когда она перестает быть пустым значит перевод прогрузился
        textarea2 = driver.find_element(By.XPATH, '//*[@id="panelTranslateText"]/div[1]/div[2]/section[2]/div[3]/div[1]/textarea')  # lmt__textarea
        value = textarea2.get_attribute('value')
        out = value
        f = open('res.txt', 'w')
        f.write(out)

        print('перевод:')

        # print(text_translate.text)
        # print(value)
        # print(text_translates)
        # for i in text_translate:
        #     print(f'{i.text}')
        # print(text_translate.text)
    except Exception as _ex:
        print(_ex)
    finally:
        f.close()
        driver.close()
        driver.quit()

    # print(str(out))
    return out

# URL = 'https://www.mentalfloss.com/posts/pepsi-harrier-jet-lawsuit-history'
# URL = 'https://www.mentalfloss.com'


URL = 'https://www.mentalfloss.com'
TRANSLATE = 'https://api.deepl.com/v2/translate'

page = requests.get(URL)
# print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

# print(soup)

allPosts = soup.find_all('a')
allImages = soup.find_all('picture')
# print('Всего записей:')
# print(len(allPosts))

posts = []
imgs = []
ro = []
y = 0

for post in allPosts:  # for post, img in zip(allPosts, allImages):
    # print('Start')
    # print(post['href'])

    if 'post' in post['href']:
        # print('first if')
        # print(post['href'])
        # print('BL+1' if BLACK_LIST[0] in post['href'] else 'ok')
        # проверка на слова из блэклиста, проходим каждое слово и передаем тру если находим его в ссылке
        # print(type(BLACK_LIST))
        # print(BLACK_LIST[0])
        for b in BLACK_LIST:
            if b in post['href']:
                # зажигаем индикатор попадания блеклиста
                ro.append(True)
                # print('BL')
        # если хоть одно тру есть из блэклиста, то ссылк ане попадает в конечный список
        if any(ro):
            # гасим индикатор
            ro = []
            continue
        # for k in img:
        #     print(k)
        #     if y == 3:
        #         print('SRC')
        #         print(k['src'])
        #         imgs.append(k['src'])
        #         print('img added')
        #         y = 0
        #     y += 1
        posts.append(post['href'])
        # print('href added')


print('Всего постов:')
print(len(posts))

print('Всего картинок:')
print(len(imgs))
# проходим по ссылкам и парсим данные
# for post in posts:

# выбираем рандомно пост
a = 0
b = len(posts) - 1
rnd = random.randint(a, b)
post1 = requests.get(posts[rnd])
posts.pop(rnd)
soup1 = BeautifulSoup(post1.text, 'html.parser')
all_text = soup1.find_all('p')
image = soup1.find_all('picture')
# находим урл картинки
p = 0
image_src = None
for g in image[0]:
    if p == 3:
        print(g['src'])
        image_src = g['src']
        p = 0
    p += 1

text = ''
for t in all_text:
    text += t.text

# __________TRANSLATE__________


# pars(URL_T, text)

# print('Перевод: ')
# print(translatedText)

# write to file
# data = open('res.txt', 'w')
# data.write(result.text)
# data.close()
