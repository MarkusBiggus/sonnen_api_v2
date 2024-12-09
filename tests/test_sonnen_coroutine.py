"""pytest tests/test_sonnen_coroutine.py -s -v -x
3. Sync update called from coroutine passed to asyncio.run_in_executor
"""
#import datetime
import os
import sys
import logging
import pytest
#import pytest_asyncio
#from pytest_mock import mocker
import asyncio
from collections.abc import (
    Callable,
)
from typing import (
    Any,
    Union,
    Dict,
)
#from asyncmock import AsyncMock
#import json

#from freezegun import freeze_time
from sonnen_api_v2 import Batterie
from dotenv import load_dotenv

from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging

load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')
BATTERIE_HOST_PORT = os.getenv('BATTERIE_HOST_PORT')

LOGGER_NAME = None # "sonnenapiv2" #


if BATTERIE_1_HOST == 'X':
    raise ValueError('Set BATTERIE_1_HOST & API_READ_TOKEN_1 in .env See env.example')

logging.getLogger("asyncio").setLevel(logging.WARNING)

if LOGGER_NAME is not None:
    filename=f'tests/logs/{LOGGER_NAME}.log'
    logging.basicConfig(filename=filename, level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(LOGGER_NAME)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler(filename=filename, mode='a')
    fh.setLevel(logging.DEBUG)
    # console handler display logs messages to console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info ('Asyncio mock data tests')


@pytest.mark.asyncio
async def test_executor_job(mocker):
    """Batterie configuration coroutine using mock data"""

    # Can't mock a coroutine!
    mocker.patch.object(Batterie, "fetch_status", __mock_status_charging)
    mocker.patch.object(Batterie, "fetch_latest_details", __mock_latest_charging)
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)
    mocker.patch.object(Batterie, "fetch_battery_status", __mock_battery)
    mocker.patch.object(Batterie, "fetch_powermeter", __mock_powermeter)
    mocker.patch.object(Batterie, "fetch_inverter_data", __mock_inverter)

    def async_add_executor_job[*_Ts, _T](
        self, target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        self.loop = asyncio.get_running_loop()
        task = self.loop.run_in_executor(None, target, *args)
    #    print (f'task type: {type(task)}')
        return task

    def test_get_status():
        """Coroutine to mock the fetch"""
        return battery.sync_get_status()

    def _test_get_latest_data():
        """Coroutine to mock the fetch"""
        return battery.sync_get_latest_data()

    def test_get_configurations():
        """Coroutine to mock the fetch"""
        return battery.sync_get_configurations()

    def _test_get_battery():
        """Coroutine to mock the fetch"""
        return battery.sync_get_battery()

    def _test_get_powermeter():
        """Coroutine to mock the fetch"""
        return battery.sync_get_powermeter()

    def _test_get_inverter():
        """Coroutine to mock the fetch"""
        return battery.sync_get_inverter()

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)


    # sync wrapped methods used by ha component called by syncio.run_in_executor

    status_data = await async_add_executor_job(mocker,
        target=test_get_status
    )
    #print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

    # latest_data = battery_charging.sync_get_latest_data()
    latest_data = await async_add_executor_job(mocker,
        target=_test_get_latest_data
    )
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Pac_total_W') == -1394

    configurations = await async_add_executor_job(mocker,
        target=test_get_configurations
    )
    #print (f'data type: {type(configurations)}')
    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20
    assert configurations.get('DepthOfDischargeLimit') == 93

    battery_info = await async_add_executor_job(mocker,
        target=_test_get_battery
    )
    assert battery_info.get('cyclecount') == 30
    assert battery_info.get('remainingcapacity') == 177.74

    assert battery_info.get('total_installed_capacity') == 20000
    assert battery_info.get('remaining_capacity') == 18200.576
    assert battery_info.get('remaining_capacity_usable') == 16752
    assert battery_info.get('backup_buffer_usable') == 2688

    #powermeter = battery_charging.sync_get_powermeter()
    powermeter = await async_add_executor_job(mocker,
        target=_test_get_powermeter
    )
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[0]['kwh_imported'] == 3969.800048828125
    assert powermeter[1]['direction'] == 'consumption'
    assert powermeter[1]['kwh_imported'] == 816.5

    #status_data = battery_charging.sync_get_inverter()
    status_data = await async_add_executor_job(mocker,
        target=_test_get_inverter
    )
    assert status_data.get('pac_total') == -1394.33
    assert status_data.get('uac') == 233.55

    # every other emulated get method
    request_connect_timeouts = battery.get_request_connect_timeouts()
    #print(f'connect_timeouts: {request_connect_timeouts}')
    assert request_connect_timeouts == (20,20)
    request_connect_timeouts = battery.set_request_connect_timeouts((15,25))
    assert request_connect_timeouts == (15,25)

    operating_mode =  battery.configuration_em_operatingmode
    operating_mode_name =  battery.configuration_em_operatingmode_name
    battery_reserve =  battery.configuration_em_usoc
    #print(f'operating_mode: {operating_mode}  name: {operating_mode_name}  battery_reserve:{battery_reserve}%')
    assert battery_reserve == 20
    assert operating_mode == 2
    assert operating_mode_name == 'Automatic - Self Consumption'