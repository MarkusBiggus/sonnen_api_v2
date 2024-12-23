""" SonnenBatterie API V2 module """

#import asyncio
#import logging
from .sonnen import Sonnen as Batterie, BatterieResponse, BatterieError

__version__ = '0.5.12'

__all__ = (
    "Batterie"
    "BatterieError",
    "BatterieResponse",
    "RealTimeAPI",
)

#_LOGGER = logging.getLogger(__name__)


async def real_time_api(auth_token, ip_address, port=80):
    battery = Batterie(auth_token, ip_address, port) # , return_when=asyncio.FIRST_COMPLETED)
    return RealTimeAPI(battery)


class RealTimeAPI:
    """Sonnen Batterie real time API
        Used by home assistant component
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, battery: Batterie):
        """Initialize the API client."""
        self.battery = Batterie(auth_token, ip_address, port)

    async def get_data(self) -> BatterieResponse:
        """Query the real time API"""
        success = await self.battery.async_update()) # rt_request(self.battery, 3)
        return BatterieResponse(
        "BatterieResponse": [
            "serial_number": 'xXx',
            "version": self.battery.configuration_de_software,
            "last_updated": self.battery.last_updated,
            "configurations": self.battery.configurations,
#            "status": self.battery.,
#            "latestdata": self.battery.,
#            "battery": self.battery.,
#            "powermeter": self.battery.,
#            "inverter": self.battery.
        ]
