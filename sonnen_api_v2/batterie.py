"""Batterie API response mapping"""
#from typing import Any, Dict, Optional

import voluptuous as vol

#from solax.inverter import Inverter
from sonnen_api_v2.units import Units # ,DailyTotal, Total
from sonnen_api_v2.utils import div1K

class Batterie_Status:
    """Define API endpoint response maps
    """

    # pylint: disable=duplicate-code
    _schema = vol.Schema(
        {
            vol.Required("version"): str,
            vol.Required("data"): vol.Schema(
                vol.All(
                    [vol.Coerce(float)],
                    vol.Length(min=200, max=200),
                )
            ),
        },
        extra=vol.REMOVE_EXTRA,
    )

    @classmethod
    def response_decoder(cls):
        return {
            'Apparent_output': (1, Units.W), #98,
            'BackupBuffer': (2, Units.PERCENT), #'20',
            'BatteryCharging': (3, Units.NONE), #True,
            'BatteryDischarging': (4, Units.NONE), #False,
            'Consumption_Avg': (5, Units.W), #486,
            'Consumption_W': (6, Units.W), #403,
            'Fac': (7, Units.HZ), #50.05781555175781,
#            'FlowConsumptionBattery': (1, Units.NONE), #False,
#            'FlowConsumptionGrid': (1, Units.NONE), #False,
#            'FlowConsumptionProduction': (1, Units.NONE), #True,
#            'FlowGridBattery': (1, Units.NONE), #False,
#            'FlowProductionBattery': (1, Units.NONE), #True,
#            'FlowProductionGrid': (1, Units.NONE), #True,
            'GridFeedIn_W': (7, Units.W), #54,
            'IsSystemInstalled': (8, Units.NONE), #1,
            'OperatingMode': (9, Units.NONE), #'2',
            'Pac_total_W': (10, Units.W), #-95,
            'Production_W': (11, Units.W), #578,
            'RSOC': (12, Units.PERCENT), #98,
            'RemainingCapacity_Wh': (13, Units.KWH, div1K), #68781,
            'Sac1': (14, Units.PERCENT), #98,
            'Sac2': (15, Units.PERCENT), #None,
            'Sac3': (16, Units.PERCENT), #None,
            'SystemStatus': (17, Units.NONE), #'OnGrid',
            'Timestamp': (18, Units.NONE), #'2022-04-30 17:00:58',
            'USOC': (19, Units.PERCENT), #98,
            'Uac': (20, Units.V), #245,
            'Ubat': (21, Units.V), #212,
            'dischargeNotAllowed': (22, Units.NONE), #False,
            'generator_autostart': (23, Units.NONE), #False

        }

    # pylint: enable=duplicate-code

#    @classmethod
#    def inverter_serial_number_getter(cls, response: Dict[str, Any]) -> Optional[str]:
#        return response["information"][2]
