"""pytest tests/test_sonnen_asyncio.py -s -v -x
"""
import datetime
import os
import sys

#from typing import Coroutine, Generator, Union
import logging
import pytest
import pytest_asyncio
from pytest_mock import mocker
from asyncmock import AsyncMock
import json


#from freezegun import freeze_time
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv


load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')

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

def status_charging()-> json:
    test_data_status_charging = {
        'Apparent_output': 98,
        'BackupBuffer': '0',
        'BatteryCharging': True,
        'BatteryDischarging': False,
        'Consumption_Avg': 486,
        'Consumption_W': 403,
        'Fac': 50.05781555175781,
        'FlowConsumptionBattery': False,
        'FlowConsumptionGrid': False,
        'FlowConsumptionProduction': True,
        'FlowGridBattery': False,
        'FlowProductionBattery': True,
        'FlowProductionGrid': True,
        'GridFeedIn_W': 54,
        'IsSystemInstalled': 1,
        'OperatingMode': '2',
        'Pac_total_W': -95,
        'Production_W': 578,
        'RSOC': 98,
        'RemainingCapacity_Wh': 68781,
        'Sac1': 98,
        'Sac2': None,
        'Sac3': None,
        'SystemStatus': 'OnGrid',
        'Timestamp': '2022-04-30 17:00:58',
        'USOC': 98,
        'Uac': 245,
        'Ubat': 212,
        'dischargeNotAllowed': False,
        'generator_autostart': False
    }
    return test_data_status_charging

@pytest_asyncio.fixture
async def get_sonnen():
    """Sonnen class fixture"""
    return  Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)

@pytest.mark.asyncio
async def test_get_value(mocker):
    """Batterie status test using mock data"""
    mock_response = status_charging()
    mocker.patch.object(Sonnen, "fetch_status", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    result = await battery.fetch_status()

    assert result is True
    assert battery.grid_in == 54
    assert battery.grid_out == 0
