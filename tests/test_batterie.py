import datetime
import os
import unittest
import json
import logging
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST')
API_READ_TOKEN = os.getenv('API_READ_TOKEN')

class TestBatterie(unittest.TestCase):

    battery_live = Sonnen(API_READ_TOKEN, BATTERIE_HOST)  # Batterie online

    battery_live.update()
    battery_live.fetch_configurations()
    print ('Live Battery Online!')

    def test_configuration_de_software(self):
        version = self.battery_live.configuration_de_software()
        print('Software Version: ' + version)
        self.assertEqual(True, True)

    def test_configuration_em_usoc(self):
        usoc = self.battery_live.configuration_em_usoc()
        self.assertEqual(usoc, 20) # config BackupBuffer value

    def test_state_core_control_module(self):
        state = self.battery_live.state_core_control_module()
        print ('Current Control State: ' + state)
        self.assertEqual(state, 'ongrid')

    def test_configuration_em_operatingmode(self):
        OpMode = self.battery_live.configuration_em_operatingmode()
        self.assertEqual(OpMode, 2) # config Operating Mode: Automatic - Self Consumption

    def test_battery_remaining_capacity(self):
        capacity = self.battery_live.battery_remaining_capacity()
        print(f'Remaining capacity: {capacity:.2f}Ah')
        self.assertEqual(True, True)

    def test_battery_rsoc(self):
        rsoc = self.battery_live.battery_rsoc()
        print(f'Relative State of Charge: {rsoc:.2f}%')
        self.assertEqual(True, True)

    def test_eclipse_led(self):
        eclipse_led = self.battery_live.ic_eclipse_led()
        print('EclipseLEDs: ' + json.dumps(eclipse_led, indent=2))
        self.assertEqual(0, 0)
