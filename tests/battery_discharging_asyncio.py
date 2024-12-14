import os
import logging
import pytest
from asyncmock import AsyncMock

from sonnen_api_v2 import Batterie
from dotenv import load_dotenv

from . mock_sonnenbatterie_v2_charging import  __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging

load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_HOST_PORT = os.getenv('BATTERIE_HOST_PORT')

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if BATTERIE_1_HOST == 'X':
    raise ValueError('Set BATTERIE_1_HOST & API_READ_TOKEN_1 in .env See env.example')

@pytest.fixture(name="battery_discharging")
async def fixture_battery_discharging(mocker) -> Batterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_discharging_asyncio test.')

    mocker.patch.object(Batterie, "async_fetch_status", AsyncMock(return_value=__mock_status_discharging()))
    mocker.patch.object(Batterie, "async_fetch_latest_details", AsyncMock(return_value=__mock_latest_discharging()))
    mocker.patch.object(Batterie, "async_fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(Batterie, "async_fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(Batterie, "async_fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(Batterie, "async_fetch_inverter", AsyncMock(return_value=__mock_inverter()))

    battery_discharging = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)
    success = await battery_discharging.async_update()
    assert success is not False

    return battery_discharging
