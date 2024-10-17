import requests
from bs4 import BeautifulSoup

def free_games(bot, message):
    try:
        url_epic = 'https://vk.com/freesteam'
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

        request_epic = requests.get(url_epic, headers=HEADERS)
        soup_epic = BeautifulSoup(request_epic.text, 'html.parser')
        all_posts = soup_epic.find_all('div', class_='wall_post_text')

        # Заголовок с названием игры
        all_text_about_game = all_posts[0].text.split(' Как получить игру')
        text_about_game = all_text_about_game[0]

        # Ссылка на игру
        if 'EpicGames' in text_about_game:
            link_part = 'https://store.epicgames.com/ru/p/'
            last_post_text = str(all_posts[0].select('[title]'))
            url_part = last_post_text.split(link_part)
            url_free_game_epic = url_part[1].split('">')
            bot.send_message(message.chat.id, f'<b>{text_about_game}</b>\n'
                                              f'{link_part}{url_free_game_epic[0]}', parse_mode= "html")
        else:
            url_part = all_text_about_game[1].split('Страница раздачи: ')
            url_free_game = url_part[1]
            bot.send_message(message.chat.id, f'<b>{text_about_game}</b>\n'
                                              f'{url_free_game}', parse_mode="html")

    except:
        bot.send_message(message.chat.id,'Не найдено')


if __name__ == '__main__':
    try:
        url_epic = 'https://vk.com/freesteam'
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

        request_epic = requests.get(url_epic, headers=HEADERS)
        soup_epic = BeautifulSoup(request_epic.text, 'html.parser')
        all_posts = soup_epic.find_all('div', class_='wall_post_text')

        # Заголовок с названием игры
        all_text_about_game = all_posts[0].text.split(' Как получить игру')
        text_about_game = all_text_about_game[0]

        if 'EpicGames' in text_about_game:
            link_part = 'https://store.epicgames.com/ru/p/'
            last_post_text = str(all_posts[0].select('[title]'))
            url_part = last_post_text.split(link_part)
            url_free_game_epic = url_part[1].split('">')
            print(f'{text_about_game}\n'
                  f'{link_part}{url_free_game_epic[0]}')
        else:
            url_part = all_text_about_game[1].split('Страница раздачи: ')
            url_free_game = url_part[1]
            print(f'{text_about_game}\n'
                  f'{url_free_game}')

    except:
        print('Не найдено')
