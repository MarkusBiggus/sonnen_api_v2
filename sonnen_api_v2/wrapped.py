from typing import Union

__all__ = [
    "set_request_connect_timeouts",
    "get_request_connect_timeouts",
    "get_latest_data",
    "get_configurations",
    "get_status"
    ]
#class wrapped:
#    """ sonnenbatterie_api_v2 wrapper support functions """

#    def __init__(self) -> None:
#        return

def set_request_connect_timeouts(self, request_timeouts: tuple[int, int]):
    self.request_timeouts = request_timeouts

def get_request_connect_timeouts(self) -> tuple[int, int]:
    return self.request_timeouts

def get_latest_data(self)-> Union[str, bool]:

    """Latest details for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_latest_details()
    if not success:
        return success

    return self._latest_details_data

def get_configurations(self)-> Union[str, bool]:
    """Configuration details for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_configurations()
    if not success:
        return success

    return self._configurations_data

def get_status(self)-> Union[str, bool]:
    """Status details for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_status()
    if not success:
        return success

    return self._status_data

def get_powermeter(self)-> Union[str, bool]:
    """powermeter details for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_powermeter()
    if not success:
        return success

    return self._powermeter_data

def get_battery(self)-> Union[str, bool]:
    """Battery status for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_battery_status()
    if not success:
        return success

    return self._battery_status

def get_inverter(self)-> Union[str, bool]:
    """Inverter details for sonnenbatterie wrapper
        Returns:
            json response
    """
    success = self.fetch_inverter_data()
    if not success:
        return success

    return self._inverter_data
