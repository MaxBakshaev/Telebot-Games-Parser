"""Главный модуль, запускает бота"""

import os
import time

from dotenv import load_dotenv
import telebot

from src.constants import (
    GREETING_TEXT, HELP_TEXT, TYPE_GAME_NAME, WAITING_TEXT, BAN_SYMBOLS,
    KEYS_NOT_FOUND, HOW_MANY_GAMES_PRINT)
# from functions import platimarket, steampay, print_result, games_free, expected
from src.functions.platimarket import plati
from src.functions.steampay import steam_pay
from src.functions.print_result import print_result
from src.functions.games_free import free_games
from src.functions.expected import get_expected

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

    bot.register_next_step_handler(message, step_after_search_game)


def step_after_search_game(message: telebot.types.Message) -> None:
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
    elif '/expect' in message.text:
        most_expected_games(message)
    # или продолжить искать игры
    else:
        find_keys(message)


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
        bot.register_next_step_handler(message, step_after_search_game)

    else:
        bot.register_next_step_handler(message, step_after_search_game)


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
    free_games(bot, message)

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
    elif '/expect' in message.text:
        most_expected_games(message)
    else:
        helper(message)


@bot.message_handler(commands=['expect'])
def most_expected_games(message: telebot.types.Message) -> None:
    """Запрашивает количество игр и переходит к функции поиска"""

    bot.send_message(message.chat.id, HOW_MANY_GAMES_PRINT)

    bot.register_next_step_handler(message, step_after_most_expected)


def step_after_most_expected(message: telebot.types.Message) -> None:
    """Действие после завершения функции find_most_expected_games()"""

    # Ввести команду
    if '/start' in message.text:
        start(message)
    elif '/free' in message.text:
        search_free_games(message)
    elif '/search' in message.text:
        search_game(message)
    elif '/expect' in message.text:
        most_expected_games(message)
    elif '/help' in message.text:
        helper(message)
    else:
        find_most_expected_games(message)


def find_most_expected_games(message):
    """Получает количество игр, проверяет его на запрещенные символы и
    переходит к функции поиска самых ожидаемых игр"""

    message_amount_games = message.text.lower()

    # проверка на введенные пользователем запрещеные символы
    bad_sym = check_bad_symbols_(message_amount_games)

    if not bad_sym:
        try:
            amount_posts = int(message_amount_games)

        except ValueError:
            bot.send_message(
                message.chat.id, HOW_MANY_GAMES_PRINT)
            bot.register_next_step_handler(message, step_after_most_expected)

        else:
            if amount_posts in range(1, 41):

                # Получить информацию об ожидаемых играх
                get_expected(bot, message, amount_posts)

                # Что делать после вывода результата
                bot.register_next_step_handler(
                    message, step_after_most_expected)

            else:
                bot.send_message(
                    message.chat.id, HOW_MANY_GAMES_PRINT)
                bot.register_next_step_handler(
                    message, step_after_most_expected)
    else:
        bot.send_message(
            message.chat.id, HOW_MANY_GAMES_PRINT)
        bot.register_next_step_handler(message, step_after_most_expected)


def check_bad_symbols_(message_amount_games: str) -> bool:
    """Не дает искать количество игр из сообщения с запрещенными символами"""
    if set(message_amount_games) & BAN_SYMBOLS:
        return True


if __name__ == '__main__':
    bot.polling(none_stop=True)
