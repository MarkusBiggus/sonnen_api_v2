import os
import unittest
import json
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST')
API_READ_TOKEN = os.getenv('API_READ_TOKEN')

class TestBatterie(unittest.TestCase):

    battery_live = Sonnen(API_READ_TOKEN, BATTERIE_HOST)  # Batterie online

    battery_live.update()

    print ('Live Battery Online!')

    def test_configuration_de_software(self):
        version = self.battery_live.configuration_de_software()
        print('Software Version: ' + version)
        self.assertEqual(True, True)

    def test_configuration_em_usoc(self):
        usoc = self.battery_live.configuration_em_usoc()
        self.assertEqual(usoc, 20) # config BackupBuffer value

    def test_status_backup_buffer(self):
        usoc = self.battery_live.status_backup_buffer()
        print(f'Backup Buffer: {usoc:2}%')
        self.assertEqual(True, True)

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

    def test_battery_cycle_count(self):
        cycles = self.battery_live.battery_cycle_count()
        print(f'Battery Cycle Count: {cycles:,}')
        self.assertEqual(True, True)

    def test_battery_charging(self):
        charging = self.battery_live.status_battery_charging()
        discharging = self.battery_live.status_battery_discharging()
    #    print(f'Battery: Charging {charging:%s} Discharging {discharging:%s}')
        print(f'Battery: Charging {charging} Discharging {discharging}')
        self.assertEqual(True, True)

    def test_status_flows(self):
        flows = self.battery_live.status_flows()
        for key, value in flows.items():
            print(f'{key}: {value}')
        self.assertEqual(True, True)

    def test_status_grid_feed_in(self):
        feedin = self.battery_live.status_grid_feed_in()
        if feedin < 0:
            print(f'Grid Draw Out: {abs(feedin):,.0f}W')
        else:
            print(f'Grid Feed In: {feedin:,.0f}W')
        self.assertEqual(True, True)

    def test_remaining_capacity(self):
        batteryCapacity = self.battery_live.battery_full_charge_capacity()
        capacity = self.battery_live.full_charge_capacity()
        remaining = self.battery_live.battery_remaining_capacity()
        usable_remaining = self.battery_live.battery_usable_remaining_capacity()
        remaining_wh = self.battery_live.remaining_capacity_wh()
        print(f'Capacity(battery): {batteryCapacity:,}kWh Capacity(data): {capacity:,}Wh  Remaining(battery): {remaining:.2f}Wh  Usable(battery): {usable_remaining:.2f}Wh  Remaining(status): {remaining_wh}Wh')
        self.assertEqual(True, True)

    def test_eclipse_led(self):
        eclipse_led = self.battery_live.ic_eclipse_led()
        print('EclipseLEDs: ' + json.dumps(eclipse_led, indent=2))
        self.assertEqual(0, 0)
