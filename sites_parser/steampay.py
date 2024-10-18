# Поиск ключей на сайте steampay.com
import requests
from bs4 import BeautifulSoup


def steam_pay(game_name, dict_price_url):

    # Формирование ссылки для перехода на страницу игры
    game_name_link = '-'.join(list(game_name.split(' ')))
    url_steampay = f'https://steampay.com/game/{game_name_link}'

    try:
        response_steampay = requests.get(url_steampay)
        response_steampay.raise_for_status()
        soup_steampay = BeautifulSoup(response_steampay.text, 'lxml')

        # Проверка на наличие ключа в продаже
        key_in_stock = soup_steampay.find(
            'span', class_='product__advantages-orange')
        stock = str(key_in_stock)
        if 'закончился' in stock:
            raise Exception
        if 'ожидается' in stock:
            raise Exception

        # Проверка региона Росссия
        region = soup_steampay.find_all(
            'ul', class_='product__info-inner-block-list')
        sell_region = str(region[3])
        if 'Россия' not in sell_region:
            raise Exception

        # Формирование цены игры
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

    except Exception:
        pass


if __name__ == '__main__':
    game_name = input('Введите название игры: ').lower()
    dict_price_url = {}
    steam_pay(game_name, dict_price_url)
    print(dict_price_url)
