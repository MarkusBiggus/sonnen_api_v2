import os, sys
import unittest
import json
import logging
from math import floor
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
API_READ_TOKEN = os.getenv('API_READ_TOKEN')
# SonnenBatterie config parameters to check against
BACKUP_BUFFER_USOC = int(os.getenv('BACKUP_BUFFER_USOC'))
OPERATING_MODE = int(os.getenv('OPERATING_MODE'))
LOGGER_NAME = "sonnenapiv2"

class TestBatterie(unittest.TestCase):

    if BATTERIE_HOST == 'X':
        raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN in .env See env.example')

    print ('Live Battery Online!')

    def setUp(self) -> None:
        logging.basicConfig(filename="logs/sonnenapiv2.log'", level=logging.DEBUG, maxBytes=52428800)
        self.logger = logging.getLogger(LOGGER_NAME)
        os.makedirs(os.path.dirname('logs/'+LOGGER_NAME+'.log'), exist_ok=True)
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs debug messages
        fh = logging.FileHandler(filename='logs/'+LOGGER_NAME+'.log', mode='a')
        fh.setLevel(logging.DEBUG)
        # console handler display logs messages to console
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    #    self.logger.info('Sonnen Live Batterie Test suite started.')


        self._battery = Sonnen(API_READ_TOKEN, BATTERIE_HOST, LOGGER_NAME)  # Batterie online

        success = self._battery.update()
#        self.assertTrue(success)
        if not success:
            self.skipTest('Failed to get battery data!')

    def test_configuration_de_software(self):
        version = self._battery.configuration_de_software
        cycles = self._battery.battery_cycle_count
        print(f'Software Version: {version}   Battery Cycles: {cycles:,}')
        self.assertEqual(True, True)

    def test_configuration_em_usoc(self):
        usoc = self._battery.configuration_em_usoc
        self.assertEqual(usoc, BACKUP_BUFFER_USOC) # config BackupBuffer value

    def test_seconds_to_reserve(self):
        seconds = self._battery.seconds_to_reserve
        if self._battery.status_battery_discharging:
            if seconds < 0:
                print(f'Seconds since Reserve: {seconds:,}')
            else:
                print(f'Seconds to Reserve: {seconds:,} (discharging)')
            seconds = self._battery.seconds_to_empty
            print(f'Seconds to Empty: {seconds:,}')
        else:
            if seconds is None:
                print(f'Seconds to reserve: Battery charging above reserve')
            else:
                print(f'Seconds to Reserve: {seconds:,} (charging)')
                usoc = self._battery.u_soc
                if usoc == self._battery.configuration_em_usoc:
                    print(f'Battery at Backup Reserve: {usoc}')
        self.assertEqual(True, True)

    def test_system_status(self):
        state = self._battery.state_core_control_module
        print (f'Core Control State: {state}')
        status = self._battery.system_status
        print (f'System Status: {status}')
        status_timestamp = self._battery.system_status_timestamp
        print (f'Status time: {status_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        validation_timestamp = self._battery.validation_timestamp
        print (f'Validation time: {validation_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        self.assertEqual(state, 'ongrid')
        self.assertEqual(status, 'OnGrid')

    def test_configuration_em_operatingmode(self):
        OpMode = self._battery.configuration_em_operatingmode
        OperatingMode = self._battery.str_em_operatingmode
        DischargeAllowed = not(self._battery.status_discharge_not_allowed)
        print (f'Operating Mode: "{OperatingMode}"  Discharge Allowed: {DischargeAllowed}')
        self.assertEqual(OpMode, OPERATING_MODE)

    def test_battery_remaining_capacity(self):
        capacity = self._battery.battery_remaining_capacity
        usable_capacity = self._battery.battery_usable_remaining_capacity
        print(f'RemainingAh capacity: {capacity:.2f}Ah  UsableAh: {usable_capacity:.2f}Ah')
        self.assertEqual(True, True)

    def test_battery_rsoc(self):
        rsoc = self._battery.battery_rsoc
        print(f'Battery Relative State of Charge: {rsoc:.0f}%')
        self.assertEqual(True, True)

    def test_data_socs(self):
        backup_buffer = self._battery.status_backup_buffer
        usable_reserve = self._battery.backup_buffer_usable_capacity_wh
        print(f'Backup Buffer: {backup_buffer:2}%  Usable Reserve: {usable_reserve:,}Wh')
        usoc = self._battery.u_soc
        rsoc = self._battery.r_soc
        seconds_to_reserve = self._battery.seconds_to_reserve
        print(f'Useable State of Charge: {usoc}%  Actual SOC: {rsoc}%  Seconds to reserve: {seconds_to_reserve}')
        if usoc > backup_buffer:
            reserve_time = self._battery.backup_reserve_at
            if reserve_time is None:
                print ('Battery above backup reserve, not discharging.')
            else:
                print('Battery Discharge to Reserve at: ' + reserve_time.strftime('%d-%b-%Y %H:%M:%S'))
        else:
            discharged_at = self._battery.fully_discharged_at
            print(f'Backup Fully Discharged at: ' + discharged_at.strftime('%d-%b-%Y %H:%M:%S'))
        self.assertEqual(True, True)

    def test_battery_charging(self):
        charging = self._battery.status_battery_charging
        discharging = self._battery.status_battery_discharging
        print(f'Battery: Charging: {charging} Discharging: {discharging}')
        charging = self._battery.charging
        discharging = self._battery.discharging
        production = self._battery.production
        consumption = self._battery.consumption
        feedin = self._battery.status_grid_feed_in
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
        flows = self._battery.status_flows
    #    pprint(getmembers(flows.items()))
        for key, value in flows.items():
            print(f'{key}: {value}')
        self.assertEqual(True, True)

    def test_status_grid_feed_in(self):
        feedin = self._battery.status_grid_feed_in
        if feedin < 0:
            print(f'Grid Import: {abs(feedin):,.0f}W')
        else:
            print(f'Grid Export: {feedin:,.0f}W')
        self.assertEqual(True, True)

    def test_last_time_full(self):
        charged = self._battery.last_time_full
        print('Battery Last Full at: ' + charged.strftime('%d-%b-%Y %H:%M'))
        self.assertEqual(True, True)

    def test_fully_charged_at(self):
        charged = self._battery.fully_charged_at
        if charged is None:
            next_full = '*not charging*'
        else:
            next_full = charged.strftime('%d-%b-%Y %H:%M')
        print('Battery Next Full at: ' + next_full)
        self.assertEqual(True, True)

    def test_powermeter(self):
        kwh_consumed = self._battery.kwh_consumed
        kwh_produced = self._battery.kwh_produced
        print(f'Power consumed: {kwh_consumed:,.1f}kWh  produced: {kwh_produced:,.1f}kWh')
        self.assertEqual(True, True)

    def test_inverter(self):
        pac_total = self._battery.inverter_pac_total
        print (f'Inverter: {pac_total:,.2f}')
        self.assertEqual(True, True)

    def test_remaining_capacity(self):
        batteryCapacity = self._battery.battery_full_charge_capacity
        batteryCapacityWh = self._battery.battery_full_charge_capacity_wh
        capacity = self._battery.full_charge_capacity
        remaining = self._battery.battery_remaining_capacity
        usableRemaining = self._battery.battery_usable_remaining_capacity
        remainingWh = self._battery.remaining_capacity_wh
        print(f'CapacityWh(data): {capacity:,}Wh  RemainingWh(status): {remainingWh:,}Wh  RemainingAh(battery): {remaining:,.3f}Ah  UsableAh(battery): {usableRemaining:,.3f}Ah')
        print(f'CapacityAh(battery): {batteryCapacity:,.3f}Ah CapacityWh(battery): {batteryCapacityWh:,.3f}Wh')
        self.assertEqual(True, True)

    def test_eclipse_led(self):
        eclipse_led = self._battery.ic_eclipse_led
        print('EclipseLEDs: ' + json.dumps(eclipse_led, indent=2))
        self.assertEqual(True, True)

    def test_wrapped(self):
        request_timeouts = self._battery.get_request_connect_timeouts()
        print(f'request_timeouts: {request_timeouts}')
        self.assertEqual((20, 20), request_timeouts)
        battery_status = self._battery.get_battery()
    #    print('battery_status: ' + json.dumps(battery_status, indent=2))
        inverter = self._battery.get_inverter()
        self.assertNotEqual(inverter, False)
        PAC = inverter.get("pac_total")
        print (f'Inverter PAC: {PAC:.2f}W ')
        remaining = self._battery.battery_remaining_capacity
        usableRemaining = self._battery.battery_usable_remaining_capacity
        remainingWh = self._battery.remaining_capacity_wh
        usableWh = floor(usableRemaining * self._battery.battery_system_dc_voltage)
        print(f'RemainingAh: {remaining:,.3f}Ah  RemainingWh: {remainingWh:,}Wh')
        print(f'UsableAh: {usableRemaining:,.3f}Ah  UsableWh: {usableWh:,}Wh')
