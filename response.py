from dataclasses import dataclass

from response_code import ResponseCode


@dataclass
class Response:
    response_code: ResponseCode
    body: any
