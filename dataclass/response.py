from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ResponseCode(Enum):
    BAD_REQUEST = -1
    UNSUPPORTED = 0
    OK = 1
    ERROR = 2
    DENIED = 3


@dataclass
class Response:
    response_code: ResponseCode
    body: Optional[dict]
    error_body: Optional[str] = None

    def is_ok_response(self) -> bool:
        return self.response_code == ResponseCode.OK


def bad_request_response(error_message: str = "Bad request") -> Response:
    return Response(ResponseCode.BAD_REQUEST, None, error_message)


def error_response(error_message: str = "Unable to handle request") -> Response:
    return Response(ResponseCode.ERROR, None, error_message)


def ok_response(response_body: any, error_message: str = None) -> Response:
    return Response(ResponseCode.OK, response_body, error_message)


def denied_response(error_message: str = "Denied", errorbody=None) -> Response:
    return Response(ResponseCode.DENIED, errorbody, error_message)


def unsupported_response(error_message: str = "Unsupported operation", errorbody=None) -> Response:
    return Response(ResponseCode.UNSUPPORTED, errorbody, error_message)
