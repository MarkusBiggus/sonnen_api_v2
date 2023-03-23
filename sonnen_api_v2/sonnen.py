""" SonnenAPI v2 module """

import functools

import datetime
import requests


def get_item(func):
    """ Decorator for getting json data from Sonnen API """
    @functools.wraps(func)
    def inner(*args):
        try:
            result = func(*args)
        except KeyError:
            print(f'{func} key not found')
            result = None
        return int(result) if result else 0
    return inner


class Sonnen:
    """Class for managing Sonnen API data"""
    # API Groups
    IC_STATUS = 'ic_status'

    # API Item keys
    CONSUMPTION_KEY = 'Consumption_W'
    PRODUCTION_KEY = 'Production_W'
    GRID_FEED_IN_WATT_KEY = 'GridFeedIn_W'
    USOC_KEY = 'USOC'
    RSOC_KEY = 'RSOC'
    BATTERY_CHARGE_OUTPUT_KEY = 'Apparent_output'
    REM_CON_WH_KEY = 'RemainingCapacity_Wh'
    PAC_KEY = 'Pac_total_W'
    SECONDS_SINCE_FULL_KEY = 'secondssincefullcharge'
    MODULES_INSTALLED_KEY = 'nrbatterymodules'
    CONSUMPTION_AVG_KEY = 'Consumption_Avg'
    FULL_CHARGE_CAPACITY_KEY = 'FullChargeCapacity'
    BATTERY_CYCLE_COUNT = 'cyclecount'
    BATTERY_FULL_CHARGE_CAPACITY = 'fullchargecapacity'
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
    BATTERY_REMAINING_CAPACITY = 'remainingcapacity'
    BATTERY_SYSTEM_CURRENT = 'systemcurrent'
    BATTERY_SYSTEM_VOLTAGE = 'systemdcvoltage'

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

        # api data
        self._latest_details_data = {}
        self._status_data = {}
        self._ic_status = {}
        self._battery_status = {}

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
        return success

    @get_item
    def consumption(self) -> int:
        """Consumption of the household
            Returns:
                house consumption in Watt
        """
        return self._latest_details_data[self.CONSUMPTION_KEY]

    @get_item
    def consumption_average(self) -> int:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """

        return self._status_data[self.CONSUMPTION_AVG_KEY]

    @get_item
    def production(self) -> int:
        """Power production of the household
            Returns:
                house production in Watt
        """
        return self._latest_details_data[self.PRODUCTION_KEY]

    def seconds_to_empty(self) -> int:
        """Time until battery discharged
            Returns:
                Time in seconds
        """
        seconds = int((self.remaining_capacity_wh() / self.discharging()) * 3600) if self.discharging() else 0

        return seconds

    def fully_discharged_at(self) -> datetime:
        """Future time of battery fully discharged
            Returns:
                Future time
        """
        if self.discharging():
            return (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_to_empty())).strftime('%d.%B %H:%M')
        return '00:00'

    @get_item
    def seconds_since_full(self) -> int:
        """Seconds passed since full charge
            Returns:
                seconds as integer
        """
        return self._latest_details_data[self.IC_STATUS][self.SECONDS_SINCE_FULL_KEY]

    @get_item
    def installed_modules(self) -> int:
        """Battery modules installed in the system
            Returns:
                Number of modules
        """
        return self._ic_status[self.MODULES_INSTALLED_KEY]

    @get_item
    def u_soc(self) -> int:
        """User state of charge
            Returns:
                User SoC in percent
        """
        return self._latest_details_data[self.USOC_KEY]

    @get_item
    def remaining_capacity_wh(self) -> int:
        """ Remaining capacity in watt hours
            IMPORTANT NOTE: Why is this double as high as it should be???
            Returns:
                 Remaining USABLE capacity of the battery in Wh
        """
        return self._status_data[self.REM_CON_WH_KEY] - 22000

    @get_item
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery system
            Returns:
                Capacity in Wh
        """
        return self._latest_details_data[self.FULL_CHARGE_CAPACITY_KEY]

    def time_since_full(self) -> datetime.timedelta:
        """Calculates time since full charge.
           Returns:
               Time in format days hours minutes seconds
        """
        return datetime.timedelta(seconds=self.seconds_since_full())

    @get_item
    def seconds_remaining_to_fully_charged(self) -> int:
        """Time remaining until fully charged
            Returns:
                Time in seconds
        """
        remaining_charge = self.full_charge_capacity() - self.remaining_capacity_wh()
        if self.charging():
            return int(remaining_charge / self.charging()) * 3600
        return 0

    def fully_charged_at(self) -> datetime:
        """ Calculating time until fully charged """
        if self.charging():
            final_time = (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds_remaining_to_fully_charged()))
            return final_time.strftime('%d.%B.%Y %H:%M')
        return 0

    @property
    def pac_total(self) -> int:
        """ Battery inverter load
            Negative if charging
            Positive if discharging
            Returns:
                  Inverter load value in watt
        """
        pac = self._latest_details_data.get(self.PAC_KEY)
        return int(pac) if pac else 0

    @get_item
    def charging(self) -> int:
        """Actual battery charging value
            Returns:
                Charging value in watt
        """
        if self.pac_total < 0:
            return abs(self.pac_total)
        return 0

    @get_item
    def discharging(self) -> int:
        """Actual battery discharging value
            Returns:
                Discharging value in watt
        """
        if self.pac_total > 0:
            return self.pac_total
        return 0

    @get_item
    def grid_in(self) -> int:
        """Actual grid feed in value
            Returns:
                Value in watt
        """
        if self._status_data[self.GRID_FEED_IN_WATT_KEY] > 0:
            return self._status_data[self.GRID_FEED_IN_WATT_KEY]
        return 0

    @get_item
    def grid_out(self) -> int:
        """Actual grid out value
            Returns:
                Value in watt
        """

        if self._status_data[self.GRID_FEED_IN_WATT_KEY] < 0:
            return abs(self._status_data[self.GRID_FEED_IN_WATT_KEY])
        return 0

    @get_item
    def battery_cycle_count(self) -> int:
        """Number of charge/discharge cycles
            Returns:
                Number of charge/discharge cycles
        """
        return self._battery_status[self.BATTERY_CYCLE_COUNT]

    @get_item
    def battery_full_charge_capacity(self) -> float:
        """Fullcharge capacity
            Returns:
                Fullcharge capacity in Ah
        """
        return self._battery_status[self.BATTERY_FULL_CHARGE_CAPACITY]

    @get_item
    def battery_max_cell_temp(self) -> float:
        """Max cell temperature
            Returns:
                Maximum cell temperature in ºC
        """
        return self._battery_status[self.BATTERY_MAX_CELL_TEMP]

    @get_item
    def battery_max_cell_voltage(self) -> float:
        """Max cell voltage
            Returns:
                Maximum cell voltage in Volt
        """
        return self._battery_status[self.BATTERY_MAX_CELL_VOLTAGE]

    @get_item
    def battery_max_module_current(self) -> float:
        """Max module DC current
            Returns:
                Maximum module DC current in Ampere
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_CURRENT]

    @get_item
    def battery_max_module_voltage(self) -> float:
        """Max module DC voltage
            Returns:
                Maximum module DC voltage in Volt
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_VOLTAGE]

    @get_item
    def battery_max_module_temp(self) -> float:
        """Max module DC temperature
            Returns:
                Maximum module DC temperature in ºC
        """
        return self._battery_status[self.BATTERY_MAX_MODULE_TEMP]

    @get_item
    def battery_min_cell_temp(self) -> float:
        """Min cell temperature
            Returns:
                Minimum cell temperature in ºC
        """
        return self._battery_status[self.BATTERY_MIN_CELL_TEMP]

    @get_item
    def battery_min_cell_voltage(self) -> float:
        """Min cell voltage
            Returns:
                Minimum cell voltage in Volt
        """
        return self._battery_status[self.BATTERY_MIN_CELL_VOLTAGE]

    @get_item
    def battery_min_module_current(self) -> float:
        """Min module DC current
            Returns:
                Minimum module DC current in Ampere
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_CURRENT]

    @get_item
    def battery_min_module_voltage(self) -> float:
        """Min module DC voltage
            Returns:
                Minimum module DC voltage in Volt
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_VOLTAGE]

    @get_item
    def battery_min_module_temp(self) -> float:
        """Min module DC temperature
            Returns:
                Minimum module DC temperature in ºC
        """
        return self._battery_status[self.BATTERY_MIN_MODULE_TEMP]

    @get_item
    def battery_rsoc(self) -> float:
        """Relative state of charge
            Returns:
                Relative state of charge in %
        """
        return self._battery_status[self.BATTERY_RSOC]

    @get_item
    def battery_remaining_capacity(self) -> float:
        """Remaining capacity
            Returns:
                Remaining capacity in Ah
        """
        return self._battery_status[self.BATTERY_REMAINING_CAPACITY]

    @get_item
    def battery_system_current(self) -> float:
        """System current
            Returns:
                System current in Ampere
        """
        return self._battery_status[self.BATTERY_SYSTEM_CURRENT]

    @get_item
    def battery_system_dc_voltage(self) -> float:
        """System battery voltage
            Returns:
                Voltage in Volt
        """
        return self._battery_status[self.BATTERY_SYSTEM_VOLTAGE]
