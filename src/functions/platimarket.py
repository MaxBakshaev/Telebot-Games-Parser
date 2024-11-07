"""Модуль для поиска ключей на сайте plati.ru"""

import requests
from bs4 import BeautifulSoup

from src.constants import (
    BANWORDS_IN_NAME, BANWORDS_IN_DESCRIPTION, PAGESIZE, PAGENUM, URL_PLATI)
from src.exceptions import APIException, FilterException


def plati(game_name: str, dict_price_url: dict) -> None:
    """Обрабатывает информацию о ключах игр из API сайта plati.ru

    :param game_name: название игры, введенное пользователем для поиска цен
    :param dict_price_url: словарь для заполнения ценой, ссылкой и названием
    """
    # API поиск игр
    url_plati = URL_PLATI.format(
        game_name=game_name,
        pagesize=PAGESIZE,
        pagenum=PAGENUM
    )

    try:
        response_plati = requests.get(url_plati)
        if response_plati.status_code != 200:
            raise APIException

    except APIException:
        pass

    else:

        response_dict = response_plati.json()

        # список продавцов
        repo_dicts = response_dict['items']

        # Проверка продавцов из списка на надежность
        check_reliability(
            dict_price_url, repo_dicts, BANWORDS_IN_NAME,
            BANWORDS_IN_DESCRIPTION, game_name)


def check_reliability(
        dict_price_url: dict, repo_dicts: list, BANWORDS_IN_NAME: tuple,
        BANWORDS_IN_DESCRIPTION: tuple, game_name: str) -> None:
    """Проверяет продавцов из списка на надежность"""

    for repo_dict in repo_dicts:
        try:
            # cтрока 'name' с названием игры на сайте
            full_name_in_site = repo_dict['name']
            name_in_site = full_name_in_site.lower()

            # Проверка надежности продавца по разным фильтрам
            check_different_filters(
                game_name, name_in_site, repo_dict, BANWORDS_IN_NAME,
                BANWORDS_IN_DESCRIPTION)

            # ссылка на игру
            repo_url = repo_dict['url']

            # Проверка на наличие ключа в продаже
            check_key_in_stock(repo_url)

            # цена игры
            repo_price = int(repo_dict['price_rur'])

        except FilterException:
            continue

        else:
            # Если проходит проверку на надежность, то
            # цена игры и ссылка добавляются в словарь
            dict_price_url[repo_price] = repo_url, full_name_in_site


def check_different_filters(
        game_name: str, name_in_site: str, repo_dict: dict,
        BANWORDS_IN_NAME: tuple, BANWORDS_IN_DESCRIPTION: tuple) -> None:
    """Проверяет надежность продавца по разным фильтрам"""

    # Проверка названия игры
    if game_name not in name_in_site:
        raise FilterException

    # Проверка слов исключений для названия
    if any(word in name_in_site for word in BANWORDS_IN_NAME):
        raise FilterException

    # Проверка слов исключений для описания
    description = repo_dict['description'].lower()
    if any(word_des in description for word_des in BANWORDS_IN_DESCRIPTION):
        raise FilterException

    # Проверка платформы Steam
    if 'steam' not in name_in_site:
        if 'steam' not in description:
            raise FilterException

    # Рейтинг продавца
    if repo_dict['seller_rating'] < 100:
        raise FilterException

    # Количество продаж
    sold = repo_dict['numsold']
    if sold < 30:
        raise FilterException

    # Количество возвратов
    returns = repo_dict['count_returns']
    if returns > 5:
        raise FilterException

    # Соотношение возвратов к продажам
    if returns / sold > 0.01:
        raise FilterException

    # Количество позитивных отзывов
    positiveresponses = repo_dict['count_positiveresponses']
    if positiveresponses < 5:
        raise FilterException

    # Количество негативных отзывов
    negativeresponses = repo_dict['count_negativeresponses']
    if negativeresponses > 5:
        raise FilterException

    # Соотношение негативных отзывов к позитивным
    if negativeresponses / positiveresponses > 0.01:
        raise FilterException


def check_key_in_stock(repo_url: str) -> None:
    """Проверяет наличие ключа в продаже"""

    try:
        response_site = requests.get(repo_url)
        if response_site.status_code != 200:
            raise APIException

        soup_plati = BeautifulSoup(
            response_site.text, 'lxml')

        # Если есть этот тег, то товар не в продаже
        key_in_site = soup_plati.find(
            'div', class_='goods_order_form_subscribe')
        if key_in_site is not None:
            raise FilterException

    except FilterException:
        raise FilterException

    except APIException:
        raise FilterException


if __name__ == '__main__':
    from src.constants import TYPE_GAME_NAME
    game_name = input(TYPE_GAME_NAME).lower()  # напр. disco elysium
    dict_price_url = {}
    plati(game_name, dict_price_url)
    print(dict_price_url)
