"""Mock batterie response for config_flow."""
import datetime
#import json
from sonnen_api_v2 import BatterieResponse
from .mock_sonnenbatterie_v2_charging import __mock_configurations

def __mock_batterieresponse(*args):
    """Mock BatterieResonse to validate token & update data response"""
    return BatterieResponse(
        version = '1.14.5',
        last_updated = datetime.datetime.now(),
        configurations = __mock_configurations()
    )
