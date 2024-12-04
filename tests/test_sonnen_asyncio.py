"""pytest tests/test_sonnen_asyncio.py -s -v -x """
#import datetime
import os
import sys
import logging
import pytest
#import pytest_asyncio
#from pytest_mock import mocker
from asyncmock import AsyncMock
#import json


#from freezegun import freeze_time
from sonnen_api_v2.sonnen import Sonnen as Batterie
from dotenv import load_dotenv

from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging

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


@pytest.mark.asyncio
async def test_get_status_charging(mocker):
    """Batterie status charging using mock data"""
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=__mock_status_charging()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == 54
    assert status_data.get('Consumption_W') == 403
    assert status_data.get('Production_W') == 578
    assert status_data.get('Pac_total_W') == -95
    # assert battery.grid_in == 54
    # assert battery.grid_out == 0

@pytest.mark.asyncio
async def test_get_status_discharging(mocker):
    """Batterie status discharging using mock data"""
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=__mock_status_discharging()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_status()
#    print(f'status: {status_data}')
    assert status_data.get('GridFeedIn_W') == -20
    assert status_data.get('Consumption_W') == 541
    assert status_data.get('Production_W') == 102
    assert status_data.get('Pac_total_W') == 438

@pytest.mark.asyncio
async def test_get_latest_charging(mocker):
    """Batterie latest data charging using mock data"""
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    latest_data = await battery.fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Pac_total_W') == -1394

@pytest.mark.asyncio
async def test_get_latest_discharging(mocker):
    """Batterie latest data discharging using mock data"""
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=__mock_latest_discharging()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    latest_data = await battery.fetch_latest_details()
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Production_W') == 102
    assert latest_data.get('Consumption_W') == 1541
    assert latest_data.get('Pac_total_W') == 1439

@pytest.mark.asyncio
async def test_get_powermeter(mocker):
    """Batterie powermeter test using mock data"""
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    powermeter = await battery.fetch_powermeter()
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[1]['direction'] == 'consumption'

@pytest.mark.asyncio
async def test_get_battery(mocker):
    """Batterie status test using mock data"""
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=__mock_battery()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_battery_status()
    assert status_data.get('cyclecount') == 30
    assert status_data.get('remainingcapacity') == 197.94

@pytest.mark.asyncio
async def test_get_inverter(mocker):
    """Batterie inverter status using mock data"""
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=__mock_inverter()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    status_data = await battery.fetch_inverter_data()
    assert status_data.get('pac_total') == -1394.33
    assert status_data.get('uac') == 233.55

@pytest.mark.asyncio
async def test_get_configurations(mocker):
    """Batterie configurations using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=__mock_configurations()))

    battery = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)
    configuratons = await battery.fetch_configurations()
    assert configuratons.get('DE_Software') == '1.14.5'
    assert configuratons.get('EM_USOC') == 20
