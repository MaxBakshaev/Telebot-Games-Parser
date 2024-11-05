import unittest

import requests
from bs4 import BeautifulSoup

from src.constants import HEADERS, URL_EXPECTED
from src.functions import expected


class TestExpected(unittest.TestCase):

    def setUp(self):
        self.request_expected = requests.get(URL_EXPECTED, headers=HEADERS)
        self.soup_expected = BeautifulSoup(
            self.request_expected.text, 'lxml')

        self.all_posts = (
            self.soup_expected.find_all('div', class_='game_search_par'))
        self.soup_expected.find_all('div', class_='game_search_par')

        self.post = self.all_posts[0]
        self.title = expected.get_title(self.post)
        self.release_date = expected.get_release_date(self.post)
        self.short_description = expected.get_short_description(self.post)
        self.image_url = expected.get_image_small(self.post)
        self.link_url = expected.get_link_url(self.post)

        self.request_expect = requests.get(self.link_url, headers=HEADERS)
        self.soup_expect = BeautifulSoup(
            self.request_expect.text, 'lxml')

        self.full_description = expected.get_full_description(
            self.soup_expect, self.short_description)
        self.big_img_url = expected.get_big_image_url(
            self.soup_expect, self.image_url)
        self.youtube_urls = expected.get_youtube_urls(self.soup_expect)
        self.system_text = expected.get_system_text(self.soup_expect)

    def test_request_status_code(self):
        self.assertEqual(200, self.request_expected.status_code)

    def test_type_parameters(self):
        self.assertEqual(str, type(self.title))
        self.assertEqual(str, type(self.release_date))
        self.assertEqual(str, type(self.short_description))
        self.assertEqual(str, type(self.image_url))
        self.assertEqual(str, type(self.link_url))

    def test_request_post(self):
        link_url = expected.get_link_url(self.post)
        request_expect = requests.get(link_url, headers=HEADERS)
        self.assertEqual(200, request_expect.status_code)

    def test_full_parameters(self):
        self.assertEqual(str, type(self.full_description))
        self.assertEqual(str, type(self.big_img_url))
        self.assertEqual(str, type(self.youtube_urls))
        self.assertEqual(str, type(self.system_text))


if __name__ == '__main__':
    unittest.main()
