"""pytest tests/test_batterie_sync.py -s -v -x
3. Sync update called from sync method
"""
import datetime
import logging
import pytest
from freezegun import freeze_time
import responses
#from sonnen_api_v2.sonnen import Sonnen as Batterie, BatterieError
from sonnen_api_v2 import Batterie, BatterieError

from .battery_charging_sync import fixture_battery_charging

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@responses.activate
@freeze_time("24-05-2022 15:38:23")
@pytest.mark.usefixtures("battery_charging")
def test_sync_methods(battery_charging: Batterie) -> None:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data sync test suite.')

    assert battery_charging.charging > 0
    assert battery_charging.discharging == 0
    assert battery_charging.fully_charged_at.strftime('%d.%B.%Y %H:%M') == '24.May.2022 17:25'

    # sync wrapped methods used by ha component
    status_data = battery_charging.sync_get_status()
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == '2022-04-30 17:00:55'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1578
    assert status_data.get('Production_W') == 2972
    assert status_data.get('Pac_total_W') == -1394

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

    from .check_results import check_charge_results

    check_charge_results(battery_charging)
