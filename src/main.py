"""Главный модуль, запускает бота"""

import os
import time

from dotenv import load_dotenv
import telebot

from constants import (
    GREETING_TEXT, HELP_TEXT, TYPE_GAME_NAME, WAITING_TEXT, BAN_SYMBOLS,
    KEYS_NOT_FOUND)
from functions import platimarket, steampay, print_result, games_free

time.sleep(5)

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> telebot.types.Message:
    """Выводит сообщение при входе"""
    return bot.send_message(message.chat.id, GREETING_TEXT, parse_mode='html')


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message) -> telebot.types.Message:
    """Показывает основные команды"""
    return bot.send_message(message.chat.id, HELP_TEXT, parse_mode='html')


@bot.message_handler(commands=['search'])
def search_game(message: telebot.types.Message) -> None:
    """Выводит сообщение, после которого запускается функция поиска ключей"""
    bot.send_message(
        message.chat.id, TYPE_GAME_NAME)
    bot.register_next_step_handler(message, find_keys)


def find_keys(message: telebot.types.Message) -> None:
    """Находит самые дешевые ключи игр"""

    game_name = message.text.lower()

    # проверка на введенные пользователем запрещеные символы
    bad_sym = check_bad_symbols(game_name, message)

    if not bad_sym:

        msg = bot.send_message(message.chat.id, WAITING_TEXT)

        # словарь для добавления цены, ссылки и названий игр
        dict_price_url = {}

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

    else:
        bot.register_next_step_handler(message, find_keys)


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


def check_bad_symbols(game_name: str, message: telebot.types.Message) \
        -> bool:
    """Не дает искать название игры из сообщения с запрещенными символами"""
    if set(game_name) & BAN_SYMBOLS:
        bot.send_message(message.chat.id, KEYS_NOT_FOUND)
        return True


@bot.message_handler(commands=['free'])
def search_free_games(message: telebot.types.Message) -> None:
    """Находит раздачи бесплатных игр"""

    mseg = bot.send_message(message.chat.id, WAITING_TEXT)

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


if __name__ == '__main__':
    bot.polling(none_stop=True)
