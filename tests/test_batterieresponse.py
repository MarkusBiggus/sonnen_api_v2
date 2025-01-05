"""pytest tests/test_batterieresponse.py -s -v -x
1. Async update called from an async method.
"""
import datetime
import os
import sys
import logging
import urllib3

#for tests only
import pytest
from freezegun import freeze_time
from unittest.mock import patch

from sonnen_api_v2 import Batterie, BatterieBackup, BatterieResponse, BatterieAuthError, BatterieError

from .battery_charging_asyncio import fixture_battery_charging
from . mock_battery_configurations import __battery_configurations_auth200

LOGGER_NAME = None # "sonnenapiv2" #

logging.getLogger("batterieResponse").setLevel(logging.WARNING)

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
@freeze_time("20-11-2023 17:00:00")
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth200)
async def test_batterieresponse(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.validate_token()

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(version='1.14.5', last_updated=datetime.datetime(2023, 11, 20, 17, 0), configurations={'EM_RE_ENABLE_MICROGRID': 'False', 'NVM_PfcIsFixedCosPhiActive': 0, 'NVM_PfcFixedCosPhi': 0.8, 'IC_BatteryModules': 4, 'EM_ToU_Schedule': [], 'DE_Software': '1.14.5', 'EM_USER_INPUT_TIME_ONE': 0, 'NVM_PfcIsFixedCosPhiLagging': 0, 'EM_Prognosis_Charging': 1, 'EM_USOC': 20, 'EM_USER_INPUT_TIME_TWO': 0, 'EM_OperatingMode': '2', 'SH_HeaterTemperatureMax': 80, 'SH_HeaterOperatingMode': 0, 'IC_InverterMaxPower_w': 5000, 'SH_HeaterTemperatureMin': 0, 'CM_MarketingModuleCapacity': 5000, 'EM_USER_INPUT_TIME_THREE': 0, 'CN_CascadingRole': 'none', 'EM_US_GEN_POWER_SET_POINT': 0, 'DepthOfDischargeLimit': 93})

    response = await _batterie.refresh_response()

    #print(f'response: {response}')

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(version='1.14.5', last_updated=datetime.datetime(2023, 11, 20, 17, 0), configurations={'EM_RE_ENABLE_MICROGRID': 'False', 'NVM_PfcIsFixedCosPhiActive': 0, 'NVM_PfcFixedCosPhi': 0.8, 'IC_BatteryModules': 4, 'EM_ToU_Schedule': [], 'DE_Software': '1.14.5', 'EM_USER_INPUT_TIME_ONE': 0, 'NVM_PfcIsFixedCosPhiLagging': 0, 'EM_Prognosis_Charging': 1, 'EM_USOC': 20, 'EM_USER_INPUT_TIME_TWO': 0, 'EM_OperatingMode': '2', 'SH_HeaterTemperatureMax': 80, 'SH_HeaterOperatingMode': 0, 'IC_InverterMaxPower_w': 5000, 'SH_HeaterTemperatureMin': 0, 'CM_MarketingModuleCapacity': 5000, 'EM_USER_INPUT_TIME_THREE': 0, 'CN_CascadingRole': 'none', 'EM_US_GEN_POWER_SET_POINT': 0, 'DepthOfDischargeLimit': 93})

    sensor_value = _batterie.get_sensor_value('configuration_de_software')
    assert sensor_value == '1.14.5'

@pytest.mark.asyncio
@patch.object(Batterie, 'async_validate_token', lambda *args: False)
async def test_batterieresponse_BatterieAuthError(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    with pytest.raises(BatterieAuthError, match='BatterieBackup: Error validating API token!'):
        response = await _batterie.validate_token()

    # assert isinstance(response, BatterieResponse) is True
    # assert response == BatterieResponse(version='1.14.5', last_updated=datetime.datetime(2023, 11, 20, 17, 0), configurations={'EM_RE_ENABLE_MICROGRID': 'False', 'NVM_PfcIsFixedCosPhiActive': 0, 'NVM_PfcFixedCosPhi': 0.8, 'IC_BatteryModules': 4, 'EM_ToU_Schedule': [], 'DE_Software': '1.14.5', 'EM_USER_INPUT_TIME_ONE': 0, 'NVM_PfcIsFixedCosPhiLagging': 0, 'EM_Prognosis_Charging': 1, 'EM_USOC': 20, 'EM_USER_INPUT_TIME_TWO': 0, 'EM_OperatingMode': '2', 'SH_HeaterTemperatureMax': 80, 'SH_HeaterOperatingMode': 0, 'IC_InverterMaxPower_w': 5000, 'SH_HeaterTemperatureMin': 0, 'CM_MarketingModuleCapacity': 5000, 'EM_USER_INPUT_TIME_THREE': 0, 'CN_CascadingRole': 'none', 'EM_US_GEN_POWER_SET_POINT': 0, 'DepthOfDischargeLimit': 93})


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_charging")
@freeze_time("20-11-2023 17:00:00")
@patch.object(urllib3.HTTPConnectionPool, 'urlopen', __battery_configurations_auth200)
@patch.object(Batterie, 'async_update', lambda *args: False)
async def test_batterieresponse_BatterieError(battery_charging: Batterie) -> None:
    """Batterie Response using mock data"""

    _batterie = BatterieBackup('fakeToken', 'fakeHost')

    response = await _batterie.validate_token()

    assert isinstance(response, BatterieResponse) is True
    assert response == BatterieResponse(version='1.14.5', last_updated=datetime.datetime(2023, 11, 20, 17, 0), configurations={'EM_RE_ENABLE_MICROGRID': 'False', 'NVM_PfcIsFixedCosPhiActive': 0, 'NVM_PfcFixedCosPhi': 0.8, 'IC_BatteryModules': 4, 'EM_ToU_Schedule': [], 'DE_Software': '1.14.5', 'EM_USER_INPUT_TIME_ONE': 0, 'NVM_PfcIsFixedCosPhiLagging': 0, 'EM_Prognosis_Charging': 1, 'EM_USOC': 20, 'EM_USER_INPUT_TIME_TWO': 0, 'EM_OperatingMode': '2', 'SH_HeaterTemperatureMax': 80, 'SH_HeaterOperatingMode': 0, 'IC_InverterMaxPower_w': 5000, 'SH_HeaterTemperatureMin': 0, 'CM_MarketingModuleCapacity': 5000, 'EM_USER_INPUT_TIME_THREE': 0, 'CN_CascadingRole': 'none', 'EM_US_GEN_POWER_SET_POINT': 0, 'DepthOfDischargeLimit': 93})

    with pytest.raises(BatterieError, match='BatterieBackup: Error updating batterie data!'):
        response = await _batterie.refresh_response()

    #print(f'response: {response}')

    # assert isinstance(response, BatterieResponse) is True
    # assert response == BatterieResponse(version='1.14.5', last_updated=datetime.datetime(2023, 11, 20, 17, 0), configurations={'EM_RE_ENABLE_MICROGRID': 'False', 'NVM_PfcIsFixedCosPhiActive': 0, 'NVM_PfcFixedCosPhi': 0.8, 'IC_BatteryModules': 4, 'EM_ToU_Schedule': [], 'DE_Software': '1.14.5', 'EM_USER_INPUT_TIME_ONE': 0, 'NVM_PfcIsFixedCosPhiLagging': 0, 'EM_Prognosis_Charging': 1, 'EM_USOC': 20, 'EM_USER_INPUT_TIME_TWO': 0, 'EM_OperatingMode': '2', 'SH_HeaterTemperatureMax': 80, 'SH_HeaterOperatingMode': 0, 'IC_InverterMaxPower_w': 5000, 'SH_HeaterTemperatureMin': 0, 'CM_MarketingModuleCapacity': 5000, 'EM_USER_INPUT_TIME_THREE': 0, 'CN_CascadingRole': 'none', 'EM_US_GEN_POWER_SET_POINT': 0, 'DepthOfDischargeLimit': 93})
