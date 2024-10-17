from sites_parser.platimarket import plati
from sites_parser.steampay import steam_pay
from sites_parser.games_free import free_games
from print_result import print_result

import os, time

import telebot
from dotenv import load_dotenv

time.sleep(5)

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Привет, выбери команду:</b>\n'
                                      '1. /search - найти самые дешевые игры в Steam\n'
                                      '2. /free - получить информацию о раздаче бесплатных игр', parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Нажмите на команду или введите ее:</b>\n'
                                      '1. /search - найти самые дешевые игры в Steam\n'
                                      '2. /free - получить информацию о раздаче бесплатных игр', parse_mode='html')

# =====================================================================================================================
# Поиск ключей
@bot.message_handler(commands=['search'])
def search_game(message):
    bot.send_message(message.chat.id, 'Введите название игры, желательно, полное 😉')
    bot.register_next_step_handler(message, find_keys)

def find_keys(message):
    msg = bot.send_message(message.chat.id, 'Запрос выполняется...\nПожалуйста, ожидайте ~10 секунд')
    game_name = message.text.lower()
    # Словарь с ценой, ссылкой и названием игр
    dict_price_url = {}

    # Поиск ключей на сайте plati.ru
    plati(game_name, dict_price_url)

    # Поиск ключей на сайте steampay.com
    steam_pay(game_name, dict_price_url)

    # Сортировка полученных цен по возрастанию
    sorted_prices = sorted(dict_price_url.items())

    # Удалить сообщение msg
    bot.delete_message(message.chat.id, msg.id)

    # Вывод результата для топ-5 цен
    print_result(sorted_prices, bot, message)

    # Что делать после вывода результата
    bot.register_next_step_handler(message, next_step)

def next_step(message):
    # Ввести команду
    if '/start' in message.text:
        start(message)
    elif '/free' in message.text:
        search_free_games(message)
    elif '/help' in message.text:
        help(message)
    elif '/search' in message.text:
        search_game(message)
    # Или продолжить искать игры
    else:
        find_keys(message)

# =====================================================================================================================
# Поиск раздачи бесплатных игр
@bot.message_handler(commands=['free'])
def search_free_games(message):
    # Получить информацию о раздаче игр
    free_games(bot, message)

    # Что делать после вывода результата
    bot.register_next_step_handler(message, next_step_2)

def next_step_2(message):
    # Ввести команду
    if '/start' in message.text:
        start(message)
    elif '/free' in message.text:
        search_free_games(message)
    elif '/search' in message.text:
        search_game(message)
    else:
        help(message)

# =====================================================================================================================


bot.polling(none_stop=True)