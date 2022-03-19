import unittest

from sonnen_api_v2 import Sonnen


class TestSonnen(unittest.TestCase):

    result1 = Sonnen('', '192.168.1.12')

    def test_fetch_latest_details(self):
        expected1 = False
        self.assertEqual(self.result1.fetch_latest_details(), expected1)

    def test_fetch_status(self):
        expected1 = False
        self.assertEqual(self.result1.fetch_status(), expected1)

    def test_consumption_average(self):
        expected1 = 0
        self.assertEqual(self.result1.consumption_average, expected1)