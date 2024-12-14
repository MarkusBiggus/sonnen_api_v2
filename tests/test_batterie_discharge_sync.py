"""pytest tests/test_batterie_sync.py -s -v -x
3. Sync update called from sync method
"""
import datetime
import logging
import pytest
from freezegun import freeze_time
import responses
from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieError
#from sonnen_api_v2 import Batterie, BatterieError

from .battery_charging_sync import fixture_battery_charging
from .battery_discharging_sync import fixture_battery_discharging
from .battery_discharging_reserve_sync import fixture_battery_discharging_reserve

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@responses.activate
@freeze_time("24-05-2022 15:38:23")
@pytest.mark.usefixtures("battery_charging","battery_discharging","battery_discharging_reserve")
def test_sync_methods(battery_charging: Batterie, battery_discharging: Batterie, battery_discharging_reserve: Batterie) -> None:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data sync test suite.')

    # battery_charging = Batterie(API_READ_TOKEN_1, BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Working and charging
    # battery_discharging = Batterie(API_READ_TOKEN_2, BATTERIE_2_HOST, BATTERIE_HOST_PORT)  # Working and discharging - no logging
#    self.battery_unreachable = Batterie('notWorkingToken', '155.156.19.5', BATTERIE_HOST_PORT, LOGGER_NAME)  # Not Reachable
#    battery_wrong_token = Batterie('notWorkingToken', BATTERIE_1_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)  # Wrong Token

    # success = battery_charging.sync_update()
    # assert success is True
    # success = battery_discharging.sync_update()
    # assert success is True
    # success = battery_discharging_reserve.sync_update()
    # assert success is True
#   success = battery_unreachable.update()
    # with pytest.raises(BatterieError) as error:
    #     success = battery_wrong_token.sync_update()
    # #   assert str(exc_info.value) == 'some info'
    # #    assert success is False
    # print(f'error: |{error.value.args[0]}|',flush=True)
    # assert error.value.args[0] == 'Get endpoint http://192.168.188.11:80/api/v2/configurations status: 401'

    assert battery_charging.charging > 0
    assert battery_charging.discharging == 0
    assert battery_charging.fully_charged_at.strftime('%d.%B.%Y %H:%M') == '24.May.2022 17:25'

    assert battery_discharging.discharging > 0
    assert battery_discharging.charging == 0
    assert battery_discharging.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'

    # sync wrapped methods used by ha component
    status_data = battery_charging.sync_get_status()
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

    status_data = battery_discharging.sync_get_status()
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:58'

    status_data = battery_discharging_reserve.sync_get_status()
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:59'

    latest_data = battery_charging.sync_get_latest_data()
    assert latest_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Consumption_W') == 1578
    assert latest_data.get('Production_W') == 2972
    assert latest_data.get('Pac_total_W') == -1394

    powermeter = battery_charging.sync_get_powermeter()
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[1]['direction'] == 'consumption'

    status_data =  battery_charging.sync_get_battery()
    assert status_data.get('cyclecount') == 30
    assert status_data.get('remainingcapacity') == 177.74

    status_data = battery_charging.sync_get_inverter()
    assert status_data.get('pac_total') == -1394.33
    assert status_data.get('uac') == 233.55

    configuratons = battery_charging.sync_get_configurations()
    assert configuratons.get('DE_Software') == '1.14.5'
    assert configuratons.get('EM_USOC') == 20

    from .check_results import check_results

    check_results(battery_charging, battery_discharging, battery_discharging_reserve)
