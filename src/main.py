"""Главный модуль, запускает бота"""

import os
import time

import telebot
from dotenv import load_dotenv

from functions import platimarket, steampay, print_result, games_free

time.sleep(5)

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> telebot.types.Message:
    """Выводит сообщение при входе"""

    return bot.send_message(
        message.chat.id,
        '<b>Привет, выбери команду:</b>\n'
        '1. /search - найти самые дешевые игры в Steam\n'
        '2. /free - получить информацию о раздаче бесплатных игр',
        parse_mode='html')


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message) -> telebot.types.Message:
    """Показывает основные команды"""

    return bot.send_message(
        message.chat.id,
        '<b>Нажмите на команду или введите ее:</b>\n'
        '1. /search - найти самые дешевые игры в Steam\n'
        '2. /free - получить информацию о раздаче бесплатных игр',
        parse_mode='html')


@bot.message_handler(commands=['search'])
def search_game(message: telebot.types.Message) -> None:
    """Выводит сообщение, после которого запускается функция поиска ключей"""

    bot.send_message(
        message.chat.id, 'Введите название игры, желательно, полное 😉')

    bot.register_next_step_handler(message, find_keys)


def find_keys(message: telebot.types.Message) -> None:
    """Находит самые дешевые ключи игр"""

    msg = bot.send_message(
        message.chat.id, 'Запрос выполняется...\n'
                         'Пожалуйста, ожидайте')

    game_name = message.text.lower()

    # словарь с ценой, ссылкой и названием игр
    dict_price_url: dict[int, tuple[str, str]] = {}

    # Поиск ключей на сайте plati.ru
    platimarket.plati(game_name, dict_price_url)

    # Поиск ключей на сайте steampay.com
    steampay.steam_pay(game_name, dict_price_url)

    # Сортировка полученных цен по возрастанию
    sorted_prices = sorted(dict_price_url.items())

    # Удалить сообщение msg
    bot.delete_message(message.chat.id, msg.id)

    # Вывод результата для топ-5 цен
    print_result.print_result(sorted_prices, bot, message)

    # Что делать после вывода результата
    bot.register_next_step_handler(message, step_after_find_keys)


def step_after_find_keys(message: telebot.types.Message) -> None:
    """Действие после завершения функции find_keys()"""

    # Ввести команду
    if '/start' in message.text:
        start(message)
    elif '/free' in message.text:
        search_free_games(message)
    elif '/help' in message.text:
        helper(message)
    elif '/search' in message.text:
        search_game(message)
    # или продолжить искать игры
    else:
        find_keys(message)


@bot.message_handler(commands=['free'])
def search_free_games(message: telebot.types.Message) -> None:
    """Находит раздачи бесплатных игр"""

    mseg = bot.send_message(
        message.chat.id, 'Запрос выполняется...\n'
                         'Пожалуйста, ожидайте')

    # Получить информацию о раздаче игр
    games_free.free_games(bot, message)

    # Удалить сообщение mseg
    bot.delete_message(message.chat.id, mseg.id)

    # Что делать после вывода результата
    bot.register_next_step_handler(message, step_after_search_free_games)


def step_after_search_free_games(message: telebot.types.Message) -> None:
    """Действие после завершения функции search_free_games()"""

    # Ввести команду
    if '/start' in message.text:
        start(message)
    elif '/free' in message.text:
        search_free_games(message)
    elif '/search' in message.text:
        search_game(message)
    else:
        helper(message)


bot.polling(none_stop=True)
