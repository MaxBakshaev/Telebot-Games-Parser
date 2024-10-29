GREETING_TEXT = '''
<b>Привет, выбери команду:</b>
1. /search - найти самые дешевые игры в Steam
2. /free - получить информацию о раздаче бесплатных игр
'''

HELP_TEXT = '''
<b>Нажмите на команду или введите ее:</b>
1. /search - найти самые дешевые игры в Steam
2. /free - получить информацию о раздаче бесплатных игр
'''

TYPE_GAME_NAME = 'Введите название игры, желательно, полное 😉 '

BAN_SYMBOLS = set('@/*#!$%^?\[]{}-_)+(=;`~.,<>\'"|')

WAITING_TEXT = '''
Запрос выполняется.
Пожалуйста, ожидайте...
'''

BANWORDS_IN_NAME = (
        'ps3', 'ps4', 'ps5', 'без рф', 'no ru', 'без активации в рф',
        'не включая рф', 'не активируется в рф', 'ubisoft', 'xbox', 'origin',
        'gog', 'аренда', 'новый аккаунт', 'чистый аккаунт', 'пустой аккаунт',
        'без ru', 'не для рф', 'не для россии', 'не для ru', 'аренда',
        'rockstar', 'rockstar'
    )

BANWORDS_IN_DESCRIPTION = (
        'без рф', 'недоступна в рф', 'недоступно в рф',
        'недоступна для россии', 'недоступна для аккаунтов россии',
        'без активации в рф', 'не включая рф', 'не активируется в рф',
        'кроме рф', 'кроме россии', 'не работает в рф', 'не работает в россии',
        'без ru', 'не для рф', 'оффлайн steam', 'доступ к счету',
        'невозможно получить на аккаунтах с регионом рф', 'аренда',
        'недоступно для аккаунтов: Россия', 'нельзя активировать с российским'
    )

# количество продавцов на страницу
PAGESIZE = 10

# номер страницы
PAGENUM = 1

URL_PLATI = 'https://plati.io/api/search.ashx?query={game_name}&pagesize={pagesize}&pagenum={pagenum}&visibleOnly=True&response=json'

URL_STEAMPAY = 'https://steampay.com/game/{game_name_link}'

URL_GAMES_FREE = 'https://freesteam.ru/category/active/'

HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/webp,image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36'
        }

RESULT_MSG_5 = '''
<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}
{sorted_prices[0][1][1]}\n
<b>{sorted_prices[1][0]} руб.</b> - {sorted_prices[1][1][0]}
{sorted_prices[1][1][1]}\n
<b>{sorted_prices[2][0]} руб.</b> - {sorted_prices[2][1][0]}
{sorted_prices[2][1][1]}\n
<b>{sorted_prices[3][0]} руб.</b> - {sorted_prices[3][1][0]}
{sorted_prices[3][1][1]}\n
<b>{sorted_prices[4][0]} руб.</b> - {sorted_prices[4][1][0]}
{sorted_prices[4][1][1]}
'''

RESULT_MSG_4 = '''
<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}
{sorted_prices[0][1][1]}\n
<b>{sorted_prices[1][0]} руб.</b> - {sorted_prices[1][1][0]}
{sorted_prices[1][1][1]}\n
<b>{sorted_prices[2][0]} руб.</b> - {sorted_prices[2][1][0]}
{sorted_prices[2][1][1]}\n
<b>{sorted_prices[3][0]} руб.</b> - {sorted_prices[3][1][0]}
{sorted_prices[3][1][1]}
'''

RESULT_MSG_3 = '''
<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}
{sorted_prices[0][1][1]}\n
<b>{sorted_prices[1][0]} руб.</b> - {sorted_prices[1][1][0]}
{sorted_prices[1][1][1]}\n
<b>{sorted_prices[2][0]} руб.</b> - {sorted_prices[2][1][0]}
{sorted_prices[2][1][1]}
'''

RESULT_MSG_2 = '''
<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}
{sorted_prices[0][1][1]}\n
<b>{sorted_prices[1][0]} руб.</b> - {sorted_prices[1][1][0]}
{sorted_prices[1][1][1]}
'''

RESULT_MSG_1 = '''
<b>{sorted_prices[0][0]} руб.</b> - {sorted_prices[0][1][0]}
{sorted_prices[0][1][1]}
'''

KEYS_NOT_FOUND = '''
Ключи не найдены.
Пожалуйста, проверьте точное написание названия игры.
Попробуйте заменить цифры на римские (например, Mafia II)
'''

EXAMPLE_SORTED_PRICES = [
    (3259, ('https://plati.market/itm/3901794',
            'STARFIELD (STEAM/RU) 0% КАРТОЙ + ПОДАРОК')),
    (3399, ('https://plati.market/itm/3898631',
            'Starfield (Steam)  🔵 РФ-СНГ')),
    (5299, ('https://plati.market/itm/3898632',
            'Starfield Premium Edition (Steam)🔵 РФ-СНГ')),
    (5690, ('https://plati.market/itm/3782364',
            'STARFIELD * RU/KZ/СНГ/TR/AR * STEAM АВТОДОСТАВКА')),
    (5934, ('https://plati.market/itm/3782302',
            'STARFIELD STANDARD/PREMIUM STEAM ⚡️АВТО RU+TR+KZ')),
    (6990, ('https://plati.market/itm/3782532',
            '🌌🌟STARFIELD STEAM GIFT🌟🌌 ☑️РФ/МИР☑️')),
    (7990, ('https://plati.market/itm/3782367',
            'STARFIELD DIGITAL PREMIUM EDITION RU/KZ/СНГ/TR/AR')),
]
