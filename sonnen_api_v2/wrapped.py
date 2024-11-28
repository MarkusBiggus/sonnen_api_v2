"""Methods to emulate sonnenbatterie (v1) package for sonnenbatterie_v2_api ha component"""
from typing import Union

import aiohttp
import asyncio

from .const import BATTERY_FULL_CHARGE_CAPACITY_WH, BATTERY_REMAINING_CAPACITY, BATTERY_USABLE_REMAINING_CAPACITY, BATTERY_RSOC

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
        self._latest_details_data = await self.fetch_latest_details()

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
        self._configurations_data = await self.fetch_configurations()

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
        self._status_data = await self.fetch_status()

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
        self._powermeter_data = await self.fetch_powermeter()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_powermeter(self))
    finally:
        event_loop.close()

    return self._powermeter_data if self._powermeter_data is not None else False

def get_battery(self)-> Union[str, bool]:
    """Battery status for sonnenbatterie wrapper
        Fake V1 API data used by ha sonnenbatterie component
        Returns:
            json response
    """
    async def _get_battery(self):
        self._battery_status = await self.fetch_battery_status()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_battery(self))
    finally:
        event_loop.close()

#    if self._status_data is None:
#        self.get_status()
#        if self._status_data is None:
#            return False
    if self._configurations_data is None:
        self.get_configurations()
        if self._configurations_data is None:
            return False
    """ current_state index of: ["standby", "charging", "discharging", "charged", "discharged"] """
    if self.status_battery_charging:
        self._battery_status['current_state'] = "charging"
    elif self.status_battery_discharging:
        self._battery_status['current_state'] = "discharging"
    elif self.battery_rsoc > 98:
        self._battery_status['current_state'] = "charged"
#    elif self.battery_rsoc == self.status_backup_buffer:
#        self._battery_status['current_state'] = '0'
    elif self.battery_usable_remaining_capacity < 2:
        self._battery_status['current_state'] = "discharged"
    else:
        self._battery_status['current_state'] = "standby"

    measurements = {'battery_status': {'cyclecount': self.battery_cycle_count,
                                       'stateofhealth': int(self.battery_rsoc)
                                      }
                    }
    self._battery_status['measurements'] = measurements
    self._battery_status['total_installed_capacity'] = self._configurations_data.get('IC_BatteryModules') * self._configurations_data.get('CM_MarketingModuleCapacity') #self.battery_full_charge_capacity_wh #_battery_status[BATTERY_FULL_CHARGE_CAPACITY_WH]
    self._battery_status['reserved_capacity'] = self.battery_unusable_capacity_wh #backup_buffer_capacity_wh
    self._battery_status['remaining_capacity'] = self.battery_remaining_capacity_wh #_battery_status[BATTERY_REMAINING_CAPACITY]
    self._battery_status['remaining_capacity_usable'] = self.battery_usable_remaining_capacity_wh #_battery_status[BATTERY_USABLE_REMAINING_CAPACITY]
    self._battery_status['backup_buffer_usable'] = self.backup_buffer_usable_capacity_wh

    return self._battery_status if self._battery_status is not None else False

def get_inverter(self)-> Union[str, bool]:
    """Inverter details for sonnenbatterie wrapper
        Returns:
            json response
    """
    async def _get_inverter(self):
        self._inverter_data = await self.fetch_inverter_data()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    try:
        event_loop.run_until_complete(_get_inverter(self))
    finally:
        event_loop.close()

    return self._inverter_data if self._inverter_data is not None else False

def get_batterysystem(self)-> Union[str, bool]:
    """battery_system not in V2 - fake it for required component attributes"""
    if self._configurations_data is None:
        self.get_configurations()
        if self._configurations_data is None:
            return False
    systemdata = {'modules': self._configurations_data.get('IC_BatteryModules'),
                  'battery_system': {'system': {'storage_capacity_per_module': self._configurations_data.get('CM_MarketingModuleCapacity') }}
                 }
    return systemdata
