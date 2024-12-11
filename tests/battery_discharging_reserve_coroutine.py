import os
import logging
import pytest
import asyncio
from collections.abc import (
    Callable,
)

from sonnen_api_v2 import Batterie
from dotenv import load_dotenv

from . mock_sonnenbatterie_v2_charging import  __mock_configurations, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging_reserve import __mock_status_discharging, __mock_latest_discharging, __mock_battery_discharging

load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_HOST_PORT = os.getenv('BATTERIE_HOST_PORT')

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if BATTERIE_1_HOST == 'X':
    raise ValueError('Set BATTERIE_1_HOST & API_READ_TOKEN_1 in .env See env.example')

@pytest.fixture(name="battery_discharging_reserve")
async def fixture_battery_discharging_reserve(mocker) -> Batterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_discharging_reserve_asyncio test.')

    # Can't mock a coroutine!
    mocker.patch.object(Batterie, "fetch_status", __mock_status_discharging)
    mocker.patch.object(Batterie, "fetch_latest_details", __mock_latest_discharging)
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)
    mocker.patch.object(Batterie, "fetch_battery_status", __mock_battery_discharging)
    mocker.patch.object(Batterie, "fetch_powermeter", __mock_powermeter)
    mocker.patch.object(Batterie, "fetch_inverter_data", __mock_inverter)

    def async_add_executor_job[*_Ts, _T](
        self, target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        self.loop = asyncio.get_running_loop()
        task = self.loop.run_in_executor(None, target, *args)
        return task

    def _sync_update():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.sync_update()


    battery_discharging_reserve = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)
    success = await async_add_executor_job(mocker,
        target = _sync_update
    )
    assert success is True

    return battery_discharging_reserve
