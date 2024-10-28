"""Модуль для вывода до 5 самых дешевых цен игр с ссылкой и названием"""

import telebot

from src.constants import (
    KEYS_NOT_FOUND, RESULT_MSG_5, RESULT_MSG_4, RESULT_MSG_3, RESULT_MSG_2,
    RESULT_MSG_1)


def print_result(
        sorted_prices: list, bot: telebot.TeleBot,
        message: telebot.types.Message) -> telebot.types.Message:
    """Выводит до 5 самых дешевых цен игр с ссылкой и названием

    :param sorted_prices: Список с ценами игр по возрастанию, ссылкой и
    названием
    """
    len_pricelist = len(sorted_prices)

    try:
        result = get_formatted_text(len_pricelist, sorted_prices)
        print_result_text(bot, message, result)
    except Exception:
        return bot.send_message(message.chat.id, KEYS_NOT_FOUND)


def get_formatted_text(
        len_pricelist: int, sorted_prices: list) -> str:
    """Форматирует текст для сообщения вывода результата поиска игр"""

    if len_pricelist >= 5:
        return RESULT_MSG_5.format(sorted_prices=sorted_prices)
    elif len_pricelist == 4:
        return RESULT_MSG_4.format(sorted_prices=sorted_prices)
    elif len_pricelist == 3:
        return RESULT_MSG_3.format(sorted_prices=sorted_prices)
    elif len_pricelist == 2:
        return RESULT_MSG_2.format(sorted_prices=sorted_prices)
    elif len_pricelist == 1:
        return RESULT_MSG_1.format(sorted_prices=sorted_prices)
    else:
        raise Exception


def print_result_text(
        bot: telebot.TeleBot, message: telebot.types.Message, result: str) \
        -> telebot.types.Message:
    """ Выводит текст сообщения с результатом поиска игр"""
    return bot.send_message(message.chat.id, result, parse_mode="html")


if __name__ == '__main__':
    from src.constants import EXAMPLE_SORTED_PRICES
    result = RESULT_MSG_5.format(sorted_prices=EXAMPLE_SORTED_PRICES)
    print(result)
