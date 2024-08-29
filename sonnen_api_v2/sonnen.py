""" SonnenAPI v2 module """

from functools import wraps

import datetime
from idlelib.pyparse import trans
import json

import requests


def get_item(_type):
    """Decorator factory for getting data from the api dictionary and casting
    to the right type """
    def decorator(fn):
        @wraps(fn)
        def inner(*args):
            try:
                result = _type(fn(*args))
            except KeyError:
                print('Key not found')
                result = None
            except ValueError:
                print(f'{fn(*args)} is not an {_type} castable!')
                result = None
            return result
        return inner
    return decorator


class Sonnen:
    """Class for managing Sonnen API data"""
    # API latestdata System-Status Groups
    IC_STATUS = 'ic_status'

    # API Item keys
    STATUS_CONSUMPTION_W = 'Consumption_W'
    STATUS_CONSUMPTION_AVG = 'Consumption_Avg'
    STATUS_PRODUCTION_W = 'Production_W'
    STATUS_BACKUPBUFFER = "BackupBuffer"
    STATUS_GRIDFEEDIN_W = 'GridFeedIn_W'
    STATUS_BATTERY_CHARGING = 'BatteryCharging'
    STATUS_BATTERY_DISCHARGING = 'BatteryDischarging'
    STATUS_REMAININGCAPACITY_WH = 'RemainingCapacity_Wh'
    STATUS_FLOW_CONSUMPTION_BATTERY = 'FlowConsumptionBattery'
    STATUS_FLOW_CONSUMPTION_GRID = 'FlowConsumptionGrid'
    STATUS_FLOW_CONSUMPTION_PRODUCTION = 'FlowConsumptionProduction'
    STATUS_FLOW_GRID_BATTERY = 'FlowGridBattery'
    STATUS_FLOW_PRODUCTION_BATTERY = 'FlowProductionBattery'
    STATUS_FLOW_PRODUCTION_GRID = 'FlowProductionGrid'
    STATUS_GRID_FEED_IN_W = 'GridFeedIn_W'
    STATUS_APPARENT_OUTPUT = 'Apparent_output'
    STATUS_PAC_TOTAL_W = 'Pac_total_W'
    STATUS_MODULES_INSTALLED = 'nrbatterymodules'
    USOC_KEY = 'USOC'
    RSOC_KEY = 'RSOC'
    DETAIL_FULL_CHARGE_CAPACITY = 'FullChargeCapacity'
    DETAIL_STATE_CORECONTROL_MODULE = "statecorecontrolmodule"
    DETAIL_PAC_TOTAL_W = 'Pac_total_W'
    DETAIL_PRODUCTION_W = 'Production_W'
    DETAIL_SECONDS_SINCE_FULLCHARGE = 'secondssincefullcharge'
    BATTERY_CYCLE_COUNT = 'cyclecount'
    BATTERY_FULL_CHARGE_CAPACITY_AH = 'fullchargecapacity'
    BATTERY_FULL_CHARGE_CAPACITY_WH = 'fullchargecapacitywh'
    BATTERY_REMAINING_CAPACITY = 'remainingcapacity'
    BATTERY_MAX_CELL_TEMP = 'maximumcelltemperature'
    BATTERY_MAX_CELL_VOLTAGE = 'maximumcellvoltage'
    BATTERY_MAX_MODULE_CURRENT = 'maximummodulecurrent'
    BATTERY_MAX_MODULE_VOLTAGE = 'maximummoduledcvoltage'
    BATTERY_MAX_MODULE_TEMP = 'maximummoduletemperature'
    BATTERY_MIN_CELL_TEMP = 'minimumcelltemperature'
    BATTERY_MIN_CELL_VOLTAGE = 'minimumcellvoltage'
    BATTERY_MIN_MODULE_CURRENT = 'minimummodulecurrent'
    BATTERY_MIN_MODULE_VOLTAGE = 'minimummoduledcvoltage'
    BATTERY_MIN_MODULE_TEMP = 'minimummoduletemperature'
    BATTERY_RSOC = 'relativestateofcharge'
    BATTERY_USABLE_REMAINING_CAPACITY = 'usableremainingcapacity'
    BATTERY_SYSTEM_CURRENT = 'systemcurrent'
    BATTERY_SYSTEM_VOLTAGE = 'systemdcvoltage'
    POWERMETER_KWH_CONSUMED = 'kwh_imported'
    POWERMETER_KWH_PRODUCED = 'kwh_imported'
    CONFIGURATION_EM_OPERATINGMODE = "EM_OperatingMode"
    CONFIGURATION_EM_USOC = "EM_USOC"
    CONFIGURATION_DE_SOFTWARE = "DE_Software"
    IC_ECLIPSE_LED = "Eclipse Led"

    # default timeout
    TIMEOUT = 5

    def __init__(self, auth_token: str, ip_address: str) -> None:
        self.ip_address = ip_address
        self.auth_token = auth_token
        self.url = f'http://{ip_address}'
        self.header = {'Auth-Token': self.auth_token}

        # read api endpoints
        self.status_api_endpoint = f'{self.url}/api/v2/status'
        self.latest_details_api_endpoint = f'{self.url}/api/v2/latestdata'
        self.battery_api_endpoint = f'{self.url}/api/v2/battery'
        self.powermeter_api_endpoint = f'{self.url}/api/v2/powermeter'
        self.configurations_api_endpoint = f'{self.url}/api/v2/configurations'

        # api data
        self._latest_details_data = {}
        self._status_data = {}
        self._ic_status = {}
        self._battery_status = {}
        self._powermeter_data = []
        self._powermeter_production = {}
        self._powermeter_consumption = {}
        self._configurations_data = {}

    def fetch_latest_details(self) -> bool:
        """Fetches latest details api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.latest_details_api_endpoint,
                headers=self.header, timeout=self.TIMEOUT
            )
            if response.status_code == 200:
                self._latest_details_data = response.json()
                self._ic_status = self._latest_details_data[self.IC_STATUS]
                return True
        except requests.ConnectionError as conn_error:
            print('Connection error to battery system - ', conn_error)
        return False

    def fetch_configurations(self) -> bool:
        """Fetches configurations api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.configurations_api_endpoint,
                headers=self.header, timeout=self.TIMEOUT
            )
            if response.status_code == 200:
                self._configurations_data = response.json()
                return True
        except requests.ConnectionError as conn_error:
            print('Connection error to sonnenBatterie - ', conn_error)
        return False

    def fetch_status(self) -> bool:
        """Fetches status api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.status_api_endpoint,
                headers=self.header, timeout=self.TIMEOUT
            )
            if response.status_code == 200:
                self._status_data = response.json()
                return True
        except requests.ConnectionError as conn_error:
            print('Connection error to battery system - ', conn_error)
        return False

    def fetch_powermeter(self) -> bool:
        """Fetches powermeter api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.powermeter_api_endpoint,
                headers=self.header, timeout=self.TIMEOUT
            )
            if response.status_code == 200:
                self._powermeter_data = response.json()
                self._powermeter_production = self._powermeter_data[0]
                self._powermeter_consumption = self._powermeter_data[1]

            #    print(self._powermeter_data)
                return True
        except requests.ConnectionError as conn_error:
            print('Connection error to battery system - ', conn_error)
        return False

    def fetch_battery_status(self) -> bool:
        """Fetches battery details api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.battery_api_endpoint,
                headers=self.header, timeout=self.TIMEOUT)
            if response.status_code == 200:
                self._battery_status = response.json()
                return True
        except requests.ConnectionError as conn_err:
            print('Connection error to battery system - ', conn_err)
        return False

    def update(self) -> bool:
        """Updates data from apis of the sonnenBatterie
            Returns:
                True if all updates were successful, else False
        """
        success = self.fetch_latest_details()
        success = success and self.fetch_status()
        success = success and self.fetch_battery_status()
        success = success and self.fetch_powermeter()
        return success


    @get_item(float)
    def kwh_consumed(self) -> float:
        """Consumed kWh"""
        return self._powermeter_consumption[self.POWERMETER_KWH_CONSUMED]

    @get_item(float)
    def kwh_produced(self) -> float:
        """Produced kWh"""
        return self._powermeter_production[self.POWERMETER_KWH_PRODUCED]

    @get_item(int)
    def consumption(self) -> int:
        """Consumption of the household
            Returns:
                house consumption in Watt
        """
        return self._latest_details_data[self.STATUS_CONSUMPTION_W]

    @get_item(int)
    def consumption_average(self) -> int:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """
        return self._status_data[self.STATUS_CONSUMPTION_AVG]

    @get_item(int)
    def production(self) -> int:
        """Power production of PV
            Returns:
                PV production in Watts
        """
        return self._latest_details_data[self.STATUS_PRODUCTION_W]

    @get_item(int)
    def seconds_to_empty(self) -> int:
        """Time until battery discharged
            Returns:
                Time in seconds
        """
        seconds = int((self.remaining_capacity_wh() / self.discharging()) * 3600) if self.discharging() else 0

        return seconds

    @get_item(int)
    def seconds_to_reserve(self) -> int:
        """Time until battery at backup reserve
            Returns:
                Time in seconds
        """
        capacity_until_reserve = self.remaining_capacity_wh() - self.backup_buffer_capacity_wh()
        seconds = int((capacity_until_reserve / self.discharging()) * 3600) if self.discharging() else 0

        return seconds

    def fully_discharged_at(self) -> datetime:
        """Future time of battery fully discharged
            Returns:
                Future time
        """
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_to_empty())) if self.discharging() else 0

    def backup_reserve_at(self) -> datetime:
        """Future time of battery discharged to backup reserve
            Returns:
                Future time
        """
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_to_reserve())) if self.discharging() else 0

    @get_item(int)
    def seconds_since_full(self) -> int:
        """Seconds passed since full charge
            Returns:
                seconds as integer
        """
        return self._latest_details_data[self.IC_STATUS][self.DETAIL_SECONDS_SINCE_FULLCHARGE]

    @get_item(int)
    def installed_modules(self) -> int:
        """Battery modules installed in the system
            Returns:
                Number of modules
        """
        return self._ic_status[self.STATUS_MODULES_INSTALLED]

    @get_item(int)
    def u_soc(self) -> int:
        """User state of charge (usable charge)
            Returns:
                User SoC in percent
        """
        return self._latest_details_data[self.USOC_KEY]

    @get_item(int)
    def u_roc(self) -> int:
        """Relative state of charge (actual charge)
            Returns:
                Integer Percent
        """
        return self._latest_details_data[self.RSOC_KEY]

    @get_item(int)
    def remaining_capacity_wh(self) -> int:
        """ Remaining capacity in watt-hours
         IMPORTANT NOTE: Why is this double as high as it should be???
            Returns:
                 Remaining USABLE capacity of the battery in Wh
        """
        return self._status_data[self.STATUS_REMAININGCAPACITY_WH] // 2

    @get_item(int)
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery
            Returns:
                Capacity in Wh
        """
        return self._latest_details_data[self.DETAIL_FULL_CHARGE_CAPACITY]

    def time_since_full(self) -> datetime.timedelta:
        """Calculates time since full charge.
           Returns:
               Time in format days hours minutes seconds
        """
        return datetime.timedelta(seconds=self.seconds_since_full())

    def last_time_full(self) -> datetime:
        """Calculates last time at full charge.
           Returns:
               DateTime
        """
        return datetime.datetime.now() - self.time_since_full()

    @get_item(int)
    def seconds_until_fully_charged(self) -> int:
        """Time remaining until fully charged
            Returns:
                Time in seconds
        """
        remaining_charge = self.battery_full_charge_capacity_wh() - self.remaining_capacity_wh()
        seconds = int(remaining_charge / self.charging()) * 3600 if self.charging() else 0

        return seconds

    def fully_charged_at(self) -> datetime:
        """ Calculating time until fully charged """
        #    return final_time.strftime('%d.%B.%Y %H:%M')
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_until_fully_charged())) if self.charging() else 0

    @get_item(int)
    def pac_total(self) -> int:
        """ Battery inverter load
            Negative if charging
            Positive if discharging
            Returns:
                  Inverter load value in watt
        """
        return self._latest_details_data[self.DETAIL_PAC_TOTAL_W]

    @get_item(int)
    def charging(self) -> int:
        """Actual battery charging value
            Returns:
                Charging value in watt
        """
        charge = self.pac_total()

        return abs(charge) if charge < 0 else 0

    @get_item(int)
    def discharging(self) -> int:
        """Actual battery discharging value
            Returns:
                Discharging value in watt
        """
        charge = self.pac_total()

        return charge if charge > 0 else 0

    @get_item(int)
    def grid_in(self) -> int:
        """Actual grid feed in value
            Returns:
                Value in watt
        """
        return self._status_data[self.STATUS_GRIDFEEDIN_W] if self._status_data[self.STATUS_GRIDFEEDIN_W] > 0 else 0

    @get_item(int)
    def grid_out(self) -> int:
        """Actual grid out value
            Returns:
                Value in watt
        """
        return abs(self._status_data[self.STATUS_GRIDFEEDIN_W]) if self._status_data[self.STATUS_GRIDFEEDIN_W] < 0 else 0

    @get_item(int)
    def battery_cycle_count(self) -> int:
        """Number of charge/discharge cycles
            Returns:
                Number of charge/discharge cycles
        """
        return self._battery_status[self.BATTERY_CYCLE_COUNT]

    @get_item(float)
    def battery_full_charge_capacity(self) -> float:
        """Fullcharge capacity
            Returns:
                Fullcharge capacity in Ah
        """
        return self._battery_status[self.BATTERY_FULL_CHARGE_CAPACITY_AH]

    @get_item(float)
    def battery_max_cell_temp(self) -> float:
        """Max cell temperature
            Returns:
                Maximum cell temperature in ºC
        """
        return self._battery_status[self.BATTERY_MAX_CELL_TEMP]

    @get_item(float)
    def battery_max_cell_voltage(self) -> float:
        """Max cell voltage
            Returns:
                Maximum cell voltage in Volt
        """
        return self._battery_status[self.BATTERY_MAX_CELL_VOLTAGE]

    @get_item(float)
    def battery_max_module_current(self) -> float:
        """Max module DC current
            Returns:
                Maximum module DC current in Ampere
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_CURRENT]

    @get_item(float)
    def battery_max_module_voltage(self) -> float:
        """Max module DC voltage
            Returns:
                Maximum module DC voltage in Volt
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_VOLTAGE]

    @get_item(float)
    def battery_max_module_temp(self) -> float:
        """Max module DC temperature
            Returns:
                Maximum module DC temperature in ºC
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_TEMP]

    @get_item(float)
    def battery_min_cell_temp(self) -> float:
        """Min cell temperature
            Returns:
                Minimum cell temperature in ºC
        """
        return self._battery_status[self.BATTERY_MIN_CELL_TEMP]

    @get_item(float)
    def battery_min_cell_voltage(self) -> float:
        """Min cell voltage
            Returns:
                Minimum cell voltage in Volt
        """
        return self._battery_status[self.BATTERY_MIN_CELL_VOLTAGE]

    @get_item(float)
    def battery_min_module_current(self) -> float:
        """Min module DC current
            Returns:
                Minimum module DC current in Ampere
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_CURRENT]

    @get_item(float)
    def battery_min_module_voltage(self) -> float:
        """Min module DC voltage
            Returns:
                Minimum module DC voltage in Volt
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_VOLTAGE]

    @get_item(float)
    def battery_min_module_temp(self) -> float:
        """Min module DC temperature
            Returns:
                Minimum module DC temperature in ºC
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_TEMP]

    @get_item(float)
    def battery_rsoc(self) -> float:
        """Relative state of charge
            Returns:
                Relative state of charge in %
        """
        return self._battery_status[self.BATTERY_RSOC]

    @get_item(float)
    def battery_full_charge_capacity_wh(self) -> float:
        """Full charge capacity
            Returns:
                Fullcharge capacity in Wh
        """
        return self._battery_status[self.BATTERY_FULL_CHARGE_CAPACITY_WH]

    @get_item(float)
    def battery_remaining_capacity(self) -> float:
        """Remaining capacity
            Returns:
                Remaining capacity in Ah
        """
        return self._battery_status[self.BATTERY_REMAINING_CAPACITY]

    @get_item(float)
    def battery_system_dc_voltage(self) -> float:
        """System battery voltage
            Returns:
                Voltage in Volt
        """
        return self._battery_status[self.BATTERY_SYSTEM_VOLTAGE]

    @get_item(float)
    def battery_remaining_capacity_wh(self) -> float:
        """Remaining capacity Wh calculated from Ah
            Returns:
                Remaining capacity in Wh
        """
        capacity_ah = self.battery_remaining_capacity()

        return capacity_ah * self.battery_system_dc_voltage()

    @get_item(float)
    def battery_usable_remaining_capacity(self) -> float:
        """Usable Remaining capacity
            Returns:
                Usable Remaining capacity in Ah
        """
        return self._battery_status[self.BATTERY_USABLE_REMAINING_CAPACITY]

    @get_item(float)
    def battery_system_current(self) -> float:
        """System current
            Returns:
                System current in Ampere
        """
        return self._battery_status[self.BATTERY_SYSTEM_CURRENT]

    @get_item(int)
    def configuration_em_operatingmode(self) -> int:
        """Operating Mode
            Returns:
                Mode Integer
                "1": Manual
                "2": Automatic - Self Consumption
                "6": Battery-Module-Extension (30%)
                "10": Time-Of-Use
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[self.CONFIGURATION_EM_OPERATINGMODE]

    @get_item(int)
    def configuration_em_usoc(self) -> int:
        """User State Of Charge - BackupBuffer value (includes 6% unusable reserve)
            Returns:
                Integer Percent
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[self.CONFIGURATION_EM_USOC]

    @get_item(int)
    def status_backup_buffer(self) -> int:
        """BackupBuffer value from Status api
            Returns:
                Integer Percent
        """
        return self._status_data[self.STATUS_BACKUPBUFFER]

    @get_item(bool)
    def status_battery_charging(self) -> bool:
        """BatteryCharging
            Returns:
                Bool
        """
        return self._status_data[self.STATUS_BATTERY_CHARGING]

    @get_item(bool)
    def status_battery_discharging(self) -> bool:
        """BatteryDischarging
            Returns:
                Bool
        """
        return self._status_data[self.STATUS_BATTERY_DISCHARGING]

    @get_item(dict)
    def status_flows(self) -> dict:
        """Status flows: production -> grid , battery
            Returns:
                dict of name:bool
        """
        flows = {
            "FlowConsumptionBattery":self._status_data[self.STATUS_FLOW_CONSUMPTION_BATTERY],
            "FlowConsumptionGrid":self._status_data[self.STATUS_FLOW_CONSUMPTION_GRID],
            "FlowConsumptionProduction":self._status_data[self.STATUS_FLOW_CONSUMPTION_PRODUCTION],
            "FlowGridBattery":self._status_data[self.STATUS_FLOW_CONSUMPTION_BATTERY],
            "FlowProductionBattery":self._status_data[self.STATUS_FLOW_PRODUCTION_BATTERY],
            "FlowProductionGrid":self._status_data[self.STATUS_FLOW_PRODUCTION_GRID],
        }
        return flows

    @get_item(int)
    def status_grid_feed_in(self) -> int:
        """GridFeedIn_W
            Returns:
                Feed watts, -ve is export (actually float with zero decimal part)
        """
        return int(self._status_data[self.STATUS_GRID_FEED_IN_W])

    @get_item(int)
    def backup_buffer_capacity_wh(self) -> int:
        """Backup Buffer capacity (includes 6% unusable)
            Returns:
                Backup Buffer in Wh
        """
        buffer_percent = self.configuration_em_usoc()
        full_charge = self.battery_full_charge_capacity_wh()

        return int(full_charge * buffer_percent / 100)

    @get_item(int)
    def backup_buffer_usable_capacity_wh(self) -> int:
        """Backup Buffer usable capacity (excludes 6% unusable)
            Returns:
                Usable Backup Buffer in Wh
        """
        buffer_percent = self.configuration_em_usoc()
        full_charge = self.battery_full_charge_capacity_wh()

        return int(full_charge * (buffer_percent - 6) / 100) if buffer_percent > 6 else 0

    def state_core_control_module(self) -> str:
        """State of control module: config, ongrid, ...
            Returns:
                String
        """
        return self._latest_details_data[self.IC_STATUS][self.DETAIL_STATE_CORECONTROL_MODULE]

    def configuration_de_software(self) -> str:
        """Software version
            Returns:
                String
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[self.CONFIGURATION_DE_SOFTWARE]

    def ic_eclipse_led(self) -> str:
        """System-Status:
                "Eclipse Led":{
                    "Blinking Red":false,
                    "Brightness":100,
                    "Pulsing Green":false,
                    "Pulsing Orange":false,
                    "Pulsing White":true,
                    "Solid Red":false
                }
            Returns:
                JSON String
        """
        return self._latest_details_data[self.IC_STATUS][self.IC_ECLIPSE_LED]
