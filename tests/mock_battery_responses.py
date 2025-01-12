"""Mock battery configuration as response to validate Auth"""

from urllib3 import HTTPResponse
from . mock_sonnenbatterie_v2_charging import __mock_configurations
import json

def __battery_auth200(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response to validate Auth."""
    resp = HTTPResponse(
        request_method=_method, #'GET',
        request_url=_url,
        body=json.dumps(__mock_configurations()),
        status=200,
        headers=_headers,
    )
    #print(f'resp: {resp._body}')
    return resp

def __battery_AuthError_401(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response for invalid Auth."""
    resp = HTTPResponse(
        request_method=_method, #'GET',
        request_url=_url,
        status=401,
        headers=_headers,
    )
    return resp

def __battery_AuthError_403(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response for invalid Auth.
        Fake forbidden token returns status 403.
    """
    resp = HTTPResponse(
        request_method=_method, #'GET',
        request_url=_url,
        status=403,
        headers=_headers,
    )
    return resp

def __battery_HTTPError_301(self, _method:str, _url:str, _body, _headers:str, _retries, **kwargs):
    """Mock response API error."""
    resp = HTTPResponse(
        request_method=_method, #'GET',
        request_url=_url,
        status=301,
        headers=_headers,
    )
    return resp
