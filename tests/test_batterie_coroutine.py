"""pytest tests/test_battery_coroutine.py -s -v -x
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

#from freezegun import freeze_time
from sonnen_api_v2 import Batterie

from .battery_charging_coroutine import fixture_battery_charging
from .battery_discharging_coroutine import fixture_battery_discharging
from .battery_discharging_reserve_coroutine import fixture_battery_discharging_reserve

LOGGER_NAME = None # "sonnenapiv2" #

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
    logger.info ('Coroutine mock data tests')


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging", "battery_discharging", "battery_discharging_reserve")
async def test_coroutine_methods(battery_charging: Batterie, battery_discharging: Batterie, battery_discharging_reserve: Batterie) -> None:
    """Batterie coroutines using mock data"""

    def async_add_executor_job[*_Ts, _T](
        target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        loop = asyncio.get_running_loop()
        task = loop.run_in_executor(None, target, *args)
        return task

    def _test_get_status():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_status()

    def _test_get_latest_data():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_latest_data()

    def test_get_configurations():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_configurations()

    def _test_get_battery():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_battery()

    def _test_get_powermeter():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_powermeter()

    def _test_get_inverter():
        """Coroutine to sync fetch"""
        return battery_charging.sync_get_inverter()


    # sync wrapped methods used by ha component called by syncio.run_in_executor

    status_data = await async_add_executor_job(
        target=_test_get_status
    )
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

    latest_data = await async_add_executor_job(
        target=_test_get_latest_data
    )
    assert latest_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Pac_total_W') == -1394

    configurations = await async_add_executor_job(
        target=test_get_configurations
    )
    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20
    assert configurations.get('DepthOfDischargeLimit') == 93

    battery_status = await async_add_executor_job(
        target=_test_get_battery
    )
    assert battery_status.get('cyclecount') == 30
    assert battery_status.get('remainingcapacity') == 177.74

    assert battery_status.get('total_installed_capacity') == 20000
    assert battery_status.get('remaining_capacity') == 18200.576
    assert battery_status.get('remaining_capacity_usable') == 16752
    assert battery_status.get('backup_buffer_usable') == 2688

    powermeter = await async_add_executor_job(
        target=_test_get_powermeter
    )
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[0]['kwh_imported'] == 3969.800048828125
    assert powermeter[1]['direction'] == 'consumption'
    assert powermeter[1]['kwh_imported'] == 816.5

    inverter_data = await async_add_executor_job(
        target=_test_get_inverter
    )
    assert inverter_data.get('pac_total') == -1394.33
    assert inverter_data.get('uac') == 233.55

    # every other emulated get method
    request_connect_timeouts = battery_charging.get_request_connect_timeouts()
    #print(f'connect_timeouts: {request_connect_timeouts}')
    assert request_connect_timeouts == (20,20)
    request_connect_timeouts = battery_charging.set_request_connect_timeouts((15,25))
    assert request_connect_timeouts == (15,25)

    operating_mode =  battery_charging.configuration_em_operatingmode
    operating_mode_name =  battery_charging.configuration_em_operatingmode_name
    battery_reserve =  battery_charging.configuration_em_usoc
    #print(f'operating_mode: {operating_mode}  name: {operating_mode_name}  battery_reserve:{battery_reserve}%')
    assert battery_reserve == 20
    assert operating_mode == 2
    assert operating_mode_name == 'Automatic - Self Consumption'

    from .check_results import check_results

    check_results(battery_charging, battery_discharging, battery_discharging_reserve)
