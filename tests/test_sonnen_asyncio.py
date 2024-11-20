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
from sonnen_api_v2.sonnen import Sonnen
from dotenv import load_dotenv

from . mock_status_charging import status_charging
from . mock_status_discharging import status_discharging
from . mock_latest_charging import latest_charging
from . mock_latest_discharging import latest_discharging
from . mock_powermeter import mock_powermeter
from . mock_battery import mock_battery
from . mock_inverter import mock_inverter

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


@pytest_asyncio.fixture
async def get_sonnen():
    """Sonnen class fixture"""
    return  Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)

@pytest.mark.asyncio
async def test_get_status_charging(mocker):
    """Batterie status test using mock data"""
    mock_response = status_charging()
    mocker.patch.object(Sonnen, "fetch_status", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == 54
    assert status_data.get('Consumption_W') == 403
    assert status_data.get('Pac_total_W') == -95
    # assert battery.grid_in == 54
    # assert battery.grid_out == 0

@pytest.mark.asyncio
async def test_get_status_discharging(mocker):
    """Batterie status test using mock data"""
    mock_response = status_discharging()
    mocker.patch.object(Sonnen, "fetch_status", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == -20
    assert status_data.get('Consumption_W') == 541
    assert status_data.get('Pac_total_W') == 438

@pytest.mark.asyncio
async def test_get_latest_charging(mocker):
    """Batterie latest data test using mock data"""
    mock_response = latest_charging()
    mocker.patch.object(Sonnen, "fetch_latest_details", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    latest_data = await battery.fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Pac_total_W') == -1394

@pytest.mark.asyncio
async def test_get_latest_discharging(mocker):
    """Batterie latest data test using mock data"""
    mock_response = latest_discharging()
    mocker.patch.object(Sonnen, "fetch_latest_details", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    latest_data = await battery.fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 102
    assert latest_data.get('Consumption_W') == 1541
    assert latest_data.get('Pac_total_W') == 1439

@pytest.mark.asyncio
async def test_get_powermeter(mocker):
    """Batterie powermeter test using mock data"""
    mock_response = mock_powermeter()
    mocker.patch.object(Sonnen, "fetch_powermeter", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
#    powermeter = json.loads(await battery.fetch_powermeter() )
    powermeter = await battery.fetch_powermeter()
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[1]['direction'] == 'consumption'

@pytest.mark.asyncio
async def test_get_battery(mocker):
    """Batterie status test using mock data"""
    mock_response = mock_battery()
    mocker.patch.object(Sonnen, "fetch_battery_status", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_battery_status()
    assert status_data.get('cyclecount') == 30
    assert status_data.get('remainingcapacity') == 75.39

@pytest.mark.asyncio
async def test_get_inventer(mocker):
    """Batterie inverter status test using mock data"""
    mock_response = mock_inverter()
    mocker.patch.object(Sonnen, "fetch_inverter_data", AsyncMock(return_value=mock_response))

    battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_inverter_data()
    assert status_data.get('pac_total') == 0.06
    assert status_data.get('uac') == 233.55
