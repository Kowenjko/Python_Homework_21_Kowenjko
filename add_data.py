"""
Додати методи для усіх ролей користувачів із попереднього проекту та відлагодити їх функціонал.
Заповнити базу випадковими даними по 5 продуктів на 3 різних категорії по 2 підкатегорії (30 продуктів)
Додати 4 покупці

Товари заповнював за допомогою парсингу із сайту https://moyamebel.com.ua/catalog/, далі за допомогою 
translators(google) зробив переклад на англійську мову

Покупців згенерував Faker 
"""

from settings import *
from faker import Faker
from random import randint
from connection import Connection
import translators as ts
import requests
from bs4 import BeautifulSoup
from pprint import pprint


sum = 0
fake = Faker()

SELECTED_URL = "https://moyamebel.com.ua/catalog/"

kitchen = 'dlya-kukhni'
wardrobe = 'shkafy'
living_room = 'gostinye'

arr_category = ['Kitchen', 'Wardrobe', 'Living room']
url_category = [SELECTED_URL+kitchen,
                SELECTED_URL+wardrobe, SELECTED_URL+living_room]

# --------------------------------------------------------------


def loadData(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup


# --------------------------------------------------------------
# Парсинг та запис в БД
# --------------------------------------------------------------
for item_category in range(len(arr_category)):
    data_product_category = [{
        'category_name': arr_category[item_category]
    }]
    # записуємо в таблицю product_category
    result_category = Connection()._postData(
        'product_category', data_product_category)
    print(
        f'{arr_category[item_category]}-->{result_category[0]}-->{result_category[1]}')
    # ----------------------------------------------------------
    parse_subcategory = loadData(url_category[item_category]).find(
        'div', class_='products_categories')
    title_sub_category = parse_subcategory.find_all(
        'div', class_='cat_tiny_title')
    # for item_sub in title_sub_category:
    for item_sub in range(2):
        data_product_subcategory = [{
            'subcategory_name': ts.google(title_sub_category[item_sub].text[1:-1], to_lenguage='en'),
            'category_id':result_category[1]
        }]
        # записуємо в таблицю product_subcategory
        result_subcategory = Connection()._postData(
            'product_subcategory', data_product_subcategory)
        print(
            f'{title_sub_category[item_sub].text[1:-1]}-->{result_subcategory[0]}-->{result_subcategory[1]}')
        # ----------------------------------------------------------------------------
        url_sub = title_sub_category[item_sub].find('a').get('href')
        parse_products = loadData(url_sub).find(
            'div', id='fn-products_content')
        products = parse_products.find_all(
            'div', class_='product-card-wrapper')
        # for j in range(len(products)):
        for j in range(5):
            products_list = []
            product_disc = {}
            # code
            product_disc['code'] = products[j].find(
                'div', class_='product_name').find('a').get('data-product')
            # product_name
            product_disc['product_name'] = ts.google(products[j].find(
                'div', class_='product_name').find('a').text, to_lenguage='en')
            # unit_price
            product_disc['unit_price'] = int((products[j].find(
                'div', class_='price_container').find('span', class_='fn-price').text).replace(' ', ''))
            # count
            product_disc['count'] = randint(1, 25)
            # description
            url_description = products[j].find(
                'div', class_='product_name').find('a').get('href')
            try:
                rez_description = ts.google(loadData(url_description).find(
                    'span', class_='product-description').find('p').text, to_lenguage='en')
                rez_description = (
                    rez_description[:75] + '..') if len(rez_description) > 75 else rez_description
                product_disc['description'] = rez_description
            except:
                product_disc['description'] = 'no description'
            # img
            product_disc['img'] = products[j].find('div', class_='image').find(
                'img', class_='fn-img').get('data-src')
            # sub_category_id
            product_disc['sub_category_id'] = result_subcategory[1]
            products_list.append(product_disc)
            # записуємо в таблицю product
            result_product = Connection()._postData(
                'product', products_list)
            sum += 1
            print(
                f"{product_disc['product_name']} -->{result_product[0]}-->{result_product[1]}-->{sum}")

# --------------------------------------------------------------
# запис фейкових даних з Faker
# --------------------------------------------------------------

for item_users in range(4):
    users = [{
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_bitrth': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'phone': fake.phone_number()[:14],
        'address': fake.street_address(),
        'password': fake.password(length=8, special_chars=False, upper_case=True),
        'email': fake.free_email(),
        'role': 'customer',
        'discount': randint(0, 70)
    }]

    result_users = Connection()._postData('users', users)
    print(result_users)
# --------------------------------------------------------------
