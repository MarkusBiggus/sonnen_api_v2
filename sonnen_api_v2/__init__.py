"""Sonnen Batterie API V2 module."""

import logging
from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieResponse, BatterieError, BatterieAuthError, BatterieHTTPError

__version__ = '0.5.12'

__all__ = (
    "Batterie"
    "BatterieError",
    "BatterieAuthError",
    "BatterieHTTPError"
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
        # try:
        success = await self.battery.async_validate_token()
        # except Exception as error:
        #     raise BatterieError from error

        if success is not True:
            _LOGGER.error('BatterieBackup: Error updating batterie data!')
            raise BatterieError('BatterieBackup: Error updating batterie data!')

        return BatterieResponse(
            version = self.battery.configuration_de_software,
            last_updated = self.battery.last_configurations,
            configurations = self.battery.configurations,
#            "status": self.battery.,
#            "latestdata": self.battery.,
#            "battery": self.battery.,
#            "powermeter": self.battery.,
#            "inverter": self.battery.
        )