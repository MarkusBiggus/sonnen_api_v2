"""pytest tests/test_sonnen_sync.py -s -v -x """
import datetime
import os
import logging
import pytest
from freezegun import freeze_time
import responses
from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieError
from dotenv import load_dotenv

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
        logging.basicConfig(filename='logs/'+LOGGER_NAME +'.log', level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
    else:
        logger = logging.getLogger(__package__).setLevel(logging.DEBUG)

    logger.info('Sonnen mock data sync test suite.')

    battery1_powermeter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/powermeter'),
        status=200,
        json=__mock_powermeter()
    )

    battery1_latest_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/latestdata'),
        status=200,
        json=__mock_latest_charging()
    )

    battery1_configurations = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/configurations'),
        status=200,
        json=__mock_configurations()
    )

    battery1_status = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/status'),
        status=200,
        json=__mock_status_charging()
    )

    battery1_battery_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/battery'),
        status=200,
        json=__mock_battery()
    )

    battery1_inverter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_1_HOST}:{BATTERIE_HOST_PORT}/api/v2/inverter'),
        status=200,
        json=__mock_inverter()
    )

    battery2_powermeter_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/powermeter'),
        status=200,
        json=__mock_powermeter()
    )

    battery2_latest_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/latestdata'),
        status=200,
        json=__mock_latest_discharging()
    )

    battery2_configurations = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/configurations'),
        status=200,
        json=__mock_configurations()
    )

    battery2_status = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/status'),
        status=200,
        json=__mock_status_discharging()
    )

    battery2_battery_data = responses.Response(
        method='GET',
        url=(f'http://{BATTERIE_2_HOST}:{BATTERIE_HOST_PORT}/api/v2/battery'),
        status=200,
        json=__mock_battery()
    )

    battery2_inverter_data = responses.Response(
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
        status=200,
        json=__mock_configurations()
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
        status=200,
        json=__mock_inverter()
    )

    responses.add(battery1_powermeter_data)
    responses.add(battery1_latest_data)
    responses.add(battery1_configurations)
    responses.add(battery1_status)
    responses.add(battery1_battery_data)
    responses.add(battery1_inverter_data)

    responses.add(battery2_powermeter_data)
    responses.add(battery2_latest_data)
    responses.add(battery2_configurations)
    responses.add(battery2_status)
    responses.add(battery2_battery_data)
    responses.add(battery2_inverter_data)

    responses.add(battery3_powermeter_data)
    responses.add(battery3_latest_data)
    responses.add(battery3_configurations)
    responses.add(battery3_status)
    responses.add(battery3_battery_data)
    responses.add(battery3_inverter_data)

#    API_READ_TOKEN_1 = os.getenv('AUTH_TOKEN')

    battery_charging_working = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Working and charging
    battery_discharging_working = Batterie(API_READ_TOKEN_2, BATTERIE_2_HOST, BATTERIE_HOST_PORT)  # Working and discharging - no logging
#    self.battery_unreachable = Batterie('notWorkingToken', '155.156.19.5', BATTERIE_HOST_PORT, LOGGER_NAME)  # Not Reachable
    battery_wrong_token_charging = Batterie('notWorkingToken', BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Wrong Token

    success = battery_charging_working.update()
    assert success is True
    success = battery_discharging_working.update()
    assert success is True
#   success = battery_unreachable.update()
    with pytest.raises(BatterieError) as error:
        success = battery_wrong_token_charging.update()
        assert error.value.args[0] == 'Get endpoint "http://192.168.188.11:80/api/v2/latestdata" status: 401'
    #   assert str(exc_info.value) == 'some info'
        assert success is False

# @responses.activate
# def test_consumption_average(self):

    result1 = battery_charging_working.consumption_average
    result2 = battery_discharging_working.consumption_average
#    result3 = battery_wrong_token_charging.consumption_average
    assert result1 == 486
    assert result2 == 563
#    assert result3 is None

# @responses.activate
# def test_consumption(self):
    result1 = battery_charging_working.consumption
    result2 = battery_discharging_working.consumption
#    result3 = battery_wrong_token_charging.consumption
    assert result1 == 1578
    assert result2 == 1541
#    assert result3 is None

# @responses.activate
# def test_installed_modules(self):
    result1 = battery_charging_working.installed_modules
#    result2 = battery_unreachable.installed_modules
#    result3 = battery_wrong_token_charging.installed_modules
    result4 = battery_discharging_working.installed_modules
    assert result1 == 4
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 4

# @responses.activate
# def test_discharging(self):
    result1 = battery_charging_working.discharging
#    result2 = battery_unreachable.discharging
#    result3 = battery_wrong_token_charging.discharging
    result4 = battery_discharging_working.discharging
    assert result1 == 0
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 1439
    result1_pac = battery_charging_working.pac_total
#    result2_pac = battery_unreachable.pac_total
#    result3_pac = battery_wrong_token_charging.pac_total
    result4_pac = battery_discharging_working.pac_total
    assert result1_pac <= 0
#    assert result2_pac == 0
#    self.assertLessEqual(result3_pac is None
    assert result4_pac >= 0

# @responses.activate
# def test_charging(self):
    result1 = battery_charging_working.charging
#    result2 = battery_unreachable.charging
#    result3 = battery_wrong_token_charging.charging
    result4 = battery_discharging_working.charging
    assert result1 == 1394
#    assert result2 == 0
#    assert result3 == 0
    assert result4 == 0

# @responses.activate
# def test_grid_in(self):
    result1 = battery_charging_working.grid_in
#    result2 = battery_unreachable.grid_in
#    result3 = battery_wrong_token_charging.grid_in
    result4 = battery_discharging_working.grid_in
    assert result1 == 54
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 0

# @responses.activate
# def test_grid_out(self):
    result1 = battery_charging_working.grid_out
#    result2 = battery_unreachable.grid_out
#    result3 = battery_wrong_token_charging.grid_out
    result4 = battery_discharging_working.grid_out
    assert result1 >= 0
#    self.assertGreaterEqual(result2 == 0
#    assert result3 is None
    assert result4 == 20

# @responses.activate
# def test_production(self):
    result1 = battery_charging_working.production
#    result2 = battery_unreachable.production
#    result3 = battery_wrong_token_charging.production
    result4 = battery_discharging_working.production
    assert result1 == 2972
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 102

# @responses.activate
# def test_usoc(self):
    result1 = battery_charging_working.u_soc
#    result2 = battery_unreachable.u_soc
#    result3 = battery_wrong_token_charging.u_soc
    result4 = battery_discharging_working.u_soc
    assert result1 == 98
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 99

# @responses.activate
# def test_seconds_to_empty(self):
    result1 = battery_charging_working.seconds_to_empty
#    result2 = battery_unreachable.seconds_to_empty
#    result3 = battery_wrong_token_charging.seconds_to_empty
    result4 = battery_discharging_working.seconds_to_empty
    assert result1 == 0
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 50707

# @responses.activate
#@freeze_time("24-05-2022 15:38:23")
#def test_fully_discharged_at(self):
    result1 = battery_charging_working.fully_discharged_at
#    result2 = battery_unreachable.fully_discharged_at
#    result3 = battery_wrong_token_charging.fully_discharged_at
    result4 = battery_discharging_working.fully_discharged_at
    assert result1 is None
#    assert result2 == '00:00'
#    assert result3 is None
    assert result4.strftime('%d.%B.%Y %H:%M') == '25.May.2022 05:43'

# @responses.activate
# @freeze_time("24-04-2022 15:38:23")
# def test_seconds_since_full(self):
    result1 = battery_charging_working.seconds_since_full
#    result2 = battery_unreachable.seconds_since_full
#    result3 = battery_wrong_token_charging.seconds_since_full
    result4 = battery_charging_working.seconds_since_full
    assert result1 == 3720
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 3720

# @responses.activate
# def test_full_charge_capacity(self):
    result1 = battery_charging_working.full_charge_capacity
#    result2 = battery_unreachable.full_charge_capacity
#    result3 = battery_wrong_token_charging.full_charge_capacity
    result4 = battery_discharging_working.full_charge_capacity
    assert result1 == 20683
#    assert result2 == 0
#    assert result3 is None
    assert result4 == 20683

# @responses.activate
# @freeze_time('24-04-2022 15:38:23')
# def test_time_since_full(self):
    result1 = battery_charging_working.time_since_full
#    result2 = battery_unreachable.time_since_full
#    result3 = battery_wrong_token_charging.time_since_full
    result4 = battery_discharging_working.time_since_full
    assert result1 == datetime.timedelta(seconds=3720)
#    assert result2, datetime.timedelta(seconds=0))
#    assert result3, datetime.timedelta(seconds=0))
    assert result4 == datetime.timedelta(seconds=574)

# @responses.activate
# @freeze_time('24-04-2022 15:38:23')
# def test_seconds_until_fully_charged(self):
    result1 = battery_charging_working.seconds_until_fully_charged
#    result2 = battery_unreachable.seconds_until_fully_charged
#    result3 = battery_wrong_token_charging.seconds_until_fully_charged
    result4 = battery_discharging_working.seconds_until_fully_charged
    assert result1 == 10800 # <-!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    assert result2 == 0
#    assert result3 == 0
    assert result4 is None

# @responses.activate
# @freeze_time('24-04-2022 15:38:23')
# def test_fully_charged_at(self):
    result1 = battery_charging_working.fully_charged_at
#    result2 = battery_unreachable.fully_charged_at
#    result3 = battery_wrong_token_charging.fully_charged_at
    result4 = battery_discharging_working.fully_charged_at
    assert result1.strftime('%d.%B.%Y %H:%M') == '24.May.2022 15:38'
#    assert result2 == 0
#    assert result3 is None)
    assert result4 is None
