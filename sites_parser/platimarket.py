import requests, bs4
# Поиск ключей на сайте plati.ru

def plati(game_name, dict_price_url):
    # Количество продавцов на страницу
    pagesize = 10
    # Номер страницы
    pagenum = 1

    # API поиск игр
    url_plati = f'https://plati.io/api/search.ashx?query={game_name}&pagesize={pagesize}&pagenum={pagenum}&visibleOnly=True&response=json'
    response_plati = requests.get(url_plati)

    try:
        response_plati.raise_for_status()
        response_dict = response_plati.json()
        # Список продавцов
        repo_dicts = response_dict['items']
        # Проверка каждого продавца из списка на надежность
        for repo_dict in repo_dicts:
            try:
                # Строка 'name' с названием игры на сайте
                full_name_in_site = repo_dict['name']
                name_in_site = full_name_in_site.lower()
                # Соответствие названия игры
                if game_name in name_in_site:
                    banwords = ['ps3', 'ps4', 'ps5', 'без рф', 'no ru', 'без активации в рф', 'не включая рф',
                                'не активируется в рф', 'ubisoft', 'xbox', 'origin', 'gog', 'аренда',
                                'новый аккаунт', 'чистый аккаунт', 'пустой аккаунт', 'без ru', 'не для рф',
                                'не для россии', 'не для ru', 'аренда', 'rockstar', 'Rockstar']
                    if any(word in name_in_site for word in banwords):
                        raise Exception
                    else:
                        # Соответствие платформы steam
                        description = repo_dict['description'].lower()
                        banwords_description = ['без рф', 'недоступна в рф', 'недоступно в рф', 'недоступна для россии',
                                                'недоступна для аккаунтов россии', 'без активации в рф', 'не включая рф',
                                                'не активируется в рф', 'кроме рф', 'кроме россии', 'не работает в рф',
                                                'не работает в россии', 'без ru', 'не для рф', 'оффлайн steam',
                                                'steam аккаунт', 'аккаунт steam', 'доступ к счету', 'steam-аккаунт',
                                                'невозможно получить на аккаунтах с регионом рф', 'аренда',
                                                'Недоступно для аккаунтов: Россия', 'нельзя активировать с российским']
                        if any(word_des in description for word_des in banwords_description):
                            raise Exception
                        else:
                            if 'steam' in description or 'steam' in name_in_site:
                                # Рейтинг продавца
                                if repo_dict['seller_rating'] > 100:
                                    # Количество продаж
                                    sold = repo_dict['numsold']
                                    if sold > 30:
                                        # Количество возвратов
                                        returns = repo_dict['count_returns']
                                        if returns < 5:
                                            # Соотношение возвратов к продажам
                                            if returns / sold < 0.01:
                                                # Количество позитивных отзывов
                                                positiveresponses = repo_dict['count_positiveresponses']
                                                if positiveresponses > 5:
                                                    # Количество негативных отзывов
                                                    negativeresponses = repo_dict['count_negativeresponses']
                                                    if negativeresponses < 5:
                                                        # Соотношение негативных отзывов к позитивным
                                                        if negativeresponses / positiveresponses < 0.01:
                                                            # Проверка на наличие ключа в продаже
                                                            try:
                                                                request_site = repo_dict['url']
                                                                response_site = requests.get(request_site)
                                                                soup_plati = bs4.BeautifulSoup(response_site.text, 'lxml')
                                                                key_in_site = soup_plati.find('div',
                                                                                              class_='goods_order_form_subscribe')
                                                                if key_in_site == None:
                                                                    # Если продавец проходит все проверки, то цена
                                                                    # игры и ссылка добавляются в словарь
                                                                    repo_price = repo_dict['price_rur']
                                                                    repo_url = repo_dict['url']
                                                                    dict_price_url[repo_price] = repo_url, full_name_in_site
                                                            except:
                                                                continue
            except:
                continue
    except:
        pass

if __name__ == '__main__':
    game_name = input('Введите название игры: ').lower()
    dict_price_url = {}
    plati(game_name, dict_price_url)
    print(dict_price_url)