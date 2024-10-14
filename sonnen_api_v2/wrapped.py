class wrapped:
    """ sonnenbatterie_api_v2 wrapper support functions """

    def __init__(self) -> None:
        return

    def set_request_connect_timeouts(self, request_timeouts: tuple[int, int]):
        self.request_timeouts = request_timeouts

    def get_request_connect_timeouts(self):
        return self.request_timeouts

    def get_latest_data(self):
        """Latest details for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_latest_details()
        return self._latest_details_data

    def get_configurations(self):
        """Configuration details for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_configurations()
        return self._configurations_data

    def get_status(self):
        """Status details for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_status()
        return self._status_data

    def get_powermeter(self):
        """powermeter details for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_powermeter()
        return self._powermeter_data

    def get_battery(self):
        """Battery status for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_battery_status()
        return self._battery_status

    def get_inverter(self):
        """Battery status for sonnenbatterie wrapper
            Returns:
                json response
        """
        self.fetch_inverter_data()
        return self._inverter_data
