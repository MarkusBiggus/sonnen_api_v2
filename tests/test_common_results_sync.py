"""pytest tests/test_common_results_sync.py -s -v -x
3. Sync update called from sync method
"""
import datetime
from sonnen_api_v2 import Batterie
import pytest
from freezegun import freeze_time
import logging

from . import battery_charging_sync
from . import battery_discharging_sync

LOGGER_NAME = "sonnenapiv2"

@freeze_time("24-05-2022 15:38:23")
#@pytest.mark.usefixtures("battery_charging","battery_discharging")
#def test_check_common_results():
def test_common_results(battery_charging: Batterie, battery_discharging: Batterie):
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

    assert battery_discharging.status_battery_charging is False
    assert battery_discharging.status_battery_discharging is True


    result1 = battery_charging.consumption_average
    result2 = battery_discharging.consumption_average
    #    result3 = battery_wrong_token_charging.consumption_average
    assert result1 == 486
    assert result2 == 563
    #    assert result3 is None

    # @responses.activate
    # def test_consumption(self):
    result1 = battery_charging.consumption
    result2 = battery_discharging.consumption
    #    result3 = battery_wrong_token_charging.consumption
    assert result1 == 1578
    assert result2 == 1541
    #    assert result3 is None

    # @responses.activate
    # def test_installed_modules(self):
#    result1 = battery_charging.installed_modules
    #    result2 = battery_unreachable.installed_modules
    #    result3 = battery_wrong_token_charging.installed_modules
#    result4 = battery_discharging.installed_modules
#    assert result1 == 4
    #    assert result2 == 0
    #    assert result3 is None
#    assert result4 == 4

    # @responses.activate
    # def test_discharging(self):
    result1 = battery_charging.discharging
    #    result2 = battery_unreachable.discharging
    #    result3 = battery_wrong_token_charging.discharging
    result4 = battery_discharging.discharging
    assert result1 == 0
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 1439
    result1_pac = battery_charging.pac_total
    #    result2_pac = battery_unreachable.pac_total
    #    result3_pac = battery_wrong_token_charging.pac_total
    result4_pac = battery_discharging.pac_total
    assert result1_pac <= 0
    #    assert result2_pac == 0
    #    self.assertLessEqual(result3_pac is None
    assert result4_pac >= 0

    # @responses.activate
    # def test_charging(self):
    result1 = battery_charging.charging
    #    result2 = battery_unreachable.charging
    #    result3 = battery_wrong_token_charging.charging
    result4 = battery_discharging.charging
    assert result1 == 1394
    #    assert result2 == 0
    #    assert result3 == 0
    assert result4 == 0

    # @responses.activate
    # def test_grid_in(self):
    result1 = battery_charging.grid_in
    #    result2 = battery_unreachable.grid_in
    #    result3 = battery_wrong_token_charging.grid_in
    result4 = battery_discharging.grid_in
    assert result1 == 0
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 0

    # @responses.activate
    # def test_grid_out(self):
    result1 = battery_charging.grid_out
    #    result2 = battery_unreachable.grid_out
    #    result3 = battery_wrong_token_charging.grid_out
    result4 = battery_discharging.grid_out
    assert result1 >= 0
    #    self.assertGreaterEqual(result2 == 0
    #    assert result3 is None
    assert result4 == 20

    # @responses.activate
    # def test_production(self):
    result1 = battery_charging.production
    #    result2 = battery_unreachable.production
    #    result3 = battery_wrong_token_charging.production
    result4 = battery_discharging.production
    assert result1 == 2972
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 102

    # @responses.activate
    # def test_usoc(self):
    result1 = battery_charging.u_soc
    #    result2 = battery_unreachable.u_soc
    #    result3 = battery_wrong_token_charging.u_soc
    result4 = battery_discharging.u_soc
    assert result1 == 88
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 88

    # @responses.activate
    # def test_seconds_to_empty(self):
    result1 = battery_charging.seconds_to_empty
    #    result2 = battery_unreachable.seconds_to_empty
    #    result3 = battery_wrong_token_charging.seconds_to_empty
    result4 = battery_discharging.seconds_to_empty
    assert result1 == 0
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 45533

    # @responses.activate
    #@freeze_time("24-05-2022 15:38:23")
    #def test_fully_discharged_at(self):
    result1 = battery_charging.fully_discharged_at
    #    result2 = battery_unreachable.fully_discharged_at
    #    result3 = battery_wrong_token_charging.fully_discharged_at
    result4 = battery_discharging.fully_discharged_at
    assert result1 is None
    #    assert result2 == '00:00'
    #    assert result3 is None
    assert result4.strftime('%d.%B.%Y %H:%M') == '25.May.2022 04:17'

    # @responses.activate
    # @freeze_time("24-04-2022 15:38:23")
    # def test_seconds_since_full(self):
    result1 = battery_charging.seconds_since_full
    #    result2 = battery_unreachable.seconds_since_full
    #    result3 = battery_wrong_token_charging.seconds_since_full
    result4 = battery_charging.seconds_since_full
    assert result1 == 3720
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 3720

    # @responses.activate
    # def test_full_charge_capacity(self):
    result1 = battery_charging.full_charge_capacity
    #    result2 = battery_unreachable.full_charge_capacity
    #    result3 = battery_wrong_token_charging.full_charge_capacity
    result4 = battery_discharging.full_charge_capacity
    assert result1 == 20683
    #    assert result2 == 0
    #    assert result3 is None
    assert result4 == 20683

    # @responses.activate
    # @freeze_time('24-04-2022 15:38:23')
    # def test_time_since_full(self):
    result1 = battery_charging.time_since_full
    #    result2 = battery_unreachable.time_since_full
    #    result3 = battery_wrong_token_charging.time_since_full
    result4 = battery_discharging.time_since_full
    assert result1 == datetime.timedelta(seconds=3720)
    #    assert result2, datetime.timedelta(seconds=0))
    #    assert result3, datetime.timedelta(seconds=0))
    assert result4 == datetime.timedelta(seconds=574)

    # @responses.activate
    # @freeze_time('24-04-2022 15:38:23')
    # def test_seconds_until_fully_charged(self):
    remaining_charge = battery_charging.battery_full_charge_capacity_wh - battery_charging.battery_remaining_capacity_wh
    assert battery_charging.battery_full_charge_capacity_wh == 20683.49
    assert battery_charging.battery_remaining_capacity_wh == 18200.576
    #print(f'remaining_charge: {remaining_charge:,.2f}Wh  full_charge_capacity: {battery_charging.battery_full_charge_capacity_wh:,.2f}Wh   remaining_capacity: {battery_charging.battery_remaining_capacity_wh:,.2f}:Wh', flush=True)
    seconds = int(remaining_charge / battery_charging.charging * 3600) if battery_charging.charging else 0
    print(f'remaining_charge: {remaining_charge:,}Wh  charging: {battery_charging.charging:,}W  seconds: {seconds}', flush=True)
    assert seconds == 6412
    assert remaining_charge == 2482.9140000000007
    result1 = battery_charging.seconds_until_fully_charged
    #    result2 = battery_unreachable.seconds_until_fully_charged
    #    result3 = battery_wrong_token_charging.seconds_until_fully_charged
    result4 = battery_discharging.seconds_until_fully_charged
    assert result1 == 6412
    #    assert result2 == 0
    #    assert result3 == 0
    assert result4 is None

    # @responses.activate
    # @freeze_time('24-04-2022 15:38:23')
    # def test_fully_charged_at(self):
    result1 = battery_charging.fully_charged_at
    #    result2 = battery_unreachable.fully_charged_at
    #    result3 = battery_wrong_token_charging.fully_charged_at
    result4 = battery_discharging.fully_charged_at
    assert result1.strftime('%d.%B.%Y %H:%M') == '24.May.2022 16:38'
    #    assert result2 == 0
    #    assert result3 is None)
    assert result4 is None
