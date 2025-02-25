# Sonnen API v2 package
Sonnen batterie API v2 fetcher

Requires API read token generated by Sonnen batterie management portal.

Does not use the default user login to authenticate API, only the token.

Parameters to run tests for batterie IP address and API token are specified in .env file. See env.example for template.

Token & IP can be validated after creating Batterie object.
This is achieved by fetching configuration details and raising errors depending on
error or status returned from usrllib3.

    from sonnen_api_v2 import Batterie, BatterieAuthError, BatterieError, BatterieHTTPError

    battery_charging = Batterie('fakeToken', 'fakeHost')
    try:
        success = battery_discharging.sync_validate_token()
    except BatterieAuthError as error:
        print('Token or IP are not valid')
    except BatterieHTTPError as error:
        print('HTTP error status not in [401, 403]')
    except BatterieError as error:
        print('Connection error accessing Batterie API endpoint')

    assert success is not False


There are three ways to update from the Batterie:

1. Async caller uses Async update

        def async async_caller()
            batterie = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)
            success = batterie.async_update()

    Test:
    see battery_charging_asyncio & test_common_results_asyncio


2.  Sync caller uses Async update

        def sync_caller()
            batterie = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)
            success = batterie.update()

    Test:
    see battery_charging_sync & test_common_results_sync


3. Async caller uses sync update from coroutine passed to asyncio.run_in_executor (ha emulation)

        async def _async_update_data(self):
            result = await asyncio.async_add_executor_job(
                self.sync_caller
            )
        def sync_caller()
            batterie = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_HOST_PORT, LOGGER_NAME)
            success = batterie.sync_update()

    Test:
    see battery_charging_coroutine & test_common_results_coroutine



Variation #3 use case is Home Assistant custom_component sonnenbackup


Within a Home Assistant integration:

```
from sonnen_api_v2 import BatterieBackup, BatterieResponse,
import asyncio

async def validate() -> BatterieResponse:
    _batterie = BatterieBackup(auth_token, ip_address, port)
    return await _batterie.validate_token()

async def update() -> BatterieResponse:
    _batterie = BatterieBackup(auth_token, ip_address, port)
    return await _batterie.refresh_response()


# hass will call from its running event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
response = loop.run_until_complete(update())

assert isinstance(response, BatterieResponse) is True
```
