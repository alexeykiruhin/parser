from selenium import webdriver
from selenium.webdriver.common.by import By

# URL = 'https://dzen.ru/news/rubric/personal_feed?issue_tld=ru'



def pars(url):
    # print('pars')
    """метод для парсинга новостей"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    out = ['', '']
    try:
        driver.get(url)
        # ссылка на статью
        es = driver.find_elements(By.CLASS_NAME, 'mg-card__link')
        print(str(es))
        elements = driver.find_element(By.CLASS_NAME, 'mg-card__link')
        # получаем ссылку на последнюю новость
        href = elements.get_attribute('href')
        # print(href)
        # получаем изображение для новости
        img = driver.find_element(By.CLASS_NAME, 'neo-image_loaded')
        img_url = img.get_attribute('src')
        # парсим новость
        out[0] = make_message(driver, href)
        # добавляем в сисок ссылку изображения
        out[1] = img_url
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

    # print(str(out))
    return out


def make_message(driver, href):
    # print('make_message')
    """Метод для генерации сообщения"""
    # парсим новость
    driver.get(href)
    # название новости
    news_title = driver.find_element(By.CLASS_NAME, 'mg-story__title')
    news_title = news_title.text
    # print('title')
    # print(news_title)

    # текст новости
    news_body_data = driver.find_elements(By.CLASS_NAME, 'mg-snippet__text')
    news_body_list = [b.text for b in news_body_data]
    # название источника
    source_name_data = driver.find_elements(By.CLASS_NAME, 'mg-snippet__agency')
    source_name_list = [n.text for n in source_name_data]
    # ссылка на источник
    source_url_data = driver.find_elements(By.CLASS_NAME, 'mg-snippets-group__source')
    source_url_list = [n.get_attribute('href') for n in source_url_data]
    # конечное сообщение
    z = 0
    out = '*' + news_title + '*'
    # ограничение на количество новостей, что бы влесть в описание картинки
    while z < 3:  # len(news_body_list):
        out += '\n' + '\n' + news_body_list[z] + '\n' \
            + 'Источник: ' + source_name_list[z] + '\n' \
            + '[Ссылка](' + source_url_list[z] + ')'
        z += 1

    return out
