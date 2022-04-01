import requests
import datetime


def get_item(func):
    def inner(*args):
        key = args[1]
        try:
            result = func(*args)
        except KeyError:
            print(f'{key} key not found')
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

    def fetch_latest_details(self) -> bool:
        """ Fetches latest details api """
        try:
            response = requests.get(self.latest_details_api_endpoint, headers=self.header)
            self._latest_details_data = response.json()
            self._latest_details_data = self._latest_details_data.get(self.IC_STATUS)
            return True
        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)
            return False

    def fetch_status(self) -> bool:
        """ Fetches status api """
        try:
            response = requests.get(self.status_api_endpoint, headers=self.header)
            self._status_data = response.json()
            return True
        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)
            return False

    def update(self) -> None:
        """ Updates data from apis of the sonnenBatterie """
        self.fetch_latest_details()
        self.fetch_status()

    @get_item
    def consumption_average(self, key) -> int:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """
        return self.status_data[key]

    @property
    def consumption_average_test(self) -> int:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """
        consumption = self._get_item(self.status_data, self.CONSUMPTION_AVG_KEY)
        if consumption:
            return int(consumption)
        return 0

    @property
    def time_to_empty(self) -> datetime.timedelta:
        """Time until battery discharged
            Returns:
                Time in string format HH MM
        """
        seconds = int((self.remaining_capacity_wh / self.discharging) * 3600) if self.discharging else 0

        return datetime.timedelta(seconds=seconds)

    @property
    def fully_discharged_at(self) -> datetime:
        """Future time of battery fully discharged
            Returns:
                Future time
        """
        return (datetime.datetime.now() + self.time_to_empty).strftime('%d.%B %H:%M')

    @property
    def seconds_since_full(self) -> int:
        """Seconds passed since full charge
            Returns:
                seconds as integer
        """
        return self._latest_details_data[self.IC_STATUS][self.SECONDS_SINCE_FULL_KEY]

    @property
    def installed_modules(self) -> int:
        """Battery modules installed in the system
            Returns:
                Number of modules
        """
        modules = self._ic_status.get(self.MODULES_INSTALLED_KEY)
        if modules:
            return int(modules)
        return 0

    @property
    def time_since_full(self) -> datetime.timedelta:
        """Calculates time since full charge.
           Returns:
               Time in format days hours minutes seconds
        """
        return datetime.timedelta(seconds=self.seconds_since_full)

    @property
    def latest_details_data(self) -> dict:
        """Latest details data dict saved from the battery api
            Returns:
                last dictionary data saved
        """
        return self._latest_details_data

    @property
    def status_data(self) -> dict:
        """Latest status data dict saved from the battery api
            Returns:
                last dictionary data saved
        """
        return self._status_data

    @property
    def consumption(self) -> int:
        """Consumption of the household
            Returns:
                house consumption in Watt
        """
        consumption = self.latest_details_data.get(self.CONSUMPTION_KEY)
        if consumption:
            return int(consumption)
        return 0

    @property
    def production(self) -> int:
        """Power production of the household
            Returns:
                house production in Watt
        """
        production = self.latest_details_data.get(self.PRODUCTION_KEY)
        if production:
            return int(production)
        return 0

    @property
    def u_soc(self) -> int:
        """User state of charge
            Returns:
                User SoC in percent
        """
        user_soc = self.latest_details_data.get(self.USOC_KEY)
        if user_soc:
            return int(user_soc)
        return 0

    @property
    def remaining_capacity_wh(self) -> int:
        """ Remaining capacity in watt hours
            IMPORTANT NOTE: it seems that sonnen_api_v2 have made a mistake
            in the API. The value should be the half.
            I have made the simple division hack here
            2300W reserve is removed as well
            Returns:
                 Remaining USABLE capacity of the battery in Wh
        """
        remaining = self.status_data.get(self.REM_CON_WH_KEY)
        if remaining:
            return int(remaining / 2 - 2300)
        return 0

    @property
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery system
            Returns:
                Capacity in Wh
        """
        capacity = self.latest_details_data.get(self.FULL_CHARGE_CAPACITY_KEY)
        if capacity:
            return int(capacity)
        return 0

    @property
    def time_remaining_to_fully_charged(self) -> datetime.timedelta:
        """Time remaining until fully charged
            Returns:
                Time in HH MM format
        """
        remaining_charge = self.full_charge_capacity - self.remaining_capacity_wh
        seconds = int((remaining_charge / self.charging) * 3600) if self.charging else 0
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
        pac = self.latest_details_data.get(self.PAC_KEY)
        return int(pac) if pac else 0

    @property
    def charging(self) -> int:
        """Actual battery charging value
            Returns:
                Charging value in watt
        """
        if self.pac_total < 0:
            return abs(self.pac_total)
        return 0

    @property
    def discharging(self) -> int:
        """Actual battery discharging value
            Returns:
                Discharging value in watt
        """
        if self.pac_total > 0:
            return abs(self.pac_total)
        return 0

    @property
    def grid_in(self) -> int:
        """Actual grid feed in value
            Returns:
                Value in watt
        """
        grid_in = self.status_data.get(self.GRID_FEED_IN_WATT_KEY)
        if grid_in:
            grid_in = int(grid_in)
            if grid_in > 0:
                return grid_in
        return 0

    @property
    def grid_out(self) -> int:
        """Actual grid out value
            Returns:
                Value in watt
        """
        grid_out = self.status_data.get(self.GRID_FEED_IN_WATT_KEY)
        if grid_out:
            grid_out = int(grid_out)
            if grid_out < 0:
                return int(abs(grid_out))
        return 0

