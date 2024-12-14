import datetime
from sonnen_api_v2.sonnen import Sonnen as Batterie
import pytest
from freezegun import freeze_time
@freeze_time("24-05-2022 15:38:23")
# @pytest.fixture
def check_results(battery_charging: Batterie, battery_discharging: Batterie, battery_discharging_reserve: Batterie = None):
    """Common results for each method of updating
        Batterie object from network device
    """
    assert battery_charging.status_battery_charging is True
    assert battery_charging.status_battery_discharging is False
    assert battery_charging.system_status == 'OnGrid'

    assert battery_discharging.status_battery_charging is False
    assert battery_discharging.status_battery_discharging is True
    assert battery_discharging.system_status == 'OnGrid'

    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.status_battery_charging is False
        assert battery_discharging_reserve.status_battery_discharging is True
        assert battery_discharging_reserve.system_status == 'OffGrid'

    assert battery_charging.consumption_average == 486
    assert battery_discharging.consumption_average == 563
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.consumption_average == 563

    assert battery_charging.consumption == 1578
    assert battery_discharging.consumption == 1541

    assert battery_charging.installed_modules == 4
    assert battery_discharging.installed_modules == 4

    assert battery_charging.discharging == 0
    assert battery_discharging.discharging == 1439
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.discharging == 1439

    assert battery_charging.pac_total <= 0
    assert battery_discharging.pac_total >= 0
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.pac_total >= 0

    assert battery_charging.charging == 1394
    assert battery_discharging.charging == 0

    assert battery_charging.grid_in == 0
    assert battery_discharging.grid_in == 0

    assert battery_charging.grid_out >= 0
    assert battery_discharging.grid_out == 20
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.grid_out == 0

    assert battery_charging.production == 2972
    assert battery_discharging.production == 102
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.production == 102

    assert battery_charging.u_soc == 88
    assert battery_discharging.u_soc == 88
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.u_soc == 18

    assert battery_charging.r_soc == 88
    assert battery_discharging.r_soc == 88
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.r_soc == 18

    assert battery_charging.seconds_until_fully_charged == 6412
    assert battery_discharging.seconds_until_reserve == 35185
    assert battery_discharging.seconds_until_fully_discharged == 45533
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.seconds_until_fully_discharged == 9314

    assert battery_charging.fully_discharged_at is None
    assert battery_discharging.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '24.May.2022 18:13'

    assert battery_charging.seconds_since_full == 3720
    assert battery_discharging.seconds_since_full == 574
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.seconds_since_full == 2574

    assert battery_charging.full_charge_capacity == 20683
    assert battery_discharging.full_charge_capacity == 20683

    assert battery_charging.time_since_full == datetime.timedelta(seconds=3720)
    assert battery_discharging.time_since_full == datetime.timedelta(seconds=574)
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.time_since_full == datetime.timedelta(seconds=2574)

    remaining_charge_to_full = battery_charging.battery_full_charge_capacity_wh - battery_charging.battery_remaining_capacity_wh
    assert remaining_charge_to_full == 2482.9140000000007

    assert battery_charging.battery_full_charge_capacity_wh == 20683.49
    assert battery_charging.battery_remaining_capacity_wh == 18200.576
    #print(f'remaining_charge_to_full: {remaining_charge_to_full:,.2f}Wh  full_charge_capacity: {battery_charging.battery_full_charge_capacity_wh:,.2f}Wh   remaining_capacity: {battery_charging.battery_remaining_capacity_wh:,.2f}:Wh', flush=True)
    assert battery_discharging.battery_remaining_capacity_wh == 18200.576
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.battery_remaining_capacity_wh == 3723.264


    assert battery_charging.fully_charged_at.strftime('%d.%B.%Y %H:%M') == '24.May.2022 17:25'

    assert battery_discharging.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'
    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.fully_discharged_at.strftime('%d.%B.%Y %H:%M') == '24.May.2022 18:13'

    assert battery_charging.seconds_until_reserve is None
    assert battery_discharging.seconds_until_reserve == 35185
    assert battery_discharging.backup_reserve_at.strftime('%d.%B.%Y %H:%M')  == '25.May.2022 01:24'

    if battery_discharging_reserve is not None:
        assert battery_discharging_reserve.seconds_until_reserve is None #-1032
        assert battery_discharging_reserve.backup_reserve_at is None # .strftime('%d.%B.%Y %H:%M')  == '24.May.2022 17:25'
