import unittest

import requests
from bs4 import BeautifulSoup

from src.constants import (
    PAGESIZE, PAGENUM, URL_PLATI, BANWORDS_IN_NAME, BANWORDS_IN_DESCRIPTION)
from src.functions import platimarket


class TestPlatimarket(unittest.TestCase):

    def setUp(self):
        self.game_name = 'cyberpunk 2077'
        self.fake_game_name = 'gvddrfvgdf'
        self.dict_price_url = {}
        self.url_plati = URL_PLATI.format(
            game_name=self.game_name,
            pagesize=PAGESIZE,
            pagenum=PAGENUM)
        self.response_plati = requests.get(self.url_plati)
        self.response_dict = self.response_plati.json()
        self.repo_dicts = self.response_dict['items']
        self.repo_dict = self.repo_dicts[1]  # проходящая по всем фильтрам игра, изменяется динамически

        self.full_name_in_site = self.repo_dict['name']
        self.name_in_site = self.full_name_in_site.lower()
        self.repo_url = self.repo_dict['url']
        self.repo_price = int(self.repo_dict['price_rur'])
        self.description = self.repo_dict['description'].lower()

        self.sold = self.repo_dict['numsold']
        self.returns = self.repo_dict['count_returns']
        self.positiveresponses = self.repo_dict['count_positiveresponses']
        self.negativeresponses = self.repo_dict['count_negativeresponses']

        self.response_site = requests.get(self.repo_url)

    def test_plati(self):
        platimarket.plati(self.game_name, self.dict_price_url)
        self.assertTrue(len(self.dict_price_url) > 0)

    def test_plati_fake_game_name(self):
        platimarket.plati(self.fake_game_name, self.dict_price_url)
        self.assertTrue(len(self.dict_price_url) == 0)

    def test_request_status_code(self):
        self.assertEqual(200, self.response_plati.status_code)

    def test_filters(self):
        self.assertFalse(self.game_name not in self.name_in_site)
        self.assertFalse(
            any(word in self.name_in_site for word in BANWORDS_IN_NAME))
        self.assertFalse(any(word_des in self.description for word_des in
                             BANWORDS_IN_DESCRIPTION))
        self.assertFalse('steam' not in self.name_in_site)
        self.assertFalse('steam' not in self.description)
        self.assertFalse(self.repo_dict['seller_rating'] < 100)
        self.assertFalse(self.sold < 30)
        self.assertFalse(self.returns > 5)
        self.assertFalse(self.returns / self.sold > 0.01)
        self.assertFalse(self.positiveresponses < 5)
        self.assertFalse(self.negativeresponses > 5)
        self.assertFalse(
            self.negativeresponses / self.positiveresponses > 0.01)

    def test_name(self):
        self.assertEqual(str, type(self.full_name_in_site))
        self.assertEqual(str, type(self.repo_url))
        self.assertEqual(int, type(self.repo_price))

    def test_check_response_site(self):
        self.assertEqual(200, self.response_site.status_code)

    def test_check_key_in_stock(self):
        soup_plati = BeautifulSoup(self.response_site.text, 'lxml')
        key_in_site = soup_plati.find(
            'div', class_='goods_order_form_subscribe')
        self.assertIsNone(key_in_site)


if __name__ == '__main__':
    unittest.main()
