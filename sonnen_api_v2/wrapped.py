from typing import Union

import aiohttp
import asyncio

__all__ = [
    "set_request_connect_timeouts",
    "get_request_connect_timeouts",
    "get_latest_data",
    "get_configurations",
    "get_status"
    ]

def set_request_connect_timeouts(self, request_timeouts: tuple[int, int]):
    self.request_timeouts = request_timeouts
    self.client_timeouts = aiohttp.ClientTimeout(connect=request_timeouts[0], sock_read=request_timeouts[1])

def get_request_connect_timeouts(self) -> tuple[int, int]:
    return self.request_timeouts

def get_latest_data(self)-> Union[str, bool]:

    """Latest details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_latest_data(self):
        await self.fetch_latest_details()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_latest_data(self))
    finally:
        event_loop.close()

    return self._latest_details_data if self._latest_details_data is not None else False

def get_configurations(self)-> Union[str, bool]:
    """Configuration details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_configurations(self):
        await self.fetch_configurations()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_configurations(self))
    finally:
        event_loop.close()

    return self._configurations_data if self._configurations_data is not None else False

def get_status(self)-> Union[str, bool]:
    """Status details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_status(self):
        await self.fetch_status()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_status(self))
    finally:
        event_loop.close()

    return self._status_data if self._status_data is not None else False

def get_powermeter(self)-> Union[str, bool]:
    """powermeter details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_powermeter(self):
        await self.fetch_powermeter()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_powermeter(self))
    finally:
        event_loop.close()

    return self._powermeter_data if self._powermeter_data is not None else False

def get_battery(self)-> Union[str, bool]:
    """Battery status for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_battery(self):
        await self.fetch_battery_status()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_battery(self))
    finally:
        event_loop.close()

    return self._battery_status if self._battery_status is not None else False

def get_inverter(self)-> Union[str, bool]:
    """Inverter details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_inverter(self):
        await self.fetch_inverter_data()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_inverter(self))
    finally:
        event_loop.close()

    return self._inverter_data if self._inverter_data is not None else False
