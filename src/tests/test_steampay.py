import unittest

import requests
from bs4 import BeautifulSoup

from src.constants import URL_STEAMPAY
from src.functions import steampay


class TestSteampay(unittest.TestCase):

    def setUp(self):
        self.game_name = 'superliminal'
        self.fake_game_name = 'asvddrfvgdf'
        self.dict_price_url = {}
        self.game_name_link = '-'.join(list(self.game_name.split(' ')))
        self.url_steampay = URL_STEAMPAY.format(
            game_name_link=self.game_name_link)
        self.response_steampay = requests.get(self.url_steampay)
        self.soup_steampay = BeautifulSoup(
            self.response_steampay.text, 'lxml')
        self.key_in_stock = self.soup_steampay.find(
            'span', class_='product__advantages-orange')
        self.stock = str(self.key_in_stock)
        self.region = self.soup_steampay.find_all(
            'ul', class_='product__info-inner-block-list')
        self.sell_region = str(self.region[3])

    def test_steam_pay(self):
        steampay.steam_pay(self.game_name, self.dict_price_url)
        self.assertTrue(len(self.dict_price_url) > 0)

    def test_steampay_fake_game_name(self):
        steampay.steam_pay(self.fake_game_name, self.dict_price_url)
        self.assertTrue(len(self.dict_price_url) == 0)

    def test_request_status_code(self):
        self.assertEqual(200, self.response_steampay.status_code)

    def test_check_key_in_stock(self):
        self.assertFalse('закончился' in self.stock)
        self.assertFalse('ожидается' in self.stock)

    def test_check_region(self):
        self.assertFalse('Россия' not in self.sell_region)
