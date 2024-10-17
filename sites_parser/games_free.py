import requests
from bs4 import BeautifulSoup

def free_games(bot, message):
    try:
        url_games = 'https://freesteam.ru/category/active/'
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

        request_games = requests.get(url_games, headers=HEADERS)
        soup_games = BeautifulSoup(request_games.text, 'lxml')
        all_posts = soup_games.find_all('div', class_='col-lg-4 col-md-4 three-columns post-box')

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
                bot.send_message(message.chat.id, f'<b>{post_info[0]}:</b>\n'
                                                  f'{post_link}', parse_mode= "html")

    except:
        bot.send_message(message.chat.id,'Не найдено')


if __name__ == '__main__':
    try:
        url_games = 'https://freesteam.ru/category/active/'
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

        request_games = requests.get(url_games, headers=HEADERS)
        soup_games = BeautifulSoup(request_games.text, 'lxml')
        all_posts = soup_games.find_all('div', class_='col-lg-4 col-md-4 three-columns post-box')

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

    except:
        print('Не найдено')
