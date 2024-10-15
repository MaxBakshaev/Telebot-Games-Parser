import requests, bs4
# Поиск ключей на сайте steampay.com

def steam_pay(game_name, dict_price_url):
    # Формирование ссылки для перехода на страницу игры
    game_name_link = '-'.join(list(game_name.split(' ')))
    url_steampay = f'https://steampay.com/game/{game_name_link}'

    response_steampay = requests.get(url_steampay)

    try:
        response_steampay.raise_for_status()
        soup_steampay = bs4.BeautifulSoup(response_steampay.text, 'lxml')

        # Проверка на наличие ключа в продаже
        key_in_stock = soup_steampay.find('span', class_='product__advantages-orange')
        stock = str(key_in_stock)
        if 'закончился' not in stock and 'ожидается' not in stock:

            # Проверка региона Росссия
            region = soup_steampay.find_all('ul', class_='product__info-inner-block-list')
            sell_region = str(region[3])
            if 'Россия' in sell_region:

                # Если страница игры проходит проверку, то выполняется код
                # Формирование цены игры
                game_name_steampay = soup_steampay.find('h1', class_='product__title')
                name_steampay = game_name_steampay.text.strip()
                line = str(soup_steampay.find('div', class_='product__current-price'))
                line_in_list = line.split(' ')
                element = line_in_list[1]
                price_in_element = ''.join([x for x in element if x.isdigit()])
                # Цена игры и ссылка добавляются в словарь
                dict_price_url[int(price_in_element)] = url_steampay, name_steampay
    except:
        pass

if __name__ == '__main__':
    game_name = input('Введите название игры: ').lower()
    dict_price_url = {}
    steam_pay(game_name, dict_price_url)
    print(dict_price_url)