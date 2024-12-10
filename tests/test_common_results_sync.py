"""pytest tests/test_common_results_sync.py -s -v -x
3. Sync update called from sync method
"""
import datetime
from sonnen_api_v2 import Batterie
import pytest
from freezegun import freeze_time
import logging

from .battery_charging_sync import fixture_battery_charging
from .battery_discharging_sync import fixture_battery_discharging
from .battery_discharging_reserve_sync import fixture_battery_discharging_reserve

LOGGER_NAME = "sonnenapiv2"

@freeze_time("24-05-2022 15:38:23")
@pytest.mark.usefixtures("battery_charging","battery_discharging")
#def test_check_common_results():
def test_common_results(battery_charging: Batterie, battery_discharging: Batterie, battery_discharging_reserve: Batterie):
    """Common results for each method of updating
        Batterie object from network device
    """
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data sync common result checks.')

    """Common results for each method of updating
        Batterie object from network device
    """
    assert battery_charging.status_battery_charging is True
    assert battery_charging.status_battery_discharging is False
    assert battery_charging.system_status == 'OnGrid'

    assert battery_discharging.status_battery_charging is False
    assert battery_discharging.status_battery_discharging is True
    assert battery_discharging.system_status == 'OnGrid'

    assert battery_discharging_reserve.status_battery_charging is False
    assert battery_discharging_reserve.status_battery_discharging is True
    assert battery_discharging_reserve.system_status == 'OffGrid'

    assert battery_charging.consumption_average == 486
    assert battery_discharging.consumption_average == 563
    assert battery_discharging_reserve.consumption_average == 563

    result1 = battery_charging.consumption
    result2 = battery_discharging.consumption
    assert result1 == 1578
    assert result2 == 1541

    result1 = battery_charging.installed_modules
    result4 = battery_discharging.installed_modules
    assert result1 == 4
    assert result4 == 4

    assert battery_charging.discharging == 0
    assert battery_discharging.discharging == 1439
    assert battery_discharging_reserve.discharging == 1439

    result1_pac = battery_charging.pac_total
    result4_pac = battery_discharging.pac_total
    assert result1_pac <= 0
    assert result4_pac >= 0

    result1 = battery_charging.charging
    result4 = battery_discharging.charging
    assert result1 == 1394
    assert result4 == 0

    result1 = battery_charging.grid_in
    result4 = battery_discharging.grid_in
    assert result1 == 0
    assert result4 == 0

    assert battery_charging.grid_out >= 0
    assert battery_discharging.grid_out == 20
    assert battery_discharging_reserve.grid_out == 0

    result1 = battery_charging.production
    result4 = battery_discharging.production
    assert result1 == 2972
    assert result4 == 102

    assert battery_charging.u_soc == 88
    assert battery_discharging.u_soc == 88
    assert battery_discharging_reserve.u_soc == 18

    assert battery_charging.r_soc == 88
    assert battery_discharging.r_soc == 88
    assert battery_discharging_reserve.r_soc == 18

    assert battery_charging.seconds_until_fully_charged == 6412
    assert battery_discharging.seconds_until_reserve == 45533
    assert battery_discharging.seconds_until_fully_discharged == 45533
    assert battery_discharging_reserve.seconds_until_fully_discharged == 5533

    assert battery_charging.fully_discharged_at is None
    assert battery_discharging.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'
    assert battery_discharging_reserve.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 05:17'

    result1 = battery_charging.seconds_since_full
    result4 = battery_charging.seconds_since_full
    assert result1 == 3720
    assert result4 == 3720

    result1 = battery_charging.full_charge_capacity
    result4 = battery_discharging.full_charge_capacity
    assert result1 == 20683
    assert result4 == 20683

    result1 = battery_charging.time_since_full
    result4 = battery_discharging.time_since_full
    assert result1 == datetime.timedelta(seconds=3720)
    assert result4 == datetime.timedelta(seconds=574)

    remaining_charge = battery_charging.battery_full_charge_capacity_wh - battery_charging.battery_remaining_capacity_wh
    assert battery_charging.battery_full_charge_capacity_wh == 20683.49
    assert battery_charging.battery_remaining_capacity_wh == 18200.576
    #print(f'remaining_charge: {remaining_charge:,.2f}Wh  full_charge_capacity: {battery_charging.battery_full_charge_capacity_wh:,.2f}Wh   remaining_capacity: {battery_charging.battery_remaining_capacity_wh:,.2f}:Wh', flush=True)
    seconds = int(remaining_charge / battery_charging.charging * 3600) if battery_charging.charging else 0
    #print(f'remaining_charge: {remaining_charge:,}Wh  charging: {battery_charging.charging:,}W  seconds: {seconds}', flush=True)
    assert seconds == 6412
    assert remaining_charge == 2482.9140000000007

    result1 = battery_charging.fully_charged_at
    result4 = battery_discharging.fully_discharged_at
    assert result1.strftime('%d.%B.%Y %H:%M') == '24.May.2022 17:25'
    assert result4.strftime('%d.%B.%Y %H:%M') == '24.May.2022 17:25'

    assert battery_discharging.seconds_until_reserve == 1111
    assert battery_discharging.backup_reserve_at.strftime('%d.%B.%Y %H:%M')  == '24.May.2022 17:25'
