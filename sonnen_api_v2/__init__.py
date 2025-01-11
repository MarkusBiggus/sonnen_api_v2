"""Sonnen Batterie API V2 module."""

import logging
from collections.abc import Awaitable

from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieResponse, BatterieError, BatterieAuthError, BatterieHTTPError
from .const import DEFAULT_PORT

__version__ = '0.5.13'

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

    def __init__(self, auth_token:str , ip_address:str, port=DEFAULT_PORT):
        """Initialize the API client."""

        self._battery = Batterie(auth_token, ip_address, port)
        self._attr_available = False

    def get_sensor_value(self, sensor_name:str):
        """Get sensor value by name from battery property.
            refresh_response must have been called at least once before any sensor value is retrieved.
        """

        return getattr(self._battery, sensor_name)

    async def refresh_response(self) -> Awaitable[BatterieResponse]:
        """Query the real time API."""

        success = await self._battery.async_update()

        self._attr_available = success
        if success is False:
            _LOGGER.error(f'BatterieBackup: Error updating batterie data! from: {self._battery.hostname}')
            raise BatterieError(f'BatterieBackup: Error updating batterie data! from: {self._battery.hostname}')

        return BatterieResponse(
            version = self._battery.configuration_de_software,
            last_updated = self._battery.last_updated,
            configurations = self._battery.configurations,
        )

    async def validate_token(self) -> Awaitable[BatterieResponse]:
        """Query the real time API."""

        success = await self._battery.async_validate_token()

        self._attr_available = success
        if success is not True:
            _LOGGER.error(f'BatterieBackup: Error validating API token! ({self._battery.api_token})')
            raise BatterieAuthError(f'BatterieBackup: Error validating API token! ({self._battery.api_token})')

        return BatterieResponse(
            version = self._battery.configuration_de_software,
            last_updated = self._battery.last_configurations,
            configurations = self._battery.configurations,
        )
