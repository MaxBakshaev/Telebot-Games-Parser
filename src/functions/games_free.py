"""Модуль для поиска раздач бесплатных игр"""

import telebot
import requests
from bs4 import BeautifulSoup

from src.constants import HEADERS, URL_GAMES_FREE
from src.exceptions import APIException


def free_games(bot: telebot.TeleBot, message: telebot.types.Message):
    """Находит раздачи и выводит информацию о них"""

    try:
        request_games = requests.get(URL_GAMES_FREE, headers=HEADERS)
        if request_games.status_code != 200:
            raise APIException

    except APIException:
        bot.send_message(message.chat.id, 'Не найдено')

    else:
        soup_games = BeautifulSoup(request_games.text, 'lxml')

        # перечень всех постов с раздачей игр
        all_posts = soup_games.find_all(
            'div', class_='col-lg-4 col-md-4 three-columns post-box')

        for post in all_posts:
            post_text = post.getText()
            splitted_text = post_text.split('\n')

            post_info = []

            for element in splitted_text:
                if 'аздач' in element:
                    post_info.append(element)

            # раздача + название игры
            game_info = post_info[1].split(' ')
            # ссылка на игру
            post_link = game_info[2]

            if 'http' in post_link:
                bot.send_message(
                    message.chat.id, f'<b>{post_info[0]}:</b>\n'
                                     f'{post_link}', parse_mode="html")


if __name__ == '__main__':

    try:
        request_games = requests.get(URL_GAMES_FREE, headers=HEADERS)
        if request_games.status_code != 200:
            raise APIException

    except APIException:
        print('Не найдено')

    else:
        soup_games = BeautifulSoup(request_games.text, 'lxml')
        all_posts = soup_games.find_all(
            'div', class_='col-lg-4 col-md-4 three-columns post-box')

        for post in all_posts:
            post_text = post.getText()
            splitted_text = post_text.split('\n')
            post_info = []

            for element in splitted_text:
                if 'аздач' in element:
                    post_info.append(element)

            game_info = post_info[1].split(' ')
            post_link = game_info[2]

            if 'http' in post_link:
                print(f'{post_info[0]}\n'
                      f'{post_link}')
