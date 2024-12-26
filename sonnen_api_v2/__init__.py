"""Sonnen Batterie API V2 module."""

import datetime
import logging
from sonnen_api_v2 import Batterie, BatterieResponse, BatterieError, BatterieAuthError
from sonnen_api_v2.const import CONFIGURATION_DE_SOFTWARE

__version__ = '0.5.12'

__all__ = (
    "Batterie"
    "BatterieError",
    "BatterieAuthError",
    "BatterieResponse",
    "SonnenBatterie",
)

_LOGGER = logging.getLogger(__name__)


class SonnenBatterie:
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
            _LOGGER.error('SonnenBatterie: Error updating batterie data!')
            raise BatterieError('SonnenBatterie: Error updating batterie data!')

        return BatterieResponse(
            version = self.battery.configuration_de_software,
            last_updated = self.battery.last_updated,
            configurations = self.battery.configurations,
#            "status": self.battery.,
#            "latestdata": self.battery.,
#            "battery": self.battery.,
#            "powermeter": self.battery.,
#            "inverter": self.battery.
        )

    async def validate_token(self) -> BatterieResponse:
        """Query the real time API."""

        configurations = await self.battery.async_fetch_configurations()
        if configurations is None:
            _LOGGER.error('SonnenBatterie: Error updating batterie data!')
            raise BatterieError('SonnenBatterie: Error updating batterie data!')

        return BatterieResponse(
            version = configurations[CONFIGURATION_DE_SOFTWARE],
            last_updated = self.battery.last_configurations,
            configurations = configurations,
#            "status": self.battery.,
#            "latestdata": self.battery.,
#            "battery": self.battery.,
#            "powermeter": self.battery.,
#            "inverter": self.battery.
        )