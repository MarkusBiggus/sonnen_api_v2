"""Mock battery configuration used as response to validate Auth"""

import responses
from . mock_sonnenbatterie_v2_charging import __mock_configurations

def __battery_configurations_auth200(self, _method:str, _url:str, _body, _headers:str, _retries):
    """Mock response to validate Auth """
    resp = responses.Response(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        json=__mock_configurations(),
        status=200,
        headers=_headers,
    )
    #print(f'resp: {resp.body}')
    return resp

def __battery_configurations_auth401(self, _method:str, _url:str, _body, _headers:str, _retries):
    """Mock response for invalid Auth """
    resp = responses.Response(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        status=401,
        headers=_headers,
    )
    return resp

def __battery_configurations_auth500(self, _method:str, _url:str, _body, _headers:str, _retries):
    """Mock response API error """
    resp = responses.Response(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        status=500,
        headers=_headers,
    )
    return resp
