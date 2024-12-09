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
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)

    def async_add_executor_job[*_Ts, _T](
        self, target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        self.loop = asyncio.get_running_loop()
        task = self.loop.run_in_executor(None, target, *args)
        print (f'task type: {type(task)}')
        return task

    def test_get_configurations():
        """Coroutine to mock the fetch"""
        return battery.sync_get_configurations()
#        return battery.fetch_configurations

    def test_get_status():
        """Coroutine to mock the fetch"""
        return battery.sync_get_status()

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)

    configurations = await async_add_executor_job(mocker,
        target=test_get_configurations
    )
    print (f'data type: {type(configurations)}')

    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20
    # sync wrapped methods used by ha component called by syncio.async_add_executor_job
    status_data = await async_add_executor_job(mocker,
        target=test_get_status
    )
    #print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == 54
    assert status_data.get('Consumption_W') == 403
    assert status_data.get('Production_W') == 578
    assert status_data.get('Pac_total_W') == -95

    # latest_data = battery_charging.sync_get_latest_data()
    # assert latest_data.get('GridFeedIn_W') == 0
    # assert latest_data.get('Production_W') == 2972
    # assert latest_data.get('Consumption_W') == 1578
    # assert latest_data.get('Pac_total_W') == -1394

    # powermeter = battery_charging.sync_get_powermeter()
    # assert powermeter[0]['direction'] == 'production'
    # assert powermeter[1]['direction'] == 'consumption'

    # status_data =  battery_charging.sync_get_battery()
    # assert status_data.get('cyclecount') == 30
    # assert status_data.get('remainingcapacity') == 177.74

    # status_data = battery_charging.sync_get_inverter()
    # assert status_data.get('pac_total') == -1394.33
    # assert status_data.get('uac') == 233.55

    # configuratons = battery_charging.sync_get_configurations()
    # assert configuratons.get('DE_Software') == '1.14.5'
    # assert configuratons.get('EM_USOC') == 20
