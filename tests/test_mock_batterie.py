"""pytest tests/test_mock_batterie.py -s -v -x
"""
#import datetime
import os
import sys

import logging
import pytest
import pytest_asyncio
from pytest_mock import mocker
from asyncmock import AsyncMock
import json


#from freezegun import freeze_time
from sonnen_api_v2.sonnen import Sonnen as Batterie
from dotenv import load_dotenv

from . mock_status_charging import status_charging
from . mock_status_discharging import status_discharging
from . mock_latest_charging import latest_charging
from . mock_latest_discharging import latest_discharging
from . mock_powermeter import mock_powermeter
from . mock_battery import mock_battery
from . mock_inverter import mock_inverter
from . mock_configurations import mock_configurations

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
BATTERIE_PORT = '80'
API_READ_TOKEN = os.getenv('API_READ_TOKEN')
# BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
# API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
# BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
# API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')

LOGGER_NAME = None # "sonnenapiv2" #


if BATTERIE_HOST == 'X':
    raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN in .env See env.example')

logging.getLogger("mock_batterie").setLevel(logging.WARNING)

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
    logger.info ('Asyncio mock batterie tests')


@pytest.mark.asyncio
async def test_get_batterie_charging(mocker: mocker):
    """Batterie charging using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=mock_configurations()))
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_charging()))
#    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_discharging()))
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_charging()))
#    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_discharging()))
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=mock_powermeter()))
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=mock_battery()))
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=mock_inverter()))

    _battery = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_PORT, LOGGER_NAME)  # Batterie online

    await _battery.async_update()
    version = _battery.configuration_de_software # mock_configurations
    status = _battery.system_status # latest_charging
    backup_buffer = _battery.status_backup_buffer # status_charging
    kwh_consumed = _battery.kwh_consumed # mock_powermeter
    cycles = _battery.battery_cycle_count # mock_battery
    PAC_total = _battery.inverter_pac_total # mock_inverter

    print(f'\n\rStatus: {status}  Software Version: {version}   Battery Cycles: {cycles:,}')
    print(f'PAC: {PAC_total:,.2f}W  Consumed: {kwh_consumed:,.2f}  Backup Buffer: {backup_buffer}%')
    assert status == 'OnGrid'
    assert cycles == 30
    assert version == '1.14.5'
    assert PAC_total == -1394.33
    assert backup_buffer == 20
    assert kwh_consumed == 816.5

@pytest.mark.asyncio
async def test_get_batterie_response(mocker: mocker):
    """Batterie charging using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=mock_configurations()))
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_charging()))
#    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_discharging()))
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_charging()))
#    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_discharging()))
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=mock_powermeter()))
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=mock_battery()))
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=mock_inverter()))

    _battery = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_PORT, LOGGER_NAME)  # Batterie online

    # called by component
    response = await _battery.get_data()
    last_updated = response.last_updated
    if last_updated is not None:
        print('Last Updated: '+ last_updated.strftime('%d-%b-%Y %H:%M:%S'))
    else:
        print('Batterie response was not updated.')

    assert response.serial_number == "123321"
