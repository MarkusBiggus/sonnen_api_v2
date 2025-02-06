import os
import logging
import pytest
from freezegun import freeze_time
import asyncio
from collections.abc import (
    Callable,
)

from sonnen_api_v2 import Batterie

from . mock_sonnenbatterie_v2_charging import __mock_configurations, __mock_powermeter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging, __mock_battery_discharging, __mock_inverter_discharging

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(name="battery_discharging")
@freeze_time("20-11-2023 17:00:55") # discharging time
async def fixture_battery_discharging(mocker) -> Batterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_discharging_asyncio test.')

    # Can't mock a coroutine!
    mocker.patch.object(Batterie, "fetch_status", __mock_status_discharging)
    mocker.patch.object(Batterie, "fetch_latest_details", __mock_latest_discharging)
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)
    mocker.patch.object(Batterie, "fetch_battery_status", __mock_battery_discharging)
    mocker.patch.object(Batterie, "fetch_powermeter", __mock_powermeter)
    mocker.patch.object(Batterie, "fetch_inverter", __mock_inverter_discharging)

    def async_add_executor_job[*_Ts, _T](
        target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        loop = asyncio.get_running_loop()
        task = loop.run_in_executor(None, target, *args)
    #    print (f'task type: {type(task)}')
        return task

    def _sync_update(battery_discharging: Batterie) -> bool:
        """Coroutine to sync fetch"""
        return battery_discharging.sync_get_update()


    battery_discharging = Batterie('fakeToken', 'fakeHost')

    success = await async_add_executor_job(
        _sync_update, battery_discharging
    )
    assert success is not False

    return battery_discharging
