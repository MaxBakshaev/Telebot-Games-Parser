"""Модуль для поиска ключей на сайте steampay.com"""

import requests
from bs4 import BeautifulSoup


def steam_pay(game_name: str, dict_price_url: dict) -> None:
    """Обрабатывает информацию о ключе игры из страницы игры сайта steampay.com

    :param game_name: название игры, введенное пользователем для поиска цен
    :param dict_price_url: словарь для заполнения по форме {int(цена): (ссылка,
     название с сайта)}
    """

    # Формирование ссылки для перехода на страницу игры
    game_name_link = '-'.join(list(game_name.split(' ')))
    url_steampay = f'https://steampay.com/game/{game_name_link}'

    try:
        response_steampay = requests.get(url_steampay)
        response_steampay.raise_for_status()
        soup_steampay = BeautifulSoup(response_steampay.text, 'lxml')

        # Проверка на наличие ключа в продаже
        check_key_in_stock(soup_steampay)

        # Проверка региона Росссия
        check_ru_region(soup_steampay)

        # Формирование цены игры и добавление в словарь
        gameprice_form(dict_price_url, soup_steampay, url_steampay)

    except Exception:
        pass


def check_key_in_stock(soup_steampay: BeautifulSoup) -> None:
    """Проверяет наличие ключа в продаже"""

    key_in_stock = soup_steampay.find(
        'span', class_='product__advantages-orange')
    stock = str(key_in_stock)
    if 'закончился' in stock:
        raise Exception
    if 'ожидается' in stock:
        raise Exception


def check_ru_region(soup_steampay: BeautifulSoup) -> None:
    """Проверяет соответствие региона Росссия"""

    region = soup_steampay.find_all(
        'ul', class_='product__info-inner-block-list')
    sell_region = str(region[3])
    if 'Россия' not in sell_region:
        raise Exception


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
    element = line_in_list[1]
    price_in_element = ''.join([x for x in element if x.isdigit()])

    # Цена игры и ссылка добавляются в словарь
    dict_price_url[int(price_in_element)] = url_steampay, name_steampay


if __name__ == '__main__':
    game_name = input('Введите название игры: ').lower()  # напр. Superliminal
    dict_price_url: dict[int, tuple[str, str]] = {}
    steam_pay(game_name, dict_price_url)
    print(dict_price_url)
