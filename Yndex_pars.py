import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from parser import parse_company_reviews
from bs4 import BeautifulSoup
import warnings

import pickle
import re

import os
import re

name = input("Введите название: ")
driver = undetected_chromedriver.Chrome()
driver.get(
    'https://yandex.ru/maps/39/rostov-na-donu/?ll=39.711332%2C47.236880&mode=poi&poi%5Bpoint%5D=39.712270%2C47.237332&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D100522677108&z=17.8')
current_url = driver.current_url

time.sleep(1)
searchBox = driver.find_element('class name', 'input__control')

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


def parsing(number, driver):
    driver.get(f"https://yandex.ru/maps/org/{number}/reviews/")
    time.sleep(2)

    SCROLL_PAUSE_TIME = 2
    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    # reviews_container = soup.find('div', 'business-reviews-card-view__reviews-container')
    # reviews_container = driver.find_element('class name', 'business-reviews-card-view__review')
    elements = driver.find_elements('class name', 'business-reviews-card-view__review')

    countqwe = driver.find_element('class name', 'tabs-select-view__title._name_reviews._selected')
    count = int(countqwe.find_element('class name', 'tabs-select-view__counter').text)
    # reviews_container = driver.find_element('class name', 'business-card-view__section')

    # Проверка, что элементы найдены
    while count > len(elements):
        # Выбор последнего элемента из списка
        last_element = elements[-1]

        # Прокрутка до последнего элемента
        last_element.location_once_scrolled_into_view

        elements = driver.find_elements('class name', 'business-reviews-card-view__review')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    reviewsAll = soup.find_all("span", class_='business-review-view__body-text')
    # reviews_2 = soup.find("span", class_='spoiler-view__text')

    reviews_text = []

    if reviewsAll:
        for review in reviewsAll:
            reviews_text.append(review.text)

    print(len(reviewsAll))
# input("Конец")
# driver.close()
# driver.quit()
# business-review-view__body-text
