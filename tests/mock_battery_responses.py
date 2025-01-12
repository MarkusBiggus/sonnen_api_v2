"""Mock battery configuration used as response to validate Auth"""
from urllib3 import HTTPResponse
import responses
from . mock_sonnenbatterie_v2_charging import __mock_configurations
import json

def __battery_configurations_auth200(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response to validate Auth """
    resp = HTTPResponse(
        request_method=_method, #'GET',
        request_url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        body=json.dumps(__mock_configurations()),
        status=200,
        headers=_headers,
    )
    #print(f'resp: {resp.body}')
    return resp

def __battery_configurations_auth401(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response for invalid Auth """
    resp = HTTPResponse(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        status=401,
        headers=_headers,
    )
    return resp

def __battery_configurations_auth500(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response API error """
    resp = HTTPResponse(
        method=_method, #'GET',
        url=_url, #(f'http://fakeHost:80/api/v2/configurations'),
        status=500,
        headers=_headers,
    )
    return resp
