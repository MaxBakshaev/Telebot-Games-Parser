import unittest

from src.constants import BAN_SYMBOLS


class TestMain(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_bad_symbols(self):
        message_amount_games = '5'
        self.assertFalse(set(message_amount_games) & BAN_SYMBOLS)

    def test_check_bad_symbols_True(self):
        message_amount_games = ('\*_>"(')
        self.assertTrue(set(message_amount_games) & BAN_SYMBOLS)
