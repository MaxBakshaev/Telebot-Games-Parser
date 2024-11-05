import unittest

import requests
from bs4 import BeautifulSoup

from src.constants import HEADERS, URL_GAMES_FREE

from src.functions import games_free


class TestGamesFree(unittest.TestCase):

    def setUp(self):
        self.request_games = requests.get(URL_GAMES_FREE, headers=HEADERS)
        self.soup_games = BeautifulSoup(
            self.request_games.text, 'lxml')
        self.all_posts = self.soup_games.find_all(
            'div', class_='col-lg-4 col-md-4 three-columns post-box')

    def test_request_status_code(self):
        self.assertEqual(200, self.request_games.status_code)

    def test_post_info_type(self):
        for post in self.all_posts:
            post_info = games_free.post_get_post_info(post)
            self.assertEqual(list, type(post_info))


if __name__ == '__main__':
    unittest.main()
