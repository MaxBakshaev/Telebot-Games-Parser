# Поиск ключей на сайте plati.ru
import requests
from bs4 import BeautifulSoup


def plati(game_name, dict_price_url):

    # количество продавцов на страницу
    pagesize = 10

    # номер страницы
    pagenum = 1

    banwords_name = [
        'ps3', 'ps4', 'ps5', 'без рф', 'no ru', 'без активации в рф',
        'не включая рф', 'не активируется в рф', 'ubisoft', 'xbox', 'origin',
        'gog', 'аренда', 'новый аккаунт', 'чистый аккаунт', 'пустой аккаунт',
        'без ru', 'не для рф', 'не для россии', 'не для ru', 'аренда',
        'rockstar', 'rockstar'
    ]

    banwords_description = [
        'без рф', 'недоступна в рф', 'недоступно в рф',
        'недоступна для россии', 'недоступна для аккаунтов россии',
        'без активации в рф', 'не включая рф', 'не активируется в рф',
        'кроме рф', 'кроме россии', 'не работает в рф', 'не работает в россии',
        'без ru', 'не для рф', 'оффлайн steam', 'доступ к счету',
        'невозможно получить на аккаунтах с регионом рф', 'аренда',
        'недоступно для аккаунтов: Россия', 'нельзя активировать с российским'
    ]

    # API поиск игр
    url_plati = (f'https://plati.io/api/search.ashx?query={game_name}&pagesize={pagesize}&pagenum={pagenum}&visibleOnly=True&response=json')

    try:
        response_plati = requests.get(url_plati)
        response_plati.raise_for_status()
        response_dict = response_plati.json()

        # список продавцов
        repo_dicts = response_dict['items']

        # Проверка продавцов из списка на надежность
        for repo_dict in repo_dicts:
            try:
                # Строка 'name' с названием игры на сайте
                full_name_in_site = repo_dict['name']
                name_in_site = full_name_in_site.lower()

                # Проверка названия игры
                if game_name not in name_in_site:
                    raise Exception

                # Проверка слов исключений для названия
                if any(word in name_in_site for word in banwords_name):
                    raise Exception

                # Проверка слов исключений для описания
                description = repo_dict['description'].lower()
                if any(word_des in description for word_des in
                       banwords_description):
                    raise Exception

                # Проверка платформы Steam
                if 'steam' not in name_in_site:
                    if 'steam' not in description:
                        raise Exception

                # Рейтинг продавца
                if repo_dict['seller_rating'] < 100:
                    raise Exception

                # Количество продаж
                sold = repo_dict['numsold']
                if sold < 30:
                    raise Exception

                # Количество возвратов
                returns = repo_dict['count_returns']
                if returns > 5:
                    raise Exception

                # Соотношение возвратов к продажам
                if returns / sold > 0.01:
                    raise Exception

                # Количество позитивных отзывов
                positiveresponses = repo_dict['count_positiveresponses']
                if positiveresponses < 5:
                    raise Exception

                # Количество негативных отзывов
                negativeresponses = repo_dict['count_negativeresponses']
                if negativeresponses > 5:
                    raise Exception

                # Соотношение негативных отзывов к позитивным
                if negativeresponses / positiveresponses > 0.01:
                    raise Exception

                # Проверка на наличие ключа в продаже
                try:
                    request_site = repo_dict['url']
                    response_site = requests.get(request_site)
                    response_site.raise_for_status()
                    soup_plati = BeautifulSoup(
                        response_site.text, 'lxml')

                    # Если есть этот тег, то товар не в продаже
                    key_in_site = soup_plati.find(
                        'div', class_='goods_order_form_subscribe')
                    if key_in_site is None:

                        # Формирование цены игры и ссылки
                        repo_price = repo_dict['price_rur']
                        repo_url = repo_dict['url']

                        # Цена игры и ссылка добавляются в словарь
                        dict_price_url[repo_price] = (
                            repo_url, full_name_in_site)

                except Exception:
                    raise Exception

            except Exception:
                continue

    except Exception:
        pass


if __name__ == '__main__':
    game_name = input('Введите название игры: ').lower()
    dict_price_url = {}
    plati(game_name, dict_price_url)
    print(dict_price_url)
