"""Модуль для поиска ключей на сайте steampay.com"""

import requests
from bs4 import BeautifulSoup

from src.constants import URL_STEAMPAY
from src.exceptions import APIException, FilterException

def steam_pay(game_name: str, dict_price_url: dict) -> None:
    """Обрабатывает информацию о ключе игры из страницы игры сайта steampay.com

    :param game_name: название игры, введенное пользователем для поиска цен
    :param dict_price_url: словарь для заполнения ценой, ссылкой и названием
    """

    # Формирование ссылки для перехода на страницу игры
    game_name_link = '-'.join(list(game_name.split(' ')))

    url_steampay = URL_STEAMPAY.format(game_name_link=game_name_link)

    try:
        response_steampay = requests.get(url_steampay)
        if response_steampay.status_code != 200:
            raise APIException

        soup_steampay = BeautifulSoup(response_steampay.text, 'lxml')

        # Проверка на наличие ключа в продаже
        check_key_in_stock(soup_steampay)

        # Проверка региона Росссия
        check_ru_region(soup_steampay)

    except APIException:
        pass
    except FilterException:
        pass

    else:
        # Формирование цены игры и добавление в словарь
        gameprice_form(dict_price_url, soup_steampay, url_steampay)


def check_key_in_stock(soup_steampay: BeautifulSoup) -> None:
    """Проверяет наличие ключа в продаже"""
    key_in_stock = soup_steampay.find(
        'span', class_='product__advantages-orange')
    stock = str(key_in_stock)
    if 'закончился' in stock:
        raise FilterException
    if 'ожидается' in stock:
        raise FilterException


def check_ru_region(soup_steampay: BeautifulSoup) -> None:
    """Проверяет соответствие региона Росссия"""
    region = soup_steampay.find_all(
        'ul', class_='product__info-inner-block-list')
    sell_region = str(region[3])
    if 'Россия' not in sell_region:
        raise FilterException


def gameprice_form(
        dict_price_url: dict, soup_steampay: BeautifulSoup, url_steampay: str)\
        -> None:
    """Формирует цену игры"""
    game_name_steampay = soup_steampay.find(
        'h1', class_='product__title')
    name_steampay = game_name_steampay.text.strip()
    line = str(soup_steampay.find(
        'div', class_='product__current-price'))
    line_in_list = line.split(' ')
    price_in_element = ''.join([x for x in line_in_list if x.isdigit()])
    # Цена игры и ссылка добавляются в словарь
    dict_price_url[int(price_in_element)] = url_steampay, name_steampay


if __name__ == '__main__':

    from src.constants import TYPE_GAME_NAME

    game_name = input(TYPE_GAME_NAME).lower()  # напр. Superliminal
    dict_price_url = {}
    steam_pay(game_name, dict_price_url)
    print(dict_price_url)
