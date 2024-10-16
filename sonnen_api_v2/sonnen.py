""" SonnenAPI v2 module """

from functools import wraps
from typing import Optional, Union
from math import floor

import datetime
from idlelib.pyparse import trans

import aiohttp
import asyncio

import logging
import requests
from .const import *

def get_item(_type):
    """Decorator factory for getting data from the api dictionary and casting
    to the right type """
    def decorator(fn):
        @wraps(fn)
        def inner(*args):
            if fn(*args) is None:
                return None
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
    """Class for managing Sonnen API V2 data"""
    from .wrapped import set_request_connect_timeouts, get_request_connect_timeouts
    from .wrapped import get_latest_data, get_configurations, get_status, get_powermeter, get_battery, get_inverter


    def __init__(self, auth_token: str, ip_address: str, logger_name: str = None) -> None:
#        wrapped.__init__(self)
        self.last_updated = None
        self.logger = logging.getLogger(logger_name) if logger_name is not None else None
        self.ip_address = ip_address
        self.auth_token = auth_token
        self.url = f'http://{ip_address}'
        self.header = {'Auth-Token': self.auth_token}
    #    self.request_timeouts = (TIMEOUT, TIMEOUT)
        self.set_request_connect_timeouts( (TIMEOUT, TIMEOUT) )
        # read api endpoints
        self.status_api_endpoint = f'{self.url}/api/v2/status'
        self.latest_details_api_endpoint = f'{self.url}/api/v2/latestdata'
        self.battery_api_endpoint = f'{self.url}/api/v2/battery'
        self.powermeter_api_endpoint = f'{self.url}/api/v2/powermeter'
        self.configurations_api_endpoint = f'{self.url}/api/v2/configurations'
        self.inverter_api_endpoint = f'{self.url}/api/v2/inverter'

        # api data
        self._latest_details_data = {}
        self._status_data = {}
        self._ic_status = {}
        self._battery_status = {}
        self._powermeter_data = []
        self._powermeter_production = {}
        self._powermeter_consumption = {}
        self._configurations_data = {}
        self._inverter_data = {}

    def _log_error(self, msg):
        if self.logger:
            self.logger.error(msg)
        else:
            print(msg)

    def fetch_latest_details(self) -> bool:
        """Fetches latest details api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.latest_details_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._latest_details_data = response.json()
                self._ic_status = self._latest_details_data[IC_STATUS]
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
        return False

    def fetch_configurations(self) -> bool:
        """Fetches configurations api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.configurations_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._configurations_data = response.json()
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
        return False

    def fetch_status(self) -> bool:
        """Fetches status api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.status_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._status_data = response.json()
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
        return False

    def fetch_powermeter(self) -> bool:
        """Fetches powermeter api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.powermeter_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._powermeter_data = response.json()
                self._powermeter_production = self._powermeter_data[0]
                self._powermeter_consumption = self._powermeter_data[1]

            #    print(self._powermeter_data)
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
        return False

    def fetch_battery_status(self) -> bool:
        """Fetches battery details api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.battery_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._battery_status = response.json()
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
        return False

    def fetch_inverter_data(self) -> bool:
        """Fetches inverter data api
            Returns:
                True if fetch was successful, else False
        """
        try:
            response = requests.get(
                self.inverter_api_endpoint,
                headers=self.header, timeout=self.request_timeouts
            )
            if response.status_code == 200:
                self._inverter_data = response.json()
                return True
        except requests.ConnectionError as conn_error:
            self._log_error(f'Connection error to sonnenBatterie - {conn_error}')
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
        self.last_updated = datetime.datetime.now() if success else None
        return success

    async def _async_fetch_data(self, url: str) -> dict:
        """Fetches data from the API endpoint with asyncio"""
        try:
            async with aiohttp.ClientSession(headers=self.header) as session:
                resp = await session.get(url)
                data = resp.json()
                return await data
        except aiohttp.ClientError as error:
            self._log_error(f'Battery: {self.ip_address} is offline!')
        except asyncio.TimeoutError as error:
            self._log_error(f'Timeout error while accessing: {url}')
        except Exception as error:
            self._log_error(f'Error while data parsing {error}')
            return {}

    async def async_fetch_latest_details(self) -> bool:
        """Fetches latest details api as coroutine"""
        try:
            self._latest_details_data = await self._async_fetch_data(
                self.latest_details_api_endpoint
            )
            self._ic_status = self._latest_details_data[self.IC_STATUS]
            return True
        except Exception as error:
            self._log_error(f'Error occurred while data parsing latest details:{error}')
            return False

    async def async_fetch_status(self) -> bool:
        """Fetches status api as coroutine"""
        try:
            self._status_data = await self._async_fetch_data(
                self.status_api_endpoint
            )
            return True
        except Exception as error:
            self._log_error(f'Error occurred while data parsing status:{error}')
            return False

    async def async_fetch_battery_status(self) -> bool:
        """Fetches battery details api as coroutine"""
        try:
            self._battery_status = await self._async_fetch_data(
                self.battery_api_endpoint
            )
            return True
        except Exception as error:
            self._log_error(f'Error occurred while data parsing battery status:{error}')
        return False


    async def async_update(self) -> bool:
        """Updates data from apis of the sonnenBatterie as coroutine"""
        success = await self.async_fetch_latest_details()
        success = success and await self.async_fetch_status()
        success = success and await self.async_fetch_battery_status()
        self.last_updated = datetime.datetime.now()
        return success

    @property
    def last_updated(self) -> Optional[datetime.datetime]:
        """Last time data fetched from batterie"""
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated: datetime.datetime=None):
        """Last time data fetched from batterie"""
        self._last_updated = last_updated

    @property
    @get_item(float)
    def kwh_consumed(self) -> float:
        """Consumed kWh"""
        return self._powermeter_consumption[POWERMETER_KWH_CONSUMED]

    @property
    @get_item(float)
    def kwh_produced(self) -> float:
        """Produced kWh"""
        return self._powermeter_production[POWERMETER_KWH_PRODUCED]

    @property
    @get_item(int)
    def consumption(self) -> int:
        """Consumption of the household
            Returns:
                house consumption in Watt
        """
        return self._latest_details_data[STATUS_CONSUMPTION_W]

    @property
    @get_item(int)
    def consumption_average(self) -> int:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """
        return self._status_data[STATUS_CONSUMPTION_AVG]

    @property
    @get_item(int)
    def production(self) -> int:
        """Power production of PV
            Returns:
                PV production in Watts
        """
        return self._latest_details_data[STATUS_PRODUCTION_W]

    @property
    @get_item(int)
    def seconds_to_empty(self) -> int:
        """Time until battery discharged
            Returns:
                Time in seconds
        """
        seconds = int((self.battery_remaining_capacity_wh / self.discharging) * 3600) if self.discharging else 0

        return seconds

    @property
    @get_item(int)
    def seconds_to_reserve(self) -> Union[int, None]:
        """Time until battery capacity at backup reserve
            Above reserve:
                Charging - None
                Discharging - seconds to reserve
            Below Reserve
                Charging - seconds to reserve
                Discharging - negative seconds since reserve
                Standby - None
            Returns:
                Time in seconds
        """
        capacity_until_reserve = self.battery_remaining_capacity_wh - self.backup_buffer_capacity_wh
        if capacity_until_reserve > 0:
            seconds = int((capacity_until_reserve / self.discharging) * 3600) if self.discharging else None
        else:
            if self.charging:
                seconds = int((abs(capacity_until_reserve) / self.charging) * 3600)
            else:
                seconds = int((capacity_until_reserve / self.discharging) * 3600) if self.discharging else None

    #    print(f'capacity_until_reserve: {capacity_until_reserve}  Seconds: {seconds}  DischargeW: {self.discharging}')
        return seconds

    @property
    @get_item(int)
    def using_reserve(self) -> int:
        """Is backup reserve being used
            Returns:
                Bool - true when reserve in use
        """
        capacity_until_reserve = self.battery_remaining_capacity_wh - self.backup_buffer_capacity_wh
        return capacity_until_reserve < 0

    @property
    def fully_discharged_at(self) -> Optional[datetime.datetime]:
        """Future time of battery fully discharged
            Returns:
                Datetime discharged or None when not discharging
        """
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_to_empty)) if self.discharging else None

    @property
    def backup_reserve_at(self) -> Optional[datetime.datetime]:
        """Time battery charged/discharged to backup reserve
            Returns:
                Datetime charged/discharged to reserve or None when not charging/discharging
        """
        seconds = self.seconds_to_reserve
        if seconds is None:
            return None

        if seconds < 0:
            return (datetime.datetime.now() - datetime.timedelta(seconds=abs(seconds))) if self.discharging else None
        else:
            return (datetime.datetime.now() + datetime.timedelta(seconds=seconds)) if self.discharging else None

    @property
    @get_item(int)
    def seconds_since_full(self) -> int:
        """Seconds passed since full charge
            Returns:
                seconds as integer
        """
        return self._latest_details_data[IC_STATUS][DETAIL_SECONDS_SINCE_FULLCHARGE]

    @property
    @get_item(int)
    def installed_modules(self) -> int:
        """Battery modules installed in the system
            Returns:
                Number of modules
        """
        return self._ic_status[STATUS_MODULES_INSTALLED]

    @property
    @get_item(int)
    def u_soc(self) -> int:
        """User state of charge (usable charge)
            Returns:
                Integer Percent
        """
        return self._latest_details_data[DETAIL_USOC]

    @property
    @get_item(int)
    def r_soc(self) -> int:
        """Relative state of charge (actual charge)
            Returns:
                Integer Percent
        """
        return self._latest_details_data[DETAIL_RSOC]

    @property
    @get_item(int)
    def remaining_capacity_wh(self) -> int:
        """ Remaining capacity in watt-hours
        IMPORTANT NOTE: Why is this double as high as it should be???
            use battery_remaining_capacity_wh for calculated value
            Returns:
                Remaining USABLE capacity of the battery in Wh
        """
        return self._status_data[STATUS_REMAININGCAPACITY_WH]

    @property
    @get_item(int)
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery
            Returns:
                Capacity in Wh
        """
        return self._latest_details_data[DETAIL_FULL_CHARGE_CAPACITY]

    @property
    def time_since_full(self) -> datetime.timedelta:
        """Calculates time since full charge.
           Returns:
               Time in format days hours minutes seconds
        """
        return datetime.timedelta(seconds=self.seconds_since_full)

    @property
    def last_time_full(self) -> datetime.datetime:
        """Calculates last time at full charge.
           Returns:
               DateTime
        """
        return datetime.datetime.now() - self.time_since_full

    @property
    @get_item(int)
    def seconds_until_fully_charged(self) -> Union[int, None]:
        """Time remaining until fully charged
            Returns:
                Time in seconds - None when not charging, zero when fully charged
        """
        remaining_charge = self.battery_full_charge_capacity_wh - self.battery_remaining_capacity_wh
        seconds = int(remaining_charge / self.charging) * 3600 if self.charging else None

        return seconds if remaining_charge != 0 else 0

    @property
    def fully_charged_at(self) -> Optional[datetime.datetime]:
        """ Calculate time until fully charged
            Returns:
                Datetime or None when not charging
        """
        #    return final_time.strftime('%d.%B.%Y %H:%M')
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_until_fully_charged)) if self.charging else None

    @property
    @get_item(int)
    def pac_total(self) -> int:
        """ Battery inverter load
            Negative if charging
            Positive if discharging
            Returns:
                Inverter load in watt
        """
#        print (f'DETAIL_PAC_TOTAL_W: {self._latest_details_data[DETAIL_PAC_TOTAL_W]}')
        return self._latest_details_data[DETAIL_PAC_TOTAL_W]

    @property
    @get_item(int)
    def charging(self) -> int:
        """Actual battery charging value is negative
            Returns:
                Charging value in watt
        """
        return abs(self.pac_total) if self.pac_total < 0 else 0

    @property
    @get_item(int)
    def discharging(self) -> int:
        """Actual battery discharging value
            Returns:
                Discharging value in watt
        """
#        print (f'self.pac_total: {self.pac_total}')
        return self.pac_total if self.pac_total > 0 else 0

    @property
    @get_item(int)
    def grid_in(self) -> int:
        """Actual grid feed in value
            Returns:
                Value in watt
        """
        return self._status_data[STATUS_GRIDFEEDIN_W] if self._status_data[STATUS_GRIDFEEDIN_W] > 0 else 0

    @property
    @get_item(int)
    def grid_out(self) -> int:
        """Actual grid out value
            Returns:
                Value in watt
        """
        return abs(self._status_data[STATUS_GRIDFEEDIN_W]) if self._status_data[STATUS_GRIDFEEDIN_W] < 0 else 0

    @property
    @get_item(int)
    def battery_cycle_count(self) -> int:
        """Number of charge/discharge cycles
            Returns:
                Number of charge/discharge cycles
        """
        return self._battery_status[BATTERY_CYCLE_COUNT]

    @property
    @get_item(float)
    def battery_full_charge_capacity(self) -> float:
        """Fullcharge capacity
            Returns:
                Fullcharge capacity in Ah
        """
        return self._battery_status[BATTERY_FULL_CHARGE_CAPACITY_AH]

    @property
    @get_item(float)
    def battery_max_cell_temp(self) -> float:
        """Max cell temperature
            Returns:
                Maximum cell temperature in ºC
        """
        return self._battery_status[BATTERY_MAX_CELL_TEMP]

    @property
    @get_item(float)
    def battery_max_cell_voltage(self) -> float:
        """Max cell voltage
            Returns:
                Maximum cell voltage in Volt
        """
        return self._battery_status[BATTERY_MAX_CELL_VOLTAGE]

    @property
    @get_item(float)
    def battery_max_module_current(self) -> float:
        """Max module DC current
            Returns:
                Maximum module DC current in Ampere
        """
        return self._battery_status[BATTERY_MAX_MODULE_CURRENT]

    @property
    @get_item(float)
    def battery_max_module_voltage(self) -> float:
        """Max module DC voltage
            Returns:
                Maximum module DC voltage in Volt
        """
        return self._battery_status[BATTERY_MAX_MODULE_VOLTAGE]

    @property
    @get_item(float)
    def battery_max_module_temp(self) -> float:
        """Max module DC temperature
            Returns:
                Maximum module DC temperature in ºC
        """
        return self._battery_status[BATTERY_MAX_MODULE_TEMP]

    @property
    @get_item(float)
    def battery_min_cell_temp(self) -> float:
        """Min cell temperature
            Returns:
                Minimum cell temperature in ºC
        """
        return self._battery_status[BATTERY_MIN_CELL_TEMP]

    @property
    @get_item(float)
    def battery_min_cell_voltage(self) -> float:
        """Min cell voltage
            Returns:
                Minimum cell voltage in Volt
        """
        return self._battery_status[BATTERY_MIN_CELL_VOLTAGE]

    @property
    @get_item(float)
    def battery_min_module_current(self) -> float:
        """Min module DC current
            Returns:
                Minimum module DC current in Ampere
        """
        return self._battery_status[BATTERY_MIN_MODULE_CURRENT]

    @property
    @get_item(float)
    def battery_min_module_voltage(self) -> float:
        """Min module DC voltage
            Returns:
                Minimum module DC voltage in Volt
        """
        return self._battery_status[BATTERY_MIN_MODULE_VOLTAGE]

    @property
    @get_item(float)
    def battery_min_module_temp(self) -> float:
        """Min module DC temperature
            Returns:
                Minimum module DC temperature in ºC
        """
        return self._battery_status[BATTERY_MIN_MODULE_TEMP]

    @property
    @get_item(float)
    def battery_rsoc(self) -> float:
        """Relative state of charge
            Returns:
                Relative state of charge in %
        """
        return self._battery_status[BATTERY_RSOC]

    @property
    @get_item(float)
    def battery_full_charge_capacity_wh(self) -> float:
        """Full charge capacity
            Returns:
                Fullcharge capacity in Wh
        """
        return self._battery_status[BATTERY_FULL_CHARGE_CAPACITY_WH]

    @property
    @get_item(float)
    def battery_remaining_capacity(self) -> float:
        """Remaining capacity
            Returns:
                Remaining capacity in Ah
        """
        return self._battery_status[BATTERY_REMAINING_CAPACITY]

    @property
    @get_item(float)
    def battery_system_dc_voltage(self) -> float:
        """System battery voltage
            Returns:
                Voltage in Volt
        """
        return self._battery_status[BATTERY_SYSTEM_VOLTAGE]

    @property
    @get_item(int)
    def battery_remaining_capacity_wh(self) -> int:
        """Remaining capacity Wh calculated from Ah
            Returns:
                Floor Int Wh
        """
        capacity_ah = self.battery_remaining_capacity

        return floor(capacity_ah * self.battery_system_dc_voltage)

    @property
    @get_item(float)
    def battery_usable_remaining_capacity(self) -> float:
        """Usable Remaining capacity
            Returns:
                Usable Remaining capacity in Ah
        """
        return self._battery_status[BATTERY_USABLE_REMAINING_CAPACITY]

    @property
    @get_item(float)
    def battery_system_current(self) -> float:
        """System current
            Returns:
                System current in Ampere
        """
        return self._battery_status[BATTERY_SYSTEM_CURRENT]

    @property
    @get_item(float)
    def battery_system_dc_voltage(self) -> float:
        """System battery voltage
            Returns:
                Voltage in Volt
        """
        return self._battery_status[BATTERY_SYSTEM_VOLTAGE]

    @property
    @get_item(int)
    def configuration_em_operatingmode(self) -> int:
        """Operating Mode
            Returns:
                Integer code
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[CONFIGURATION_EM_OPERATINGMODE]

    @property
    def str_em_operatingmode(self) -> str:
        """Operating Mode code translated
            Returns:
                string
        """
        _EM_OPERATINGMODE = {
            "1": 'Manual',
            "2": 'Automatic - Self Consumption',
            "6": 'Battery-Module-Extension (30%)',
            "10": 'Time-Of-Use'
        }
        if self._configurations_data == {}:
            self.fetch_configurations()

        return _EM_OPERATINGMODE[self._configurations_data[CONFIGURATION_EM_OPERATINGMODE]]

    @property
    @get_item(int)
    def configuration_em_usoc(self) -> int:
        """User State Of Charge - BackupBuffer value (includes 6% unusable reserve)
            Returns:
                Integer Percent
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[CONFIGURATION_EM_USOC]

    @property
    @get_item(int)
    def status_backup_buffer(self) -> int:
        """BackupBuffer value from Status api
            Returns:
                Integer Percent
        """
        return self._status_data[STATUS_BACKUPBUFFER]

    @property
    @get_item(bool)
    def status_battery_charging(self) -> bool:
        """BatteryCharging
            Returns:
                Bool
        """
        return self._status_data[STATUS_BATTERY_CHARGING]

    @property
    @get_item(bool)
    def status_battery_discharging(self) -> bool:
        """BatteryDischarging
            Returns:
                Bool
        """
        return self._status_data[STATUS_BATTERY_DISCHARGING]

    @property
    @get_item(dict)
    def status_flows(self) -> dict:
        """Status flows: production -> grid , battery
            Returns:
                dict of name:bool
        """
        flows = {
            "FlowConsumptionBattery":self._status_data[STATUS_FLOW_CONSUMPTION_BATTERY],
            "FlowConsumptionGrid":self._status_data[STATUS_FLOW_CONSUMPTION_GRID],
            "FlowConsumptionProduction":self._status_data[STATUS_FLOW_CONSUMPTION_PRODUCTION],
            "FlowGridBattery":self._status_data[STATUS_FLOW_CONSUMPTION_BATTERY],
            "FlowProductionBattery":self._status_data[STATUS_FLOW_PRODUCTION_BATTERY],
            "FlowProductionGrid":self._status_data[STATUS_FLOW_PRODUCTION_GRID],
        }
        return flows

    @property
    @get_item(int)
    def status_grid_feed_in(self) -> int:
        """GridFeedIn_W
            Returns:
                Feed watts, -ve is export (actually float with zero decimal part)
        """
        return int(self._status_data[STATUS_GRIDFEEDIN_W])

    @property
    @get_item(bool)
    def status_discharge_not_allowed(self) -> bool:
        """dischargeNotAllowed - Surplus Fullchage feature in progress
            Returns:
                Bool
        """
        return self._status_data[STATUS_DISCHARGE_NOT_ALLOWED]

    @property
    @get_item(int)
    def backup_buffer_capacity_wh(self) -> int:
        """Backup Buffer capacity (includes 7% unusable)
            Returns:
                Backup Buffer in Wh
        """
        buffer_percent = self.configuration_em_usoc
        full_charge = self.battery_full_charge_capacity_wh

        return int(full_charge * buffer_percent / 100)

    @property
    @get_item(int)
    def backup_buffer_usable_capacity_wh(self) -> int:
        """Backup Buffer usable capacity (excludes 7% unusable)
            Returns:
                Usable Backup Buffer in Wh
        """
        buffer_percent = self.configuration_em_usoc
        full_charge = self.battery_full_charge_capacity_wh

        return int(full_charge * (buffer_percent - 7) / 100) if buffer_percent > 7 else 0

    @property
    def state_core_control_module(self) -> str:
        """State of control module: config, ongrid, offgrid, critical error, ...
            Returns:
                String
        """
        return self._latest_details_data[IC_STATUS][DETAIL_STATE_CORECONTROL_MODULE]

    @property
    def system_status(self) -> str:
        """System Status: Config, OnGrid, OffGrid, Critical Error, ...
            Returns:
                String
        """
        return self._status_data[STATUS_SYSTEMSTATUS]

    @property
    def system_status_timestamp(self) -> datetime.datetime:
        """Timestamp: "2024-10-09 14:00:07"
            Returns:
                datetime
        """
        print (f'{self._status_data[STATUS_TIMESTAMP]}')
        return  datetime.datetime.fromisoformat(self._status_data[STATUS_TIMESTAMP])

    @property
    def validation_timestamp(self) -> datetime.datetime:
        """Timestamp: "Wed Sep 18 12:26:06 2024"
            Returns:
                datetime
        """
        print (f'{self._latest_details_data[IC_STATUS]["timestamp"]}')
        return  datetime.datetime.strptime(self._latest_details_data[IC_STATUS]["timestamp"], '%a %b %d %H:%M:%S %Y')

    @property
    def configuration_de_software(self) -> str:
        """Software version
            Returns:
                String
        """
        if self._configurations_data == {}:
            self.fetch_configurations()

        return self._configurations_data[CONFIGURATION_DE_SOFTWARE]

    @property
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
        return self._latest_details_data[IC_STATUS][IC_ECLIPSE_LED]
