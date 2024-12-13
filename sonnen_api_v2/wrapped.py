"""Methods to emulate sonnenbatterie (v1) package for sonnenbatterie_v2_api ha component
    Uses sync methods called by asyncio.run_in_executor from home assistant
"""
from typing import Union, Dict

import aiohttp
import asyncio

from .const import IC_STATUS, BATTERY_UNUSABLE_RESERVE

def set_request_connect_timeouts(self, request_timeouts: tuple[int, int]):
    self.request_timeouts = request_timeouts
    self.client_timeouts = aiohttp.ClientTimeout(connect=request_timeouts[0], sock_read=request_timeouts[1])
    return self.request_timeouts

def get_request_connect_timeouts(self) -> tuple[int, int]:
    return self.request_timeouts

def get_status(self)-> Union[str, bool]:
    """Status details for sonnenbatterie wrapper
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_status(self):
        self._status_data = await self.async_fetch_status()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_status(self))
    finally:
        event_loop.close()

    return self._status_data

def sync_get_status(self)-> Union[str, bool]:
    """Status details for sonnenbatterie wrapper
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._status_data = self.fetch_status()
    return self._status_data

def get_latest_data(self)-> Union[str, bool]:
    """Latest details for sonnenbatterie wrapper
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_latest_data(self):
        self._latest_details_data = None
        self._latest_details_data = await self.async_fetch_latest_details()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_latest_data(self))
    finally:
        event_loop.close()
    return _aug_latest_details(self)

def sync_get_latest_data(self)-> Union[str, bool]:
    """Latest details for sonnenbatterie wrapper
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._latest_details_data = None
    self._latest_details_data = self.fetch_latest_details()
    return _aug_latest_details(self)

def _aug_latest_details(self):
    """Augment latest_details for sonnenbatterie wrapper
        Returns:
            json response
    """
    if self._latest_details_data is not None:
        self._ic_status = self._latest_details_data[IC_STATUS]  # noqa: F405
    else:
        self._ic_status = None
    return self._latest_details_data

def get_configurations(self)-> Union[str, bool]:
    """Configuration details for sonnenbatterie wrapper
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_configurations(self):
        self._configurations_data = None
        self._configurations_data = await self.async_fetch_configurations()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_configurations(self))
    finally:
        event_loop.close()

    return _aug_configurations(self)

def sync_get_configurations(self)-> Union[str, bool]:
    """Configuration details for sonnenbatterie wrapper
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._configurations_data = None
    self._configurations_data = self.fetch_configurations()
    return _aug_configurations(self)

def _aug_configurations(self):
    """Augment Configurations for sonnenbatterie wrapper
        Returns:
            json response
    """
    if self._configurations_data is not None:
        self._configurations_data['DepthOfDischargeLimit'] = int((1 - BATTERY_UNUSABLE_RESERVE) * 100)
    return self._configurations_data

def get_battery(self)-> Union[Dict, bool]:
    """Battery status for sonnenbatterie wrapper
        Fake V1 API data used by ha sonnenbatterie component
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_battery(self):
        self._battery_status = None
        self._battery_status = await self.async_fetch_battery_status()
        if self._configurations_data is None:
            self._configurations_data = await self.async_fetch_configurations()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_battery(self))
    finally:
        event_loop.close()

    if self._battery_status is None:
        return None

    return _aug_battery(self)

def sync_get_battery(self)-> Union[Dict, bool]:
    """Battery status for sonnenbatterie wrapper
        Fake V1 API data used by ha sonnenbatterie component
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._battery_status = None
    self._battery_status = self.fetch_battery_status()
    if self._battery_status is None:
        return None

    if self._configurations_data is None:
        self._configurations_data = self.sync_get_configurations()

    return _aug_battery(self)

def _aug_battery(self):
    """Augment Battery status for sonnenbatterie wrapper
        Fake V1 API data used by ha sonnenbatterie component
        Returns:
            json response
    """
    if self._configurations_data is None:
        self._battery_status['total_installed_capacity'] = 0
    else:
        self._battery_status['total_installed_capacity'] = int(self._configurations_data.get('IC_BatteryModules')) * int(self._configurations_data.get('CM_MarketingModuleCapacity'))

    self._battery_status['reserved_capacity'] = self.battery_unusable_capacity_wh
    self._battery_status['remaining_capacity'] = self.battery_remaining_capacity_wh
    self._battery_status['remaining_capacity_usable'] = self.battery_usable_remaining_capacity_wh
    self._battery_status['backup_buffer_usable'] = self.backup_buffer_usable_capacity_wh
    return self._battery_status


def get_powermeter(self)-> Union[str, bool]:
    """powermeter details for sonnenbatterie wrapper
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_powermeter(self):
        self._powermeter_data = await self.async_fetch_powermeter()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_powermeter(self))
    finally:
        event_loop.close()

    if self._powermeter_data is not None:
        self._powermeter_production = self._powermeter_data[0]
        self._powermeter_consumption = self._powermeter_data[1]
    else:
        self._powermeter_production = None
        self._powermeter_consumption = None

    return self._powermeter_data

def sync_get_powermeter(self)-> Union[str, bool]:
    """powermeter details for sonnenbatterie wrapper
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._powermeter_data = self.fetch_powermeter()
    if self._powermeter_data is not None:
        self._powermeter_production = self._powermeter_data[0]
        self._powermeter_consumption = self._powermeter_data[1]
    else:
        self._powermeter_production = None
        self._powermeter_consumption = None
    return self._powermeter_data

def get_inverter(self)-> Union[str, bool]:
    """Inverter details for sonnenbatterie wrapper
        for Sync caller with Async fetch
        Returns:
            json response
    """
    async def _get_inverter(self):
        self._inverter_data = await self.async_fetch_inverter()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_inverter(self))
    finally:
        event_loop.close()

    return self._inverter_data

def sync_get_inverter(self)-> Union[str, bool]:
    """Inverter details for sonnenbatterie wrapper
        for Sync caller with Sync fetch
        Returns:
            json response
    """
    self._inverter_data = self.fetch_inverter()
    return self._inverter_data
