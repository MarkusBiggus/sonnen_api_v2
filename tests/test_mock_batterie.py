"""pytest tests/test_mock_batterie.py -s -v -x
"""
#import datetime
import os
import sys

import logging
import pytest
import pytest_asyncio
#from pytest_mock import mocker
from asyncmock import AsyncMock
#import json
from dotenv import load_dotenv
#from freezegun import freeze_time

from sonnen_api_v2.sonnen import Sonnen as Batterie

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
async def test_get_batterie_charging(mocker):
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
async def test_get_batterie_response(mocker):
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

    # called by sonnen ha component
    response = await _battery.get_data()
    last_updated = response.last_updated
    version = response.version
    if last_updated is not None:
        print(f'Version: {version}  Last Updated: '+ last_updated.strftime('%d-%b-%Y %H:%M:%S'))
    else:
        print('Batterie response was not updated!')

    assert response.serial_number == "XxxxxX"

# @pytest.mark.asyncio
# async def test_get_batterie_wrapped(mocker):
def test_get_batterie_wrapped(mocker):
    """sonnenbatterie package Emulated methods using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=mock_configurations()))
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_charging()))
#    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=status_discharging()))
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_charging()))
#    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=latest_discharging()))
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=mock_powermeter()))
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=mock_battery()))
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=mock_inverter()))

    _battery = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_PORT, LOGGER_NAME)  # Batterie online
    assert _battery is not False
    latestData = {}
    # code syntax from custom_component coordinator.py
    latestData["powermeter"] = _battery.get_powermeter()
    latestData["battery_system"] = _battery.get_batterysystem()
    print(f'latest: {latestData}')
    batt_module_capacity = int(
        latestData["battery_system"]["battery_system"]["system"][
            "storage_capacity_per_module"
        ]
    )
    assert batt_module_capacity == 5000
    batt_module_count = int(latestData["battery_system"]["modules"])
    assert batt_module_count == 2

    latestData["powermeter"] = _battery.get_powermeter()
    if(isinstance(latestData["powermeter"],dict)):
        newPowerMeters=[]
        for index,dictIndex in enumerate(latestData["powermeter"]):
            newPowerMeters.append(latestData["powermeter"][dictIndex])
        print(f'new powermeters: {newPowerMeters}')

    latestData["status"] = _battery.get_status()
    print(f'status type: {type(latestData["status"])}')
    if latestData["status"]["BatteryCharging"]:
        battery_current_state = "charging"
    elif latestData["status"]["BatteryDischarging"]:
        battery_current_state = "discharging"
    else:
        battery_current_state = "standby"
    RSOC = latestData["status"]["RSOC"]
    print(f'battery_state: {battery_current_state}  RSOC: {RSOC}%')

    print(f'module_capacity: {batt_module_capacity:,}Wh  module_count: {batt_module_count}')
    batt_reserved_factor = 7.0
    total_installed_capacity = int(batt_module_count * batt_module_capacity)
    reserved_capacity = int(
            total_installed_capacity * (batt_reserved_factor / 100.0)
        )
    remaining_capacity = (
            int(total_installed_capacity * latestData["status"]["RSOC"]) / 100.0
        )
    remaining_capacity_usable = max(
            0, int(remaining_capacity - reserved_capacity))
    print(f'remaining_capacity_usable: {remaining_capacity_usable:,}Wh')
