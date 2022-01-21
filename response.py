from dataclasses import dataclass

from enum import Enum


class ResponseCode(Enum):
    BAD_REQUEST = -1
    UNSUPPORTED = 0
    OK = 1
    ERROR = 2
    DENIED = 3


@dataclass
class Response:
    response_code: ResponseCode
    body: any
