"""Sonnen Batterie API V2 module."""

import logging
from sonnen_api_v2 import Batterie, BatterieResponse, BatterieError, BatterieAuthError

__version__ = '1.0.0'

__all__ = (
    "Batterie"
    "BatterieError",
    "BatterieAuthError",
    "BatterieResponse",
    "BatterieBackup",
)

_LOGGER = logging.getLogger(__name__)


class BatterieBackup:
    """Sonnen Batterie real time API.

        Used by home assistant component sonnenbackup
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, auth_token:str , ip_address:str, port=None):
        """Initialize the API client."""
        self.battery = Batterie(auth_token, ip_address, port)

    async def get_response(self) -> BatterieResponse:
        """Query the real time API."""
        success = await self.battery.async_update()
        if success is False:
            _LOGGER.error('BatterieBackup: Error updating batterie data!')
            raise BatterieError('BatterieBackup: Error updating batterie data!')

        return BatterieResponse(
            serial_number = 'xXx', #comes from config entry
            version = self.battery.configuration_de_software,
            last_updated = self.battery.last_updated,
            configurations = self.battery.configurations,
#            "status": self.battery.,
#            "latestdata": self.battery.,
#            "battery": self.battery.,
#            "powermeter": self.battery.,
#            "inverter": self.battery.
        )