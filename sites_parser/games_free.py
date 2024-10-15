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
        last_post_text = str(all_posts[0].select('[title]'))
        url_part = last_post_text.split('https://store.epicgames.com/ru/p/')
        url_free_game_epic = url_part[1].split('">')

        bot.send_message(message.chat.id , f'https://store.epicgames.com/ru/p/{url_free_game_epic[0]}\n'
                                           f'<b>{text_about_game}</b>', parse_mode= "html")
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

        # Ссылка на игру
        last_post_text = str(all_posts[0].select('[title]'))
        url_part = last_post_text.split('https://store.epicgames.com/ru/p/')
        url_free_game_epic = url_part[1].split('">')

        print(f'{text_about_game}\n'
              f'https://store.epicgames.com/ru/p/{url_free_game_epic[0]}')
    except:
        print('Не найдено')
