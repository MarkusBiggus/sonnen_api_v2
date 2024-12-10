import os
import logging
import pytest
#from freezegun import freeze_time
import responses

from sonnen_api_v2 import Batterie
from dotenv import load_dotenv

from . mock_sonnenbatterie_v2_charging import __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging

load_dotenv()

BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')
BATTERIE_HOST_PORT = os.getenv('BATTERIE_HOST_PORT')

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if BATTERIE_2_HOST == 'X':
    raise ValueError('Set BATTERIE_2_HOST & API_READ_TOKEN_2 in .env See env.example')

@responses.activate
#@freeze_time("24-05-2022 15:38:23")
@pytest.fixture(name="battery_discharging")
def battery_discharging_sync() -> Batterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_discharging_sync test.')

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

    responses.add(battery_discharging_powermeter_data)
    responses.add(battery_discharging_latest_data)
    responses.add(battery_discharging_configurations)
    responses.add(battery_discharging_status)
    responses.add(battery_discharging_battery_data)
    responses.add(battery_discharging_inverter_data)

    battery_discharging = Batterie(API_READ_TOKEN_2, BATTERIE_2_HOST, BATTERIE_HOST_PORT)  # Working and discharging - no logging
    success = battery_discharging.sync_update()
    assert success is True

    return battery_discharging
#     result1 = battery_charging.fully_charged_at
#     assert result1.strftime('%d.%B.%Y %H:%M') == '24.May.2022 16:38'

#     # sync wrapped methods used by ha component called by syncio.async_add_executor_job
#     status_data = battery_charging.sync_get_status()
# #    print(f'status: {status_data}')
#     assert status_data.get('GridFeedIn_W') == 0
#     assert status_data.get('Consumption_W') == 1578
#     assert status_data.get('Production_W') == 2972
#     assert status_data.get('Pac_total_W') == -1394

#     latest_data = battery_charging.sync_get_latest_data()
#     assert latest_data.get('GridFeedIn_W') == 0
#     assert latest_data.get('Production_W') == 2972
#     assert latest_data.get('Consumption_W') == 1578
#     assert latest_data.get('Pac_total_W') == -1394

#     powermeter = battery_charging.sync_get_powermeter()
#     assert powermeter[0]['direction'] == 'production'
#     assert powermeter[1]['direction'] == 'consumption'

#     status_data =  battery_charging.sync_get_battery()
#     assert status_data.get('cyclecount') == 30
#     assert status_data.get('remainingcapacity') == 177.74

#     status_data = battery_charging.sync_get_inverter()
#     assert status_data.get('pac_total') == -1394.33
#     assert status_data.get('uac') == 233.55

#     configuratons = battery_charging.sync_get_configurations()
#     assert configuratons.get('DE_Software') == '1.14.5'
#     assert configuratons.get('EM_USOC') == 20
