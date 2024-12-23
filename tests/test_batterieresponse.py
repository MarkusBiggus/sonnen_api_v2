"""pytest tests/test_batterieresponse.py -s -v -x
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
    logger.info ('Response for HA mock data tests')


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
async def test_batterieresponse(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    status_data = await battery_charging.async_fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2023-11-20 17:00:55'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

    response = battery_charging.async_fetch_status()