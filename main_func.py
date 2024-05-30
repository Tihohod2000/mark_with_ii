import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from yandex_reviews_parser.utils import YandexParser
from parser import parse_company_reviews
from bs4 import BeautifulSoup
import warnings

import pickle
import re

import os
import re
import shutil
import string
import tensorflow as tf
import os

from selenium.webdriver.chrome.options import Options

# option = webdriver.ChromeOptions()

print(tf.__version__)

warnings.filterwarnings('ignore')

from keras.models import load_model


def open_drive(name):
    # Создаем экземпляр драйвера с указанием опций
    chrome_options = ChromeOptions()
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Запуск браузера в режиме headless
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("useAutomationExtension", False)

    # name = input("Введите название и адресс: ")
    global driver
    # driver = undetected_chromedriver.Chrome(options=chrome_options)
    driver = undetected_chromedriver.Chrome(headless=True)
    # driver = undetected_chromedriver.Chrome()
    # driver = webdriver.Chrome(options=chrome_options)  # Запуск браузера в режиме headles
    # driver = webdriver.Chrome(options = option)
    # driver = webdriver.Chrome()

    driver.get(
        'https://yandex.ru/maps/39/rostov-na-donu/?ll=39.711332%2C47.236880&mode=poi&poi%5Bpoint%5D=39.712270%2C47.237332&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D100522677108&z=17.8')
    current_url = driver.current_url

    if "showcaptcha" in current_url:
        print("Ошибка, пройдите капчу")
        quit()
    #     # showcaptcha = input("Прошёл")
    #     pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    time.sleep(1)
    searchBox = driver.find_element('class name', 'input__control')
    # print(searchBox)

    pattern = r"/(\d+)/\?"
    searchBox.send_keys(name)
    searchBox.send_keys(Keys.ENTER)
    time.sleep(2)
    current_url = driver.current_url
    time.sleep(2)

    if "org" in current_url:
        print(current_url)
        # print("rere")
        match = re.search(pattern, current_url)
        number = match.group(1)
        print(number)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        right_name = soup.find("a", class_='card-title-view__title-link').text
        right_category = soup.find("a", class_='business-categories-view__category').text
        # right_address = soup.find("div", class_='business-contacts-view__address-link').text
        meta_tag = soup.find('meta', {'itemprop': 'address'})
        right_address = meta_tag.get('content')
        # print(right_address)
        mark_of_map = soup.find("span", class_='business-rating-badge-view__rating-text').text
        print(right_name)
        print(right_category)
        print(right_address)
    else:
        selectBox = driver.find_element('class name', 'search-business-snippet-view__content')
        # print(selectBox)
        selectBox.click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        right_name = soup.find("a", class_='card-title-view__title-link').text
        right_category = soup.find("a", class_='business-categories-view__category').text
        # right_address = soup.find("div", class_='business-contacts-view__address-link').text
        meta_tag = soup.find('meta', {'itemprop': 'address'})
        right_address = meta_tag.get('content')
        mark_of_map = soup.find("span", class_='business-rating-badge-view__rating-text').text
        print(right_name)
        print(right_category)
        print(right_address)

        # Получаем текущий URL страницы
        current_url = driver.current_url
        match = re.search(pattern, current_url)
        number = match.group(1)
        print(number)
        # driver.close()
        # driver.quit()
    return right_name, right_category, right_address, number, mark_of_map

    # time.sleep(20)
    # print("Готово")
    time.sleep(2)


def predict(number):
    ###Парсинг отзывов
    company_reviews = parse_company_reviews(number)
    time.sleep(2)

    if len(company_reviews['company_reviews']) == 0:
        print("нет отзывов")
        mark_1 = 0
        mark_2 = 0
        return mark_1, mark_2

    try:
        if company_reviews['error'] == 'Страница не найдена':
            print("Ошибка парсинга отзывов")
            quit()
    except Exception as e:
        print(e)
    # Извлекаем все значения из атрибута 'text' из каждого элемента списка 'company_reviews'(Отзывы)
    text_values = [review['text'] for review in company_reviews['company_reviews']]

    ###Предсказание оценок моделью
    loaded_model = tf.keras.models.load_model("model\model_LSTM_2")
    predict_of_mark = loaded_model.predict(text_values)
    # Счётчик отзывов
    count = 0
    # Накопительная переменная оценок
    mark = 0

    for i in predict_of_mark:
        count += 1
        mark += float(i[0])

    # округление до сотых
    mark_1 = round(mark / count, 1)
    # округление до целых
    mark_2 = int(round(mark / count, 0))

    if mark_1 > 5 or mark_2 > 5:
        if mark_1 > 5:
            mark_1 = 5
        if mark_2 > 5:
            mark_2 = 5

    print(mark_1)
    print(mark_2)
    print("Конец программы")
    return mark_1, mark_2


def discon():
    try:
        # cursor.close()
        # connection.close()
        print("Соединение с PostgreSQL закрыто")
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
