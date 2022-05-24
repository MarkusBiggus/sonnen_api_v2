import requests
import datetime


def get_item(func):
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
    TIMEOUT = 5

    def __init__(self, auth_token: str, ip: str):
        self.ip = ip
        self.auth_token = auth_token
        self.url = f'http://{ip}'
        self.header = {'Auth-Token': self.auth_token}

        # read api endpoints
        self.status_api_endpoint = f'{self.url}/api/v2/status'
        self.latest_details_api_endpoint = f'{self.url}/api/v2/latestdata'

        # api data
        self._latest_details_data = {}
        self._status_data = {}
        self._ic_status = {}

    def fetch_latest_details(self) -> None:
        """ Fetches latest details api """
        try:
            response = requests.get(self.latest_details_api_endpoint, headers=self.header, timeout=self.TIMEOUT)
            if response.status_code == 200:
                self._latest_details_data = response.json()
                self._ic_status = self._latest_details_data[self.IC_STATUS]

        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)

    def fetch_status(self) -> None:
        """ Fetches status api """
        try:
            response = requests.get(self.status_api_endpoint, headers=self.header, timeout=self.TIMEOUT)
            if response.status_code == 200:
                self._status_data = response.json()
        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)

    def update(self) -> None:
        """ Updates data from apis of the sonnenBatterie """
        self.fetch_latest_details()
        self.fetch_status()

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
        return self._status_data[self.REM_CON_WH_KEY]

    @get_item
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery system
            Returns:
                Capacity in Wh
        """
        return self._latest_details_data[self.FULL_CHARGE_CAPACITY_KEY]

    @property
    def time_since_full(self) -> datetime.timedelta:
        """Calculates time since full charge.
           Returns:
               Time in format days hours minutes seconds
        """
        return datetime.timedelta(seconds=self.seconds_since_full())

    @property
    def time_remaining_to_fully_charged(self) -> datetime.timedelta:
        """Time remaining until fully charged
            Returns:
                Time in HH MM format
        """
        remaining_charge = self.full_charge_capacity() - self.remaining_capacity_wh()
        seconds = int((remaining_charge / self.charging()) * 3600) if self.charging else 0
        return datetime.timedelta(seconds=seconds)

    @property
    def fully_charged_at(self) -> datetime:
        return (datetime.datetime.now() + self.time_remaining_to_fully_charged).strftime('%d.%B %H:%M')

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

