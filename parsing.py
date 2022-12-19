import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# service = Service(executable_path=ChromeDriverManager().install())
# options = Options()
# options.add_argument('--disable-extensions')
# options.add_argument('--disable-blink-features=AutomationControlled')  ## to avoid getting detected
# #options.add_argument('headless')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=service, options=options)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)


def pars(url):
    """Подключаем Selenium, парсим ссылку на статью и проверяем её на дубликаты.
    Возвращаем список из 2х элементов: [0] - новость, [1] - ссылка на изображение"""
    out = ['', '']
    try:
        driver.get(url)
        # ссылка на статью
        last_news = driver.find_element(By.CLASS_NAME, 'mg-card__link')
        # получаем ссылку на последнюю новость
        href = last_news.get_attribute('href')
        name_news = last_news.text
        print(f'New news: {name_news}')
        # получаем изображение для новости
        img = driver.find_element(By.CLASS_NAME, 'neo-image_loaded')
        img_url = img.get_attribute('src')
        # Read file
        data = read_file()

        try:
            driver.get(href)
            print('BUTTON1')
        except:
            print('driver - error')
        # название новости
        news_title = driver.find_element(By.CLASS_NAME, 'mg-story__title')
        news_title = news_title.text
        # текст новости
        news_body_data = driver.find_elements(By.CLASS_NAME, 'mg-snippet__text')
        news_body_list = [b.text for b in news_body_data[::-1]]
        # название источника
        source_name_data = driver.find_elements(By.CLASS_NAME, 'mg-snippet__agency')
        source_name_list = [n.text for n in source_name_data[::-1]]
        # ссылка на источник
        source_url_data = driver.find_elements(By.CLASS_NAME, 'mg-snippets-group__source')
        source_url_list = [n.get_attribute('href') for n in source_url_data[::-1]]
        # конечное сообщение
        print('make msg2')
        print(name_news)
        z = 0
        out[0] = '*' + news_title + '*'
        # ограничение на количество новостей, что бы влесть в описание картинки
        while z < 3:  # len(news_body_list):
            out[0] += '\n' + '\n' + news_body_list[z] + '\n' \
                      + 'Источник: ' + source_name_list[z] + '\n' \
                      + '[Ссылка](' + source_url_list[z] + ')'
            z += 1
        # добавляем в сисок ссылку изображения
        out[1] = img_url

        # Duplicate check and write to file
        # print("Duplicate check ...")
        if name_news not in data:
            print('Not duplicate')
            data.append(name_news)
            write_to_file(data)
            print('after')
            # парсим новость
            # out[0] = make_message(driver, href)
            print('end write')
        else:
            out = []
            print('Duplicate')

    except:
        print('Error')
        driver.get(href)
    finally:
        driver.close()
        driver.quit()
        print('finally')

    print(f'Return {out}')
    return out


def write_to_file(data):
    """Write to file"""
    print('start write')
    with open('last_news_list.json', 'w+') as outfile:
        outfile.write(json.dumps(data, indent=2, ensure_ascii=False))
    print('stop write')
    return print("Write to file")


def read_file():
    """Read file"""
    print(f'Hello')
    with open('last_news_list.json', 'r') as json_file:
        try:
            d = json.load(json_file)
            print('Read file')
        except Exception as _e:
            print(_e)
        finally:
            print(f'Count news: {len(d)}')
    return d
