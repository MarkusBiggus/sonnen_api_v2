""" SonnenAPI v2 Battery Response handler """

import json
import logging
#import sys
from collections import namedtuple
from typing import Any, Callable, Dict, Generator, Optional, Tuple, Union

import voluptuous as vol
from voluptuous import Invalid, MultipleInvalid
from voluptuous.humanize import humanize_error

from .units import SensorUnit
from .utils import PackerBuilderResult, contains_none_zero_value

__all__ = ("BatterieResponse")

from typing import Unpack

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class BatteryResponse(
    namedtuple(
        "BatteryResponse",
        [
            "data",
            # "dongle_serial_number",
            # "version",
            # "type",
            # "Battery_serial_number",
        ],
    )
):
    """ SonnenAPI v2 Battery Response data """
    # @property
    # def serial_number(self):
    #     return self.dongle_serial_number


_KEY_DATA = "data"
# _KEY_SERIAL = "sn"
# _KEY_VERSION = "version"
# _KEY_VER = "ver"
_KEY_TYPE = "type"


# GenericResponseSchema = vol.All(
# #    vol.Schema({vol.Required(_KEY_SERIAL): str}, extra=vol.ALLOW_EXTRA),
#     # vol.Any(
#     #     vol.Schema({vol.Required(_KEY_VERSION): str}, extra=vol.ALLOW_EXTRA),
#     #     vol.Schema({vol.Required(_KEY_VER): str}, extra=vol.ALLOW_EXTRA),
#     # ),
#     vol.Schema(
#         {
#             vol.Required(_KEY_TYPE): vol.Any(int, str),
#             vol.Required(_KEY_DATA): vol.Schema(contains_none_zero_value),
#         },
#         extra=vol.ALLOW_EXTRA,
#     ),
# )

ProcessorTuple = Tuple[Callable[[Any], Any], ...]
SensorIndexSpec = Union[int, PackerBuilderResult]
ResponseDecoder = Dict[
    str,
    Tuple[SensorIndexSpec, SensorUnit, Unpack[ProcessorTuple]],
]

JSONResponseSchema = vol.All(
    vol.Schema(
        {
            vol.Required(_KEY_TYPE): vol.Any(int, str),
            vol.Required(_KEY_DATA): vol.Schema(contains_none_zero_value),
        },
        extra=vol.ALLOW_EXTRA,
    ),
)


class ResponseParser:
    def __init__(
        self,
        schema: vol.Schema,
        decoder: ResponseDecoder,
        # dongle_serial_number_getter: Callable[[Dict[str, Any]], Optional[str]],
        # Battery_serial_number_getter: Callable[[Dict[str, Any]], Optional[str]],
    ) -> None:
        self.schema = vol.And(JSONResponseSchema, schema)
        self.response_decoder = decoder
        # self.dongle_serial_number_getter = dongle_serial_number_getter
        # self.Battery_serial_number_getter = Battery_serial_number_getter

    def _decode_map(self) -> Dict[str, SensorIndexSpec]:
        sensors: Dict[str, SensorIndexSpec] = {}
        for name, mapping in self.response_decoder.items():
            sensors[name] = mapping[0]
        return sensors

    def _postprocess_gen(
        self,
    ) -> Generator[Tuple[str, Callable[[Any], Any]], None, None]:
        """
        Return map of functions to be applied to each sensor value
        """
        for name, mapping in self.response_decoder.items():
            (_, _, *processors) = mapping
            for processor in processors:
                yield name, processor

    def map_response(self, resp_data) -> Dict[str, Any]:
        result = {}
        for sensor_name, decode_info in self._decode_map().items():
            if isinstance(decode_info, (tuple, list)):
                indexes = decode_info[0]
                packer = decode_info[1]
                values = tuple(resp_data[i] for i in indexes)
                val = packer(*values)
            else:
                val = resp_data[decode_info]
            result[sensor_name] = val
        for sensor_name, processor in self._postprocess_gen():
            result[sensor_name] = processor(result[sensor_name])
        return result

    def handle_response(self, resp: json) -> BatteryResponse:
        """
        Decode response and map array result using mapping definition.

        Args:
            resp (json): API response

        Returns:
            BatteryResponse: Mapped battery response.
        """

#        raw_json = resp.decode("utf-8").replace(",,", ",0.0,").replace(",,", ",0.0,")
        # json_response = {}
        # for key, value in json.loads(raw_json).items():
        #     json_response[key.lower()] = value

        try:
            response = self.schema(resp)
        except (Invalid, MultipleInvalid) as ex:
            _ = humanize_error(resp, ex)
            raise

        return BatteryResponse(
            data=self.map_response(response),
            # data=self.map_response(response[_KEY_DATA]),
            # dongle_serial_number=self.dongle_serial_number_getter(response),
            # version=response.get(_KEY_VER, response.get(_KEY_VERSION)),
            # type=response[_KEY_TYPE],
            # Battery_serial_number=self.Battery_serial_number_getter(response),
        )
