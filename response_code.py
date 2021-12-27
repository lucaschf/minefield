import json
from enum import Enum


class ResponseCode(Enum):
    BAD_REQUEST = -1
    UNSUPPORTED = 0
    OK = 1
    ERROR = 2
    DENIED = 3


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)
