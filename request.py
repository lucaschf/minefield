from dataclasses import dataclass
from enum import Enum


class RequestCode(Enum):
    get_in_line = 0
    take_guess = 1
    game_status = 2


@dataclass
class Request:
    code: RequestCode
    body: any
