import requests
import datetime


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
        self._latest_details_data = None
        self._status_data = None

    def fetch_latest_details(self) -> None:
        """ Fetches latest details api """
        try:
            response = requests.get(self.latest_details_api_endpoint, headers=self.header)
            self._latest_details_data = response.json()
        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)

    def fetch_status(self) -> None:
        """ Fetches status api """
        try:
            response = requests.get(self.status_api_endpoint, headers=self.header)
            self._status_data = response.json()
        except requests.ConnectionError as e:
            print('Connection error to battery system - ', e)

    def update(self) -> None:
        """ Updates data from apis of the sonnenBatterie """
        self.fetch_latest_details()
        self.fetch_status()

    @property
    def consumption_average(self) -> str:
        """Average consumption in watt
           Returns:
               average consumption in watt
        """
        return self._status_data[self.CONSUMPTION_AVG_KEY]

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
        return self._latest_details_data[self.IC_STATUS][self.MODULES_INSTALLED_KEY]

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
    def consumption(self) -> str:
        """Consumption of the household
            Returns:
                house consumption in Watt
        """
        return self._latest_details_data[self.CONSUMPTION_KEY]

    @property
    def production(self) -> str:
        """Power production of the household
            Returns:
                house production in Watt
        """
        return self._latest_details_data[self.PRODUCTION_KEY]

    @property
    def u_soc(self) -> str:
        """User state of charge
            Returns:
                User SoC in percent
        """
        return self._latest_details_data[self.USOC_KEY]

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
        return self._status_data[self.REM_CON_WH_KEY] / 2 - 2300

    @property
    def full_charge_capacity(self) -> int:
        """Full charge capacity of the battery system
            Returns:
                Capacity in Wh
        """
        return self._latest_details_data[self.FULL_CHARGE_CAPACITY_KEY]

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
        return self._latest_details_data[self.PAC_KEY]

    @property
    def charging(self) -> int:
        """Actual battery charging value
            Returns:
                Charging value in watt
        """
        if self.pac_total < -1:
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
        if self._status_data[self.GRID_FEED_IN_WATT_KEY] > 0:
            return self._status_data[self.GRID_FEED_IN_WATT_KEY]
        return 0

    @property
    def grid_out(self) -> int:
        """Actual grid out value
            Returns:
                Value in watt
        """
        if self._status_data[self.GRID_FEED_IN_WATT_KEY] < 0:
            return abs(self._status_data[self.GRID_FEED_IN_WATT_KEY])
        return 0

