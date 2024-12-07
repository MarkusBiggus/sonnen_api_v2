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
    battery = await Batterie(auth_token, ip_address, port) # , return_when=asyncio.FIRST_COMPLETED)
    return RealTimeAPI(battery)


class RealTimeAPI:
    """Sonnen Batterie real time API
        Used by home assistant component
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, battery: Batterie):
        """Initialize the API client."""
        self.battery = battery

    async def get_data(self) -> BatterieResponse:
        """Query the real time API"""
        return await self.battery.get_data() # rt_request(self.battery, 3)
