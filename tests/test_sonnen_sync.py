"""pytest tests/test_sonnen_sync.py -s -v -x
3. Sync update called from sync method
"""
#import datetime
import os
import logging
import pytest
from freezegun import freeze_time
import responses
#from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieError
from sonnen_api_v2 import Batterie, BatterieError
from dotenv import load_dotenv
from . check_results import check_results

from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging

load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')
BATTERIE_HOST_PORT = os.getenv('BATTERIE_HOST_PORT')

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if BATTERIE_1_HOST == 'X':
    raise ValueError('Set BATTERIE_1_HOST & API_READ_TOKEN_1 in .env See env.example')

@responses.activate
@freeze_time("24-05-2022 15:38:23")
def test_sync_methods() -> None:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data sync test suite.')

    battery_charging_powermeter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/powermeter'),
        status=200,
        json=__mock_powermeter()
    )

    battery_charging_latest_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/latestdata'),
        status=200,
        json=__mock_latest_charging()
    )

    battery_charging_configurations = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/configurations'),
        status=200,
        json=__mock_configurations()
    )

    battery_charging_status = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/status'),
        status=200,
        json=__mock_status_charging()
    )

    battery_charging_battery_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/battery'),
        status=200,
        json=__mock_battery()
    )

    battery_charging_inverter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/inverter'),
        status=200,
        json=__mock_inverter()
    )

    battery_discharging_powermeter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/powermeter'),
        status=200,
        json=__mock_powermeter()
    )

    battery_discharging_latest_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/latestdata'),
        status=200,
        json=__mock_latest_discharging()
    )

    battery_discharging_configurations = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/configurations'),
        status=200,
        json=__mock_configurations()
    )

    battery_discharging_status = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/status'),
        status=200,
        json=__mock_status_discharging()
    )

    battery_discharging_battery_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/battery'),
        status=200,
        json=__mock_battery()
    )

    battery_discharging_inverter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/inverter'),
        status=200,
        json=__mock_inverter()
    )

    battery3_powermeter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/powermeter'),
        status=401,
        json={"error":"Unauthorized"}
    )

    battery3_latest_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/latestdata'),
        status=401,
        json={"error":"Unauthorized"}
    )

    battery3_configurations = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/configurations'),
        status=401,
        json={"error":"Unauthorized"}
    )

    battery3_status = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/status'),
        status=401,
        json={"error":"Unauthorized"}
    )

    battery3_battery_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/battery'),
        status=401,
        json={"error":"Unauthorized"}
    )

    battery3_inverter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/inverter'),
        status=401,
        json={"error":"Unauthorized"}
    )

    responses.add(battery_charging_powermeter_data)
    responses.add(battery_charging_latest_data)
    responses.add(battery_charging_configurations)
    responses.add(battery_charging_status)
    responses.add(battery_charging_battery_data)
    responses.add(battery_charging_inverter_data)

    responses.add(battery_discharging_powermeter_data)
    responses.add(battery_discharging_latest_data)
    responses.add(battery_discharging_configurations)
    responses.add(battery_discharging_status)
    responses.add(battery_discharging_battery_data)
    responses.add(battery_discharging_inverter_data)

    responses.add(battery3_powermeter_data)
    responses.add(battery3_latest_data)
    responses.add(battery3_configurations)
    responses.add(battery3_status)
    responses.add(battery3_battery_data)
    responses.add(battery3_inverter_data)

#    API_READ_TOKEN_1 = os.getenv('AUTH_TOKEN')

    battery_charging = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Working and charging
    battery_discharging = Batterie(API_READ_TOKEN_2, BATTERIE_2_HOST, BATTERIE_HOST_PORT)  # Working and discharging - no logging
#    self.battery_unreachable = Batterie('notWorkingToken', '155.156.19.5', BATTERIE_HOST_PORT, LOGGER_NAME)  # Not Reachable
    battery_wrong_token = Batterie('notWorkingToken', BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Wrong Token

    success = battery_charging.update()
    assert success is True
    success = battery_discharging.update()
    assert success is True
#   success = battery_unreachable.update()
    with pytest.raises(BatterieError) as error:
        success = battery_wrong_token.update()
        print(f'error: |{error.value.args[0]}|')
        assert error.value.args[0] == 'Get endpoint http://192.168.188.11:80/api/v2/configurations status: 401'
    #   assert str(exc_info.value) == 'some info'
    #    assert success is False

    check_results(battery_charging, battery_discharging)