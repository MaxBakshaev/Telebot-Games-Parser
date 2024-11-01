"""Модуль для поиска самых ожидаемых игр"""

import telebot
import requests
from bs4 import BeautifulSoup

from src.constants import (
    HEADERS, URL_EXPECTED, URL_EXPECTED_SHORT, RESULT_EXPECTED_SHORT,
    RESULT_EXPECTED)
from src.exceptions import RequestException


def get_expected(
        bot: telebot.TeleBot, message: telebot.types.Message,
        amount_posts: int) -> None:
    """Получает запрос с количеством игр и переходит к парсингу игр"""

    try:
        request_expected = requests.get(URL_EXPECTED, headers=HEADERS)
        if request_expected.status_code != 200:
            raise RequestException

    except RequestException:
        bot.send_message(message.chat.id, 'Не найдено')

    else:
        soup_expected = BeautifulSoup(request_expected.text, 'lxml')

        # перечень всех ожидаемых игр
        all_posts = (
            soup_expected.find_all('div', class_='game_search_par'))

        for post in all_posts[0:amount_posts]:
            try:
                # парсинг всей информации по играм
                parse_posts(bot, message, post)
            except Exception:
                continue


def parse_posts(
        bot: telebot.TeleBot, message: telebot.types.Message,
        post: BeautifulSoup) -> None:
    """Парсит всю информацию по играм"""

    title, release_date, short_description, image_url = (
        get_short_parameters(post))

    try:
        link_url = get_link_url(post)
        request_expect = requests.get(link_url, headers=HEADERS)
        if request_expect.status_code != 200:
            raise RequestException

    except RequestException:
        print_result_short(
            bot, message, title, release_date, short_description, image_url)

    else:
        soup_expect = BeautifulSoup(
            request_expect.text, 'lxml')

        full_description, big_img_url, youtube_urls, system_text = (
            get_parameters(soup_expect, short_description, image_url))

        print_result_full(
            bot, message, big_img_url, title, release_date, full_description,
            youtube_urls, system_text, short_description, image_url)


def get_short_parameters(post: BeautifulSoup) -> tuple:
    """Получает параметры для вывода короткого результата"""

    # название
    title = get_title(post)
    # дата релиза
    release_date = get_release_date(post)
    # короткое описание
    short_description = get_short_description(post)
    # ссылка на маленькую картинку
    image_url = get_image_small(post)

    return title, release_date, short_description, image_url


def get_title(post: BeautifulSoup) -> str:
    """Получает название игры"""
    return post.find('div', class_='title').getText().strip()


def get_release_date(post: BeautifulSoup) -> str:
    """Получает дату релиза"""
    try:
        return post.find('div', class_='date').getText().strip()
    except Exception:
        return 'неизвестно'


def get_short_description(post: BeautifulSoup) -> str:
    """Получает краткое описание"""
    try:
        game_desc = post.find(
            'div', class_='description').getText().strip()
        return f'{game_desc}\n'
    except Exception:
        return ''


def get_image_small(post: BeautifulSoup) -> str:
    """Получает ссылку на маленькую картинку"""
    try:
        image = str(post.find(class_='aimg'))
        image_split = (image.split(
            'data-src="')[1]).split('" height')[0]
        return f'{URL_EXPECTED_SHORT}{image_split}'
    except Exception:
        return ''


def print_result_short(
        bot: telebot.TeleBot, message: telebot.types.Message, title: str,
        release_date: str, short_description: str, image_url: str):
    """Выводит короткий результат"""
    bot.send_photo(
        message.chat.id,
        image_url,
        caption=RESULT_EXPECTED_SHORT.format(
            title=title,
            release_date=release_date,
            short_description=short_description),
        parse_mode="html")


def get_link_url(post: BeautifulSoup) -> str:
    """Получает ссылку на страницу игры"""
    try:
        link = str(post.find('a'))
        link_split = (link.split('href="')[1]).split('"></a>')[0]
        return f'{URL_EXPECTED_SHORT}{link_split}'
    except Exception:
        return ''


def get_parameters(
        soup_expect: BeautifulSoup, short_description: str, image_url: str) \
        -> tuple:
    """Получает параметры для вывода полного результата"""

    # полное описание
    full_description = get_full_description(soup_expect, short_description)
    # большая картинка
    big_img_url = get_big_image_url(soup_expect, image_url)
    # ссылки на видео игры в ютубе
    youtube_urls = get_youtube_urls(soup_expect)
    # минимальные системные требования
    system_text = get_system_text(soup_expect)

    return full_description, big_img_url, youtube_urls, system_text


def get_full_description(soup_expect: BeautifulSoup, short_description: str) \
        -> str:
    """Получает полное описание"""
    try:
        full_desc = str((soup_expect.find(
            'div', class_='article_block a_text')).getText())
        return f'{full_desc}\n'
    except Exception:
        return short_description


def get_big_image_url(soup_expect: BeautifulSoup, image_url: str) -> str:
    """Получает ссылку на большую картинку"""
    try:
        big_photo = str(soup_expect.find(
            'div', class_='img_holder hasslider'))
        big_img = \
            (big_photo.split('data-src="')[1]).split('" height')[0]
        return f'{URL_EXPECTED_SHORT}{big_img}'
    except Exception:
        return image_url


def get_youtube_urls(soup_expect: BeautifulSoup) -> str:
    """Получает ссылки на видео игры в ютубе"""
    try:
        info = str(soup_expect.find_all('li', class_='iv')).split(' ')
        youtube_links = []
        for element in info:
            if 'data-src="//www.youtube.com' in element:
                link = element.split('data-src="//')[1].split('"')[0]
                youtube_links.append(link)
        youtube = '\n'.join(youtube_links)
        if len(youtube_links) != 0:
            return f'{youtube}\n'
        else:
            raise Exception
    except Exception:
        return ''


def get_system_text(soup_expect: BeautifulSoup) -> str:
    """Получает минимальные системные требования игры"""
    try:
        system_recommended = (soup_expect.find_all(
            'div', class_='reqs_'))
        system_min = str(system_recommended[0].getText('\n')).strip()
        sys_min = system_min.split('Минимальные:')[1].strip()
        if 'Клавиатура, мышь' in sys_min:
            sys_min = sys_min.split('Клавиатура, мышь')[0]
        return (f'Минимальные системные требования:\n'
                f'{sys_min}')
    except Exception:
        return ''


def print_result_full(
        bot: telebot.TeleBot, message: telebot.types.Message, big_img_url: str,
        title: str, release_date: str, full_description: str,
        youtube_urls: str, system_text: str, short_description: str,
        image_url: str) -> None:
    """Выводит полный результат"""
    try:
        bot.send_photo(
            message.chat.id,
            big_img_url,
            caption=RESULT_EXPECTED.format(
                title=title,
                release_date=release_date,
                full_description=full_description,
                youtube_urls=youtube_urls,
                system_text=system_text),
            parse_mode="html")

    except Exception:
        # Выводит короткий результат
        print_result_short(
            bot, message, title, release_date, short_description,
            image_url)


if __name__ == '__main__':

    def parse_posts_(post: BeautifulSoup) -> None:
        """Парсит всю информацию по играм"""

        title, release_date, short_description, image_url = (
            get_short_parameters(post))

        try:
            link_url = get_link_url(post)
            request_expect = requests.get(link_url, headers=HEADERS)
            if request_expect.status_code != 200:
                raise RequestException

        except RequestException:
            print(
                f'{title}\n'
                f'{image_url}\n'
                f'{release_date}\n'
                f'\n'
                f'{short_description}\n')

        else:
            soup_expect = BeautifulSoup(request_expect.text, 'lxml')

            full_description, big_img_url, youtube_urls, system_text = (
                get_parameters(soup_expect, short_description, image_url))

            try:
                print(
                    f'{title}\n'
                    f'{big_img_url}\n'
                    f'{release_date}\n'
                    f'\n'
                    f'{full_description}\n'
                    f'{youtube_urls}\n'
                    f'{system_text}\n')
            except Exception:
                print(
                    f'{title}\n'
                    f'{image_url}\n'
                    f'{release_date}\n'
                    f'\n'
                    f'{short_description}\n')


    amount_posts = int(input('Введите число от 1 до 40: '))
    try:
        request_expected = requests.get(URL_EXPECTED, headers=HEADERS)
        if request_expected.status_code != 200:
            raise RequestException

    except RequestException:
        print('Не найдено')

    else:
        soup_expected = BeautifulSoup(request_expected.text, 'lxml')

        # перечень всех ожидаемых игр
        all_posts = (
            soup_expected.find_all('div', class_='game_search_par'))

        for post in all_posts[0:amount_posts]:
            try:
                # парсинг всей информации по играм
                parse_posts_(post)
            except Exception:
                continue
