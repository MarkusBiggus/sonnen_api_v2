import datetime
import os
import unittest
import responses
import logging
from freezegun import freeze_time
from sonnen_api_v2 import Sonnen


class TestSonnen(unittest.TestCase):

    @responses.activate
    def setUp(self) -> None:
        test_data_latest_charging = {
            'Consumption_W': 403,
            'FullChargeCapacity': 19531,
            'GridFeedIn_W': 0,
            'Pac_total_W': -94,
            'Production_W': 578,
            'RSOC': 98,
            'SetPoint_W': -145,
            'Timestamp': '2022-04-30 17:00:58',
            'USOC': 98,
            'UTC_Offet': 2,
            'ic_status': {
                'DC Shutdown Reason': {
                    'Critical BMS Alarm': False,
                    'Electrolyte Leakage': False,
                    'Error condition in BMS initialization': False,
                    'HW_Shutdown': False,
                    'HardWire Over Voltage': False,
                    'HardWired Dry Signal A': False,
                    'HardWired Under Voltage': False,
                    'Holding Circuit Error': False,
                    'Initialization Timeout': False,
                    'Initialization of AC contactor failed': False,
                    'Initialization of BMS hardware failed': False,
                    'Initialization of DC contactor failed': False,
                    'Initialization of Inverter failed': False,
                    'Invalid or no SystemType was set': False,
                    'Inverter Over Temperature': False,
                    'Inverter Under Voltage': False,
                    'Inverter Version Too Low For Dc-Module': False,
                    'Manual shutdown by user': False,
                    'Minimum rSOC of System reached': False,
                    'Modules voltage out of range': False,
                    'No Setpoint received by HC': False,
                    'Odd number of battery modules': False,
                    'One single module detected and module voltage is out of range': False,
                    'Only one single module detected': False,
                    'Shutdown Timer started': False,
                    'System Validation failed': False,
                    'Voltage Monitor Changed': False
                },
                'Eclipse Led': {
                    'Blinking Red': False,
                    'Pulsing Green': False,
                    'Pulsing Orange': False,
                    'Pulsing White': True,
                    'Solid Red': False
                },
                'MISC Status Bits': {
                    'Discharge not allowed': False,
                    'F1 open': False,
                    'Min System SOC': False,
                    'Min User SOC': False,
                    'Setpoint Timeout': False
                },
                'Microgrid Status': {
                    'Continious Power Violation': False,
                    'Discharge Current Limit Violation': False,
                    'Low Temperature': False,
                    'Max System SOC': False,
                    'Max User SOC': False,
                    'Microgrid Enabled': False,
                    'Min System SOC': False,
                    'Min User SOC': False,
                    'Over Charge Current': False,
                    'Over Discharge Current': False,
                    'Peak Power Violation': False,
                    'Protect is activated': False,
                    'Transition to Ongrid Pending': False
                },
                'Setpoint Priority': {
                    'BMS': False,
                    'Energy Manager': True,
                    'Full Charge Request': False,
                    'Inverter': False,
                    'Min User SOC': False,
                    'Trickle Charge': False
                },
                'System Validation': {
                    'Country Code Set status flag 1': False,
                    'Country Code Set status flag 2': False,
                    'Self test Error DC Wiring': False,
                    'Self test Postponed': False,
                    'Self test Precondition not met': False,
                    'Self test Running': False,
                    'Self test successful finished': False
                },
                'nrbatterymodules': 4,
                'secondssincefullcharge': 3720,
                'statebms': 'ready',
                'statecorecontrolmodule': 'ongrid',
                'stateinverter': 'running',
                'timestamp': 'Sat Apr 30 17:00:57 2022'
            }
        }

        test_data_status_discharging = {
            'Apparent_output': 438,
            'BackupBuffer': '0',
            'BatteryCharging': False,
            'BatteryDischarging': True,
            'Consumption_Avg': 563,
            'Consumption_W': 541,
            'Fac': 50.0167121887207,
            'FlowConsumptionBattery': True,
            'FlowConsumptionGrid': False,
            'FlowConsumptionProduction': True,
            'FlowGridBattery': False,
            'FlowProductionBattery': False,
            'FlowProductionGrid': False,
            'GridFeedIn_W': -20,
            'IsSystemInstalled': 1,
            'OperatingMode': '2',
            'Pac_total_W': 438,
            'Production_W': 102,
            'RSOC': 99,
            'RemainingCapacity_Wh': 41027,
            'Sac1': 438,
            'Sac2': None,
            'Sac3': None,
            'SystemStatus': 'OnGrid',
            'Timestamp': '2022-05-06 20:24:39',
            'USOC': 99,
            'Uac': 237,
            'Ubat': 211,
            'dischargeNotAllowed': False,
            'generator_autostart': False
        }

        test_data_latest_discharging = {
            'Consumption_W': 541,
            'FullChargeCapacity': 19531,
            'GridFeedIn_W': 0,
            'Pac_total_W': 439,
            'Production_W': 102,
            'RSOC': 99,
            'SetPoint_W': 439,
            'Timestamp': '2022-05-06 20:24:38',
            'USOC': 99,
            'UTC_Offet': 2,
            'ic_status': {
                'DC Shutdown Reason': {
                    'Critical BMS Alarm': False,
                    'Electrolyte Leakage': False,
                    'Error condition in BMS initialization': False,
                    'HW_Shutdown': False,
                    'HardWire Over Voltage': False,
                    'HardWired Dry Signal A': False,
                    'HardWired Under Voltage': False,
                    'Holding Circuit Error': False,
                    'Initialization Timeout': False,
                    'Initialization of AC contactor failed': False,
                    'Initialization of BMS hardware failed': False,
                    'Initialization of DC contactor failed': False,
                    'Initialization of Inverter failed': False,
                    'Invalid or no SystemType was set': False,
                    'Inverter Over Temperature': False,
                    'Inverter Under Voltage': False,
                    'Inverter Version Too Low For Dc-Module': False,
                    'Manual shutdown by user': False,
                    'Minimum rSOC of System reached': False,
                    'Modules voltage out of range': False,
                    'No Setpoint received by HC': False,
                    'Odd number of battery modules': False,
                    'One single module detected and module voltage is out of range': False,
                    'Only one single module detected': False,
                    'Shutdown Timer started': False,
                    'System Validation failed': False,
                    'Voltage Monitor Changed': False
                },
                'Eclipse Led': {
                    'Blinking Red': False,
                    'Pulsing Green': False,
                    'Pulsing Orange': False,
                    'Pulsing White': True,
                    'Solid Red': False
                },
                'MISC Status Bits': {
                    'Discharge not allowed': False,
                    'F1 open': False,
                    'Min System SOC': False,
                    'Min User SOC': False,
                    'Setpoint Timeout': False
                },
                'Microgrid Status': {
                    'Continious Power Violation': False,
                    'Discharge Current Limit Violation': False,
                    'Low Temperature': False,
                    'Max System SOC': False,
                    'Max User SOC': False,
                    'Microgrid Enabled': False,
                    'Min System SOC': False,
                    'Min User SOC': False,
                    'Over Charge Current': False,
                    'Over Discharge Current': False,
                    'Peak Power Violation': False,
                    'Protect is activated': False,
                    'Transition to Ongrid Pending': False
                },
                'Setpoint Priority': {
                    'BMS': False,
                    'Energy Manager': True,
                    'Full Charge Request': False,
                    'Inverter': False,
                    'Min User SOC': False,
                    'Trickle Charge': False
                },
                'System Validation': {
                    'Country Code Set status flag 1': False,
                    'Country Code Set status flag 2': False,
                    'Self test Error DC Wiring': False,
                    'Self test Postponed': False,
                    'Self test Precondition not met': False,
                    'Self test Running': False,
                    'Self test successful finished': False
                },
                'nrbatterymodules': 4,
                'secondssincefullcharge': 574,
                'statebms': 'ready',
                'statecorecontrolmodule': 'ongrid',
                'stateinverter': 'running',
                'timestamp': 'Fri May 6 20:24:36 2022'
            }
        }

        test_data_status_charging = {
            'Apparent_output': 98,
            'BackupBuffer': '0',
            'BatteryCharging': True,
            'BatteryDischarging': False,
            'Consumption_Avg': 486,
            'Consumption_W': 403,
            'Fac': 50.05781555175781,
            'FlowConsumptionBattery': False,
            'FlowConsumptionGrid': False,
            'FlowConsumptionProduction': True,
            'FlowGridBattery': False,
            'FlowProductionBattery': True,
            'FlowProductionGrid': True,
            'GridFeedIn_W': 54,
            'IsSystemInstalled': 1,
            'OperatingMode': '2',
            'Pac_total_W': -95,
            'Production_W': 578,
            'RSOC': 98,
            'RemainingCapacity_Wh': 40781,
            'Sac1': 98,
            'Sac2': None,
            'Sac3': None,
            'SystemStatus': 'OnGrid',
            'Timestamp': '2022-04-30 17:00:58',
            'USOC': 98,
            'Uac': 245,
            'Ubat': 212,
            'dischargeNotAllowed': False,
            'generator_autostart': False
        }

        test_data_powermeter = [
            {
                'a_l1': 2.4730000495910645, 'a_l2': 0,
                'a_l3': 0,
                'channel': 1,
                'deviceid': 4,
                'direction': 'production',
                'error': 0,
                'kwh_exported': 0,
                'kwh_imported': 3969.800048828125,
                'v_l1_l2': 0,
                'v_l1_n': 246.60000610351562,
                'v_l2_l3': 0,
                'v_l2_n': 0,
                'v_l3_l1': 0,
                'v_l3_n': 0,
                'va_total': 609.5,
                'var_total': 0,
                'w_l1': 609.5,
                'w_l2': 0,
                'w_l3': 0,
                'w_total': 609.5
            },
            {
                'a_l1': 2.0929999351501465,
                'a_l2': 0,
                'a_l3': 0,
                'channel': 2,
                'deviceid': 4,
                'direction': 'consumption',
                'error': 0,
                'kwh_exported': 0,
                'kwh_imported': 816.5,
                'v_l1_l2': 0,
                'v_l1_n': 246.6999969482422,
                'v_l2_l3': 0,
                'v_l2_n': 0,
                'v_l3_l1': 0,
                'v_l3_n': 0,
                'va_total': 516.2000122070312,
                'var_total': -512.7999877929688,
                'w_l1': 59.29999923706055,
                'w_l2': 0,
                'w_l3': 0,
                'w_total': 59.29999923706055
            }
        ]

        battery1_powermeter_data = responses.Response(
            method='GET',
            url='http://192.168.188.11/api/v2/powermeter',
            status=200,
            json=test_data_powermeter
        )

        battery1_latest_data = responses.Response(
            method='GET',
            url='http://192.168.188.11/api/v2/latestdata',
            status=200,
            json=test_data_latest_charging
        )

        battery1_status = responses.Response(
            method='GET',
            url='http://192.168.188.11/api/v2/status',
            status=200,
            json=test_data_status_charging
        )

        battery2_powermeter_data = responses.Response(
            method='GET',
            url='http://192.168.188.12/api/v2/powermeter',
            status=200,
            json=test_data_powermeter
        )

        battery2_latest_data = responses.Response(
            method='GET',
            url='http://192.168.188.12/api/v2/latestdata',
            status=200,
            json=test_data_latest_discharging
        )

        battery2_status = responses.Response(
            method='GET',
            url='http://192.168.188.12/api/v2/status',
            status=200,
            json=test_data_status_discharging
        )

        battery3_powermeter_data = responses.Response(
            method='GET',
            url='http://155.547.4.57/api/v2/powermeter',
            status=401,
            json={}
        )

        battery3_latest_data = responses.Response(
            method='GET',
            url='http://155.547.4.57/api/v2/latestdata',
            status=401,
            json={}
        )

        battery3_status = responses.Response(
            method='GET',
            url='http://155.547.4.57/api/v2/status',
            status=200,
            json=test_data_status_charging
        )

        responses.add(battery1_latest_data)
        responses.add(battery1_status)
        responses.add(battery1_powermeter_data)

        responses.add(battery2_latest_data)
        responses.add(battery2_status)
        responses.add(battery2_powermeter_data)

        responses.add(battery3_latest_data)
        responses.add(battery3_status)
        responses.add(battery3_powermeter_data)

        token = os.getenv('AUTH_TOKEN')
        self.battery_charging_working = Sonnen(token, '192.168.188.11')  # Working and charging
        self.battery_discharging_working = Sonnen(token, '192.168.188.12')  # Working and discharging
        self.battery_unreachable = Sonnen('xyZio', '155.156.19.5')  # Not Reachable
        self.battery_wrong_token_charging = Sonnen('notWorkingToken', '155.547.4.57')  # Wrong Token

        self.battery_charging_working.update()
        self.battery_unreachable.update()
        self.battery_wrong_token_charging.update()
        self.battery_discharging_working.update()

    @responses.activate
    def test_consumption_average(self):

        result1 = self.battery_charging_working.consumption_average()
        result2 = self.battery_unreachable.consumption_average()
        result3 = self.battery_wrong_token_charging.consumption_average()
        self.assertEqual(result1, 486)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 486)

    @responses.activate
    def test_consumption(self):
        self.battery_charging_working.update()
        self.battery_unreachable.update()
        self.battery_wrong_token_charging.update()
        result1 = self.battery_charging_working.consumption()
        result2 = self.battery_unreachable.consumption()
        result3 = self.battery_wrong_token_charging.consumption()
        self.assertEqual(result1, 403)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)

    @responses.activate
    def test_installed_modules(self):
        self.battery_charging_working.update()
        self.battery_unreachable.update()
        self.battery_wrong_token_charging.update()
        result1 = self.battery_charging_working.installed_modules()
        result2 = self.battery_unreachable.installed_modules()
        result3 = self.battery_wrong_token_charging.installed_modules()
        self.assertEqual(result1, 4)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)

    @responses.activate
    def test_discharging(self):
        result1 = self.battery_charging_working.discharging()
        result2 = self.battery_unreachable.discharging()
        result3 = self.battery_wrong_token_charging.discharging()
        result4 = self.battery_discharging_working.discharging()
        self.assertEqual(result1, 0)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 439)
        result1_pac = self.battery_charging_working.pac_total
        result2_pac = self.battery_unreachable.pac_total
        result3_pac = self.battery_wrong_token_charging.pac_total
        result4_pac = self.battery_discharging_working.pac_total
        self.assertLessEqual(result1_pac, 0)
        self.assertEqual(result2_pac, 0)
        self.assertLessEqual(result3_pac, 0)
        self.assertGreaterEqual(result4_pac, 0)

    @responses.activate
    def test_charging(self):
        result1 = self.battery_charging_working.charging()
        result2 = self.battery_unreachable.charging()
        result3 = self.battery_wrong_token_charging.charging()
        result4 = self.battery_discharging_working.charging()
        self.assertEqual(result1, 94)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 0)

    @responses.activate
    def test_grid_in(self):
        result1 = self.battery_charging_working.grid_in()
        result2 = self.battery_unreachable.grid_in()
        result3 = self.battery_wrong_token_charging.grid_in()
        result4 = self.battery_discharging_working.grid_in()
        self.assertEqual(result1, 54)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 54)
        self.assertEqual(result4, 0)

    @responses.activate
    def test_grid_out(self):
        result1 = self.battery_charging_working.grid_out()
        result2 = self.battery_unreachable.grid_out()
        result3 = self.battery_wrong_token_charging.grid_out()
        result4 = self.battery_discharging_working.grid_out()
        self.assertGreaterEqual(result1, 0)
        self.assertGreaterEqual(result2, 0)
        self.assertGreaterEqual(result3, 0)
        self.assertEqual(result4, 20)

    @responses.activate
    def test_production(self):
        result1 = self.battery_charging_working.production()
        result2 = self.battery_unreachable.production()
        result3 = self.battery_wrong_token_charging.production()
        result4 = self.battery_discharging_working.production()
        self.assertEqual(result1, 578)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 102)

    @responses.activate
    def test_usoc(self):
        result1 = self.battery_charging_working.u_soc()
        result2 = self.battery_unreachable.u_soc()
        result3 = self.battery_wrong_token_charging.u_soc()
        result4 = self.battery_discharging_working.u_soc()
        self.assertEqual(result1, 98)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 99)

    @responses.activate
    def test_seconds_to_empty(self):
        result1 = self.battery_charging_working.seconds_to_empty()
        result2 = self.battery_unreachable.seconds_to_empty()
        result3 = self.battery_wrong_token_charging.seconds_to_empty()
        result4 = self.battery_discharging_working.seconds_to_empty()
        self.assertEqual(result1, 0)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 156030)

    @responses.activate
    @freeze_time("24-05-2022 15:38:23")
    def test_fully_discharged_at(self):
        result1 = self.battery_charging_working.fully_discharged_at()
        result2 = self.battery_unreachable.fully_discharged_at()
        result3 = self.battery_wrong_token_charging.fully_discharged_at()
        result4 = self.battery_discharging_working.fully_discharged_at()
        self.assertEqual(result1, '00:00')
        self.assertEqual(result2, '00:00')
        self.assertEqual(result3, '00:00')
        self.assertEqual(result4, '26.May 10:58')

    @responses.activate
    @freeze_time("24-04-2022 15:38:23")
    def test_seconds_since_full(self):
        result1 = self.battery_charging_working.seconds_since_full()
        result2 = self.battery_unreachable.seconds_since_full()
        result3 = self.battery_wrong_token_charging.seconds_since_full()
        result4 = self.battery_charging_working.seconds_since_full()
        self.assertEqual(result1, 3720)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 3720)

    @responses.activate
    def test_full_charge_capacity(self):
        result1 = self.battery_charging_working.full_charge_capacity()
        result2 = self.battery_unreachable.full_charge_capacity()
        result3 = self.battery_wrong_token_charging.full_charge_capacity()
        result4 = self.battery_discharging_working.full_charge_capacity()
        self.assertEqual(result1, 19531)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 19531)

    @responses.activate
    @freeze_time('24-04-2022 15:38:23')
    def test_time_since_full(self):
        result1 = self.battery_charging_working.time_since_full()
        result2 = self.battery_unreachable.time_since_full()
        result3 = self.battery_wrong_token_charging.time_since_full()
        result4 = self.battery_charging_working.time_since_full()
        self.assertEqual(result1, datetime.timedelta(seconds=3720))
        self.assertEqual(result2, datetime.timedelta(seconds=0))
        self.assertEqual(result3, datetime.timedelta(seconds=0))
        self.assertEqual(result4, datetime.timedelta(seconds=3720))

    @responses.activate
    @freeze_time('24-04-2022 15:38:23')
    def test_time_remaining_to_fully_charged(self):
        result1 = self.battery_charging_working.seconds_remaining_to_fully_charged()
        result2 = self.battery_unreachable.seconds_remaining_to_fully_charged()
        result3 = self.battery_wrong_token_charging.seconds_remaining_to_fully_charged()
        result4 = self.battery_discharging_working.seconds_remaining_to_fully_charged()
        self.assertEqual(result1, 25200)
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 0)

    @responses.activate
    @freeze_time('24-04-2022 15:38:23')
    def test_fully_charged_at(self):
        result1 = self.battery_charging_working.fully_charged_at()
        result2 = self.battery_unreachable.fully_charged_at()
        result3 = self.battery_wrong_token_charging.fully_charged_at()
        result4 = self.battery_discharging_working.fully_charged_at()
        self.assertEqual(result1, '24.April.2022 22:38')
        self.assertEqual(result2, 0)
        self.assertEqual(result3, 0)
        self.assertEqual(result4, 0)
