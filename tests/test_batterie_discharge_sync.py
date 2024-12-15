"""pytest tests/test_batterie_sync.py -s -v -x
3. Sync update called from sync method
"""
import datetime
import logging
import pytest
from freezegun import freeze_time
import responses
from sonnen_api_v2 import Batterie, BatterieError

from .battery_discharging_sync import fixture_battery_discharging

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@responses.activate
@freeze_time("24-05-2022 15:38:23")
@pytest.mark.usefixtures("battery_discharging")
def test_sync_methods(battery_discharging: Batterie) -> None:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data sync test suite.')

    assert battery_discharging.discharging > 0
    assert battery_discharging.charging == 0
    assert battery_discharging.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'

    # sync wrapped methods used by ha component
    status_data = battery_discharging.sync_get_status()
    latest_data = battery_discharging.sync_get_latest_data()
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == latest_data.get('Timestamp')
    assert status_data.get('GridFeedIn_W') == latest_data.get('GridFeedIn_W')
    assert status_data.get('Consumption_W') == latest_data.get('Consumption_W')
    assert status_data.get('Production_W') == latest_data.get('Production_W')
    assert status_data.get('Pac_total_W') == latest_data.get('Pac_total_W')

    assert status_data.get('Timestamp') == '2023-11-20 17:00:58'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1541
    assert status_data.get('Production_W') == 103
    assert status_data.get('Pac_total_W') == 1438

    assert latest_data.get('Timestamp') == '2023-11-20 17:00:58'
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Consumption_W') == 1541
    assert latest_data.get('Production_W') == 103
    assert latest_data.get('Pac_total_W') == 1438

    powermeter = battery_discharging.sync_get_powermeter()
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[1]['direction'] == 'consumption'

    battery_status =  battery_discharging.sync_get_battery()
    assert battery_status.get('cyclecount') == 30
    assert battery_status.get('remainingcapacity') == 177.74

    inverter_data = battery_discharging.sync_get_inverter()
    assert status_data.get('Pac_total_W') == inverter_data.get('pac_total')

    assert inverter_data.get('pac_total') == 1438
    assert inverter_data.get('uac') == 233.55

    configurations = battery_discharging.sync_get_configurations()
    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20

    from .check_results import check_discharge_results

    check_discharge_results(battery_discharging)