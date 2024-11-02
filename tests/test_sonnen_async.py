import datetime
import os
from typing import Coroutine, Generator, Union
#import unittest
from unittest.mock import patch
import logging
#import pytest
#import aiohttp
#from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
import asyncio

from aioresponses.compat import AIOHTTP_VERSION, URL
from aioresponses import CallbackResult, aioresponses

from aiohttp import hdrs
from aiohttp import http
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse

#from freezegun import freeze_time
from sonnen_api_v2 import Sonnen
from dotenv import load_dotenv
from ddt import ddt, data
from .base import fail_on, AsyncTestCase #, skipIf

try:
    from aiohttp.errors import (
        ClientConnectionError,
        ClientResponseError,
        HttpProcessingError,
    )
except ImportError:
    from aiohttp.client_exceptions import (
        ClientConnectionError,
        ClientResponseError,
    )
    from aiohttp.http_exceptions import HttpProcessingError

from aioresponses.compat import AIOHTTP_VERSION, URL
from aioresponses import CallbackResult, aioresponses

load_dotenv()

BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')

LOGGER_NAME = "sonnenapiv2"


if BATTERIE_1_HOST == 'X':
    raise ValueError('Set BATTERIE_1_HOST & API_READ_TOKEN_1 in .env See env.example')

logging.getLogger("asyncio").setLevel(logging.WARNING)

    #value = web.AppKey("value", str)
    #    @responses.activate
    #    @aioresponses()
async def status_charging(request):
    test_data_status_charging = {
        'Apparent_output': 98,
        'BackupBuffer': '0',
        'BatteryCharging': True,
        'BatteryDischarging': False,
        'Consumption_Avg': 486,
        'Consumption_W': 403,
        'Fac': 50.05781555175781,
        'FlowConsumptionBattery': False,
        'FlowConsumptionGrid': False,
        'FlowConsumptionProduction': True,
        'FlowGridBattery': False,
        'FlowProductionBattery': True,
        'FlowProductionGrid': True,
        'GridFeedIn_W': 54,
        'IsSystemInstalled': 1,
        'OperatingMode': '2',
        'Pac_total_W': -95,
        'Production_W': 578,
        'RSOC': 98,
        'RemainingCapacity_Wh': 68781,
        'Sac1': 98,
        'Sac2': None,
        'Sac3': None,
        'SystemStatus': 'OnGrid',
        'Timestamp': '2022-04-30 17:00:58',
        'USOC': 98,
        'Uac': 245,
        'Ubat': 212,
        'dischargeNotAllowed': False,
        'generator_autostart': False
    }
    return web.Response(
        body = test_data_status_charging
    )

@ddt
class AIOResponsesTestCase(AsyncTestCase):
    async def setup(self):
        self._battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)  # Working and charging
        self.url = self._battery.status_api_url
        self.session = ClientSession()

    async def teardown(self):
        close_result = self.session.close()
        if close_result is not None:
            await close_result

    def run_async(self, coroutine: Union[Coroutine, Generator]):
        return self.loop.run_until_complete(coroutine)

    async def request(self, url: str):
        return await self.session.get(url)

    @data(
        hdrs.METH_HEAD,
        hdrs.METH_GET,
        hdrs.METH_POST,
        hdrs.METH_PUT,
        hdrs.METH_PATCH,
        hdrs.METH_DELETE,
        hdrs.METH_OPTIONS,
    )
    @patch('aioresponses.aioresponses.add')
    @fail_on(unused_loop=False)

    # @pytest.fixture
    # async def cli(aiohttp_client):
    #     app = web.Application()
    # #    app.router.add_get('http://' + BATTERIE_1_HOST + '/api/v2/status', status_charging)
    #     app.router.add_get('/api/v2/status', status_charging)
    #     return await aiohttp_client(app)

    @aioresponses()
    async def test_returned_response_headers(self, m):
        m.get(self.url,
            content_type='application/json',
            headers={'Connection': 'keep-alive'})
        response = await self.session.get(self.url)

        self.assertEqual(response.headers['Connection'], 'keep-alive')
        self.assertEqual(response.headers[hdrs.CONTENT_TYPE], 'application/json')

    @aioresponses()
    async def test_get_value(self):
#        battery = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)  # Working and charging
        self._battery.update()
        self.assertEqual(self._battery.grid_in, 54)

    #    cli.server.app[value] = 'bar'
        # resp = await cli.get('http://' + BATTERIE_1_HOST + '/api/v2/status')
        # assert resp.status == 200
        # assert await resp.text() == 'value: bar'

        # battery1_status = responses.Response(
        #     method='GET',
        #     url='http://' + BATTERIE_1_HOST + '/api/v2/status',
        #     status=200,
        #     json=test_data_status_charging
        # )
        # responses.add(battery1_status)

    #    self.battery_charging_working = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)  # Working and charging
    #    self.battery_discharging_working = Sonnen(API_READ_TOKEN_2, BATTERIE_2_HOST)  # Working and discharging - no logging
    #    self.battery_wrong_token_charging = Sonnen('notWorkingToken', BATTERIE_1_HOST, LOGGER_NAME)  # Wrong Token

    #    success = self.battery_charging_working.update()
    #    self.assertTrue(success)
        # success = self.battery_discharging_working.update()
        # self.assertTrue(success)
        # success = self.battery_wrong_token_charging.update()
        # self.assertFalse(success)

    # async def get_application(self):
    #     """
    #     Override the get_app method to return mocked application.
    #     """
    #     async def data_status_charging(request):
    #         return web.Response(text=self.test_data_status_charging)

    #     app = web.Application()
    #     app.router.add_get('http://' + BATTERIE_1_HOST + '/api/v2/status', data_status_charging)
    #     return app

    # @aioresponses()
    # async def test_charging(self):
    #     self.battery_charging_working = Sonnen(API_READ_TOKEN_1, BATTERIE_1_HOST, LOGGER_NAME)  # Working and charging
    #     async with self.client.request("GET", "/") as resp:
    #         self.assertEqual(resp.status, 200)
    #         text = await resp.text()
    #     result1 = self.battery_charging_working.charging
    # #    result4 = self.battery_discharging_working.charging
    #     self.assertEqual(result1, 1394)
    # #    self.assertEqual(result4, 0)
