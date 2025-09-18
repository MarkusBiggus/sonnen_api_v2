"""Mock batterie response for config_flow."""

import datetime
from freezegun import freeze_time

from sonnen_api_v2 import BatterieResponse
#from .mock_sonnenbatterie_v2_charging import __mock_configurations

@freeze_time("20-11-2023 17:00:00.54321")
def __mock_batterieresponse(*args):
    """Mock BatterieResponse to validate token & update data response"""
    return BatterieResponse(
        version = '0.5.15',
        last_updated = datetime.datetime.now(),
        sensor_values = {}, # __mock_configurations(),
        package_build = '48'
    )
