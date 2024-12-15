"""pytest tests/test_batterie_asyncio.py -s -v -x
1. Async update called from an async method.
"""
#import datetime
import os
import sys
import logging
import pytest

#from freezegun import freeze_time
from sonnen_api_v2 import Batterie

from .battery_charging_asyncio import fixture_battery_charging
from .battery_discharging_asyncio import fixture_battery_discharging
from .battery_discharging_reserve_asyncio import fixture_battery_discharging_reserve

LOGGER_NAME = None # "sonnenapiv2" #

logging.getLogger("asyncio").setLevel(logging.WARNING)

if LOGGER_NAME is not None:
    filename=f'/tests/logs/{LOGGER_NAME}.log'
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
@pytest.mark.usefixtures("battery_charging", "battery_discharging", "battery_discharging_reserve")
async def test_asyncio_methods(battery_charging: Batterie, battery_discharging: Batterie, battery_discharging_reserve: Batterie) -> None:
    """Batterie asyncio using mock data"""

    status_data = await battery_charging.async_fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

    status_data = await battery_discharging.async_fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:58'
    assert status_data.get('GridFeedIn_W') == -20
    assert status_data.get('Consumption_W') == 541
    assert status_data.get('Production_W') == 102
    assert status_data.get('Pac_total_W') == 438

    status_data = await battery_discharging_reserve.async_fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:59'

    latest_data = await battery_charging.async_fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Pac_total_W') == -1394

    latest_data = await battery_charging.async_fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 102
    assert latest_data.get('Consumption_W') == 1541
    assert latest_data.get('Pac_total_W') == 1439

    configurations = await battery_charging.async_fetch_configurations()
    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20

    battery_status = await battery_charging.async_fetch_battery_status()
    assert battery_status.get('cyclecount') == 30
    assert battery_status.get('remainingcapacity') == 177.74

    powermeter = await battery_charging.async_fetch_powermeter()
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[1]['direction'] == 'consumption'

    inverter_data = await battery_charging.async_fetch_inverter()
    assert inverter_data.get('pac_total') == -1394.33
    assert inverter_data.get('uac') == 233.55

    from .check_results import check_results

    check_results(battery_charging, battery_discharging, battery_discharging_reserve)
