import os
import unittest
import json
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_1_HOST')
API_READ_TOKEN = os.getenv('API_READ_TOKEN_1')
BACKUP_BUFFER_USOC = int(os.getenv('BACKUP_BUFFER_USOC'))
OPERATING_MODE = int(os.getenv('OPERATING_MODE'))

class TestBatterie(unittest.TestCase):

    battery_live = Sonnen(API_READ_TOKEN, BATTERIE_HOST)  # Batterie online

    battery_live.update()

    print ('Live Battery Online!')

    def test_configuration_de_software(self):
        version = self.battery_live.configuration_de_software()
        cycles = self.battery_live.battery_cycle_count()
        print(f'Software Version: {version}   Battery Cycles: {cycles:,}')
        self.assertEqual(True, True)

    def test_configuration_em_usoc(self):
        usoc = self.battery_live.configuration_em_usoc()
        self.assertEqual(usoc, BACKUP_BUFFER_USOC) # config BackupBuffer value

    def test_seconds_to_empty(self):
        if self.battery_live.status_battery_discharging():
            seconds = self.battery_live.seconds_to_reserve()
            if seconds < 0:
                print(f'Seconds since Reserve: {seconds:,}')
            else:
                print(f'Seconds to Reserve: {seconds:,}')
            seconds = self.battery_live.seconds_to_empty()
            print(f'Seconds to Empty: {seconds:,}')
        else:
            usoc = self.battery_live.u_soc()
            if usoc == self.battery_live.configuration_em_usoc():
                print(f'Battery at Backup Reserve: {usoc}')
        self.assertEqual(True, True)

    def test_state_core_control_module(self):
        state = self.battery_live.state_core_control_module()
        print ('Current Control State: ' + state)
        self.assertEqual(state, 'ongrid')

    def test_configuration_em_operatingmode(self):
        OpMode = self.battery_live.configuration_em_operatingmode()
        self.assertEqual(OpMode, OPERATING_MODE) # config Operating Mode: 2 = Automatic - Self Consumption

    def test_battery_remaining_capacity(self):
        capacity = self.battery_live.battery_remaining_capacity()
        usable_capacity = self.battery_live.battery_usable_remaining_capacity()
        print(f'Remaining capacity: {capacity:.2f}Ah  Usable: {usable_capacity:.2f}Ah')
        self.assertEqual(True, True)

    def test_battery_rsoc(self):
        rsoc = self.battery_live.battery_rsoc()
        print(f'Battery Relative State of Charge: {rsoc:.0f}%')
        self.assertEqual(True, True)

    def test_data_socs(self):
        backup_buffer = self.battery_live.status_backup_buffer()
        print(f'Backup Buffer: {backup_buffer:2}%')
        usoc = self.battery_live.u_soc()
        rsoc = self.battery_live.u_roc()
        print(f'Useable State of Charge: {usoc}%  Actual SOC: {rsoc}%')
        if usoc > backup_buffer:
            reserve_time = self.battery_live.backup_reserve_at()
            if reserve_time == 0:
                print ('Battery above backup reserve, not discharging.')
            else:
                print('Battery Discharge to Reserve at: ' + reserve_time.strftime('%d-%b-%Y %H:%M'))
        else:
            discharged_at = self.battery_live.fully_discharged_at()
            print(f'Backup Fully Discharged at: ' + discharged_at.strftime('%d-%b-%Y %H:%M'))
        usable_reserve = self.battery_live.backup_buffer_usable_capacity_wh()
        print(f'Backup Usable Reserve: {usable_reserve:,}Wh')
        self.assertEqual(True, True)

    def test_battery_charging(self):
        charging = self.battery_live.status_battery_charging()
        discharging = self.battery_live.status_battery_discharging()
        print(f'Battery: Charging: {charging} Discharging: {discharging}')
        charging = self.battery_live.charging()
        discharging = self.battery_live.discharging()
        production = self.battery_live.production()
        consumption = self.battery_live.consumption()
        feedin = self.battery_live.status_grid_feed_in()
        if charging != 0:
            print(f'Battery Charging: {charging:,}W  Production: {production:,}W  Consumption: {consumption:,}W  Grid Export: {feedin:,}W ')
        else:
            flow = 'import' if feedin > 0 else 'export'
            if discharging != 0:
                print(f'Battery Discharging: {discharging:,}W  Production: {production:,}W  Consumption: {consumption:,}W')
            else:
                print(f'Battery Idle. Grid {flow}: {abs(feedin):,}W  Production: {production:,}W  Consumption: {consumption:,}W')
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

    def test_last_time_full(self):
        charged = self.battery_live.last_time_full()
        print('Battery Last Full at: ' + charged.strftime('%d-%b-%Y %H:%M'))
        self.assertEqual(True, True)

    def test_fully_charged_at(self):
        charged = self.battery_live.fully_charged_at()
        if charged != 0:
            next_full = charged.strftime('%d-%b-%Y %H:%M')
        else:
            next_full = '*not charging*'
        print('Battery Next Full at: ' + next_full)
        self.assertEqual(True, True)

    def test_powermeter(self):
        kwh_consumed = self.battery_live.kwh_consumed()
        kwh_produced = self.battery_live.kwh_produced()
        print(f'Power consumed: {kwh_consumed:,.1f}kWh  produced: {kwh_produced:,.1f}kWh')
        self.assertEqual(True, True)

    def test_remaining_capacity(self):
        batteryCapacity = self.battery_live.battery_full_charge_capacity()
        batteryCapacityWh = self.battery_live.battery_full_charge_capacity_wh()
        capacity = self.battery_live.full_charge_capacity()
        remaining = self.battery_live.battery_remaining_capacity()
        usableRemaining = self.battery_live.battery_usable_remaining_capacity()
        remainingWh = self.battery_live.remaining_capacity_wh()
        print(f'Capacity(data): {capacity:,}Wh  Remaining(battery): {remaining:,.3f}Ah  Usable(battery): {usableRemaining:,.3f}Ah  Remaining(status): {remainingWh:,}Wh')
        print(f'Capacity(battery): {batteryCapacity:,.3f}Ah Capacity(battery): {batteryCapacityWh:,.3f}Wh')
        self.assertEqual(True, True)

    def test_eclipse_led(self):
        eclipse_led = self.battery_live.ic_eclipse_led()
        print('EclipseLEDs: ' + json.dumps(eclipse_led, indent=2))
        self.assertEqual(0, 0)
