import unittest

from sonnen_api_v2 import Sonnen


class TestSonnen(unittest.TestCase):

    def setUp(self) -> None:
        self.batterie1 = Sonnen('', '192.168.1.12')

        self.batterie2 = Sonnen('xyZio', '192.168.2.50')
        self.batterie2._status_data[Sonnen.CONSUMPTION_AVG_KEY] = '2000'
        self.batterie2._ic_status[Sonnen.MODULES_INSTALLED_KEY] = '5'
        self.batterie2._latest_details_data[Sonnen.PAC_KEY] = '2005'
        self.batterie2._status_data[Sonnen.GRID_FEED_IN_WATT_KEY] = '456'

    def test_fetch_latest_details(self):
        expected1 = False
        self.assertEqual(self.batterie1.fetch_latest_details(), expected1)

    def test_fetch_status(self):
        expected1 = False
        self.assertEqual(self.batterie1.fetch_status(), expected1)

    def test_consumption_average(self):
        expected1 = 0
        expected2 = 2000
        self.assertEqual(self.batterie1.consumption_average(self.batterie1.CONSUMPTION_AVG_KEY), expected1)
        self.assertEqual(self.batterie2.consumption_average(self.batterie2.CONSUMPTION_AVG_KEY), expected2)

    def test_installed_modules(self):
        expected1 = 0
        expected2 = 5
        self.assertEqual(self.batterie1.installed_modules, expected1)
        self.assertEqual(self.batterie2.installed_modules, expected2)

    def test_discharging(self):
        expected1 = 0
        expected2 = 2005
        self.assertEqual(self.batterie1.discharging, expected1)
        self.assertEqual(self.batterie2.discharging, expected2)

    def test_charging(self):
        expected1 = 0
        expected2 = 205
        self.batterie2._latest_details_data[Sonnen.PAC_KEY] = '-205'
        self.assertEqual(self.batterie1.charging, expected1)
        self.assertEqual(self.batterie2.charging, expected2)

    def test_grid_in(self):
        expected1 = 0
        expected2 = 456
        self.assertEqual(self.batterie1.grid_in, expected1)
        self.assertEqual(self.batterie2.grid_in, expected2)

    def test_grid_out(self):
        expected1 = 0
        expected2 = 512
        self.batterie2._status_data[Sonnen.GRID_FEED_IN_WATT_KEY] = '-512'
        self.assertEqual(self.batterie1.grid_out, expected1)
        self.assertEqual(self.batterie2.grid_out, expected2)