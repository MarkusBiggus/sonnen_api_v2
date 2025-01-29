import datetime
from sonnen_api_v2 import Batterie

def check_charge_results(battery_charging: Batterie):
    """Common results for each method of updating
        Batterie object from network device
    """
    assert battery_charging.status_battery_charging is True
    assert battery_charging.status_battery_discharging is False
    assert battery_charging.system_status == 'OnGrid'
    assert battery_charging.consumption_average == 486
    assert battery_charging.consumption == 1578
    assert battery_charging.kwh_consumed == 816.5
    assert battery_charging.kwh_produced == 3969.80
    assert battery_charging.installed_modules == 4
    assert battery_charging.discharging == 0
    assert battery_charging.pac_total <= 0
    assert battery_charging.charging == 1394
    assert battery_charging.grid_in == 0
    assert battery_charging.grid_out >= 0
    assert battery_charging.production == 2972
    assert battery_charging.u_soc == 81
    assert battery_charging.r_soc == 88
    assert battery_charging.status_rsoc == 88
    assert battery_charging.status_usoc == 81
    assert battery_charging.fully_discharged_at is None
    assert battery_charging.seconds_since_full == 3720
    assert battery_charging.battery_full_charge_capacity_wh == 20683.49
    assert battery_charging.full_charge_capacity == 20683.49
    assert battery_charging.time_since_full == datetime.timedelta(seconds=3720)
    assert battery_charging.battery_remaining_capacity_wh == 18200.6
    assert battery_charging.status_remaining_capacity_wh == 18201.5
    assert battery_charging.status_usable_capacity_wh == 16753.6
    assert battery_charging.used_capacity_wh == 2482.0
    assert battery_charging.seconds_until_fully_charged == 2673
    assert battery_charging.fully_charged_at.strftime('%d.%b.%Y %H:%M') == '20.Nov.2023 17:44'
    assert battery_charging.seconds_until_reserve is None
    assert battery_charging.battery_activity_state == 'charging'

def check_discharge_results(battery_discharging: Batterie):
    assert battery_discharging.seconds_until_reserve == 38833
    assert battery_discharging.backup_reserve_at.strftime('%d.%b.%Y %H:%M')  == '21.Nov.2023 03:48'
    assert battery_discharging.seconds_until_fully_discharged == 49189
    assert battery_discharging.fully_discharged_at.strftime('%d.%b.%Y %H:%M') == '21.Nov.2023 06:40'
    assert battery_discharging.battery_full_charge_capacity_wh == 20683.49
    assert battery_discharging.battery_remaining_capacity_wh == 18200.6
    assert battery_discharging.backup_buffer_capacity_wh ==  4136.7
    assert battery_discharging.capacity_until_reserve == 14063.9
    assert battery_discharging.status_remaining_capacity_wh == 18201.5
    assert battery_discharging.status_usable_capacity_wh == 16753.6
    assert battery_discharging.seconds_since_full == 574
    assert battery_discharging.time_since_full == datetime.timedelta(seconds=574)
    assert battery_discharging.battery_full_charge_capacity == 201.98
    assert battery_discharging.r_soc == 88
    assert battery_discharging.u_soc == 81
    assert battery_discharging.status_rsoc == 88
    assert battery_discharging.status_usoc == 81
    assert battery_discharging.production == 103
    assert battery_discharging.grid_out == 0
    assert battery_discharging.charging == 0
    assert battery_discharging.grid_in == 0
    assert battery_discharging.pac_total >= 0
    assert battery_discharging.discharging == 1438
    assert battery_discharging.installed_modules == 4
    assert battery_discharging.consumption == 1541
    assert battery_discharging.consumption_average == 1563
    assert battery_discharging.kwh_consumed == 816.5
    assert battery_discharging.kwh_produced == 3969.80
    assert battery_discharging.status_battery_charging is False
    assert battery_discharging.status_battery_discharging is True
    assert battery_discharging.system_status == 'OnGrid'
    assert battery_discharging.battery_activity_state == 'discharging'

def check_reserve_results(battery_discharging_reserve: Batterie):
    assert battery_discharging_reserve.battery_full_charge_capacity == 201.98
    assert battery_discharging_reserve.status_remaining_capacity_wh == 3723.0
    assert battery_discharging_reserve.seconds_since_full == 2574
    assert battery_discharging_reserve.time_since_full == datetime.timedelta(seconds=2574)
    assert battery_discharging_reserve.battery_full_charge_capacity_wh == 20683.49
    assert battery_discharging_reserve.used_capacity_wh == 16960.5
    assert battery_discharging_reserve.battery_remaining_capacity_wh == 3722.9 # 5170.7
    assert battery_discharging_reserve.battery_unusable_capacity_wh == 1447.8
    assert battery_discharging_reserve.status_usable_capacity_wh == 2275.2
    assert battery_discharging_reserve.battery_usable_remaining_capacity_wh == 2275.1
    assert battery_discharging_reserve.used_capacity_wh + battery_discharging_reserve.battery_remaining_capacity_wh == 20683.4 # 20683.49
    assert battery_discharging_reserve.backup_buffer_capacity_wh == 4136.7
    assert battery_discharging_reserve.backup_buffer_usable_capacity_wh == 2688.9 # ? 3436.7
    assert battery_discharging_reserve.seconds_until_fully_discharged == 9320
    assert battery_discharging_reserve.capacity_to_reserve == 413.8
    assert battery_discharging_reserve.fully_discharged_at.strftime('%d.%b.%Y %H:%M') == '20.Nov.2023 19:36'
    assert battery_discharging_reserve.using_reserve is True
    assert battery_discharging_reserve.capacity_until_reserve is None
    assert battery_discharging_reserve.seconds_until_reserve is None
    assert battery_discharging_reserve.backup_reserve_at is None
    assert battery_discharging_reserve.r_soc == 18
    assert battery_discharging_reserve.u_soc == 11
    assert battery_discharging_reserve.status_rsoc == 18
    assert battery_discharging_reserve.status_usoc == 11
    assert battery_discharging_reserve.production == 103
    assert battery_discharging_reserve.grid_out == 0
    assert battery_discharging_reserve.pac_total >= 0
    assert battery_discharging_reserve.discharging == 1438
    assert battery_discharging_reserve.consumption == 1541
    assert battery_discharging_reserve.consumption_average == 1563
    assert battery_discharging_reserve.status_battery_charging is False
    assert battery_discharging_reserve.status_battery_discharging is True
    assert battery_discharging_reserve.system_status == 'OffGrid'
    assert battery_discharging_reserve.battery_activity_state == 'discharging reserve'
