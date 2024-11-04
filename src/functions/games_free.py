"""Модуль для поиска раздач бесплатных игр"""

import telebot
import requests
from bs4 import BeautifulSoup

from src.constants import HEADERS, URL_GAMES_FREE
from src.exceptions import RequestException


def free_games(bot: telebot.TeleBot, message: telebot.types.Message) -> None:
    """Находит раздачи и выводит информацию о них"""

    try:
        request_games = requests.get(URL_GAMES_FREE, headers=HEADERS)
        if request_games.status_code != 200:
            raise RequestException

    except RequestException:
        bot.send_message(message.chat.id, 'Не найдено')

    else:
        soup_games = BeautifulSoup(request_games.text, 'lxml')

        # перечень всех постов с раздачей игр
        all_posts = soup_games.find_all(
            'div', class_='col-lg-4 col-md-4 three-columns post-box')

        for post in all_posts:
            # информация об игре
            post_info = post_get_post_info(post)

            # информация по игре, разбитая на слова
            game_title = post_info[1].split(' ')

            # Как только доходит до ссылки выводим результат
            for game_link in game_title:
                if 'http' in game_link:
                    free_games_print_result(bot, message, game_link, post_info)
                    break


def post_get_post_info(post: BeautifulSoup) -> list:
    """Возвращает заголовок игры со словом Раздача и названием игры"""
    post_info = []
    post_text = post.getText()
    splitted_text = post_text.split('\n')
    for element in splitted_text:
        if 'аздач' in element:
            post_info.append(element)
    return post_info


def free_games_print_result(
        bot: telebot.TeleBot, message: telebot.types.Message, game_link: str,
        post_info: list) -> None:
    """Выводит результат"""
    bot.send_message(
        message.chat.id, f'<b>{post_info[0]}:</b>\n'
                         f'{game_link}', parse_mode="html")


if __name__ == '__main__':

    try:
        request_games = requests.get(URL_GAMES_FREE, headers=HEADERS)
        if request_games.status_code != 200:
            raise RequestException

    except RequestException:
        print('Не найдено')

    else:
        soup_games = BeautifulSoup(request_games.text, 'lxml')
        all_posts = soup_games.find_all(
            'div', class_='col-lg-4 col-md-4 three-columns post-box')
        for post in all_posts:
            post_info = post_get_post_info(post)
            game_title = post_info[1].split(' ')
            for game_link in game_title:
                if 'http' in game_link:
                    print(f'{post_info[0]}\n'
                          f'{game_link}')
                    break
