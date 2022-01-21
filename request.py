from dataclasses import dataclass

from request_code import RequestCode


@dataclass
class Request:
    code: RequestCode
    body: any
