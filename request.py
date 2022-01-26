from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dacite import from_dict, Config


class RequestCode(Enum):
    get_in_line = 0
    take_guess = 1
    game_status = 2


@dataclass
class Request:
    code: RequestCode
    body: any

    # noinspection DuplicatedCode
    def content(self, klass) -> Optional:
        if not self.body:
            return None

        if type(self.body) != dict:
            if type(self.body) != type(klass):
                raise AttributeError(f"Expected {klass} but got {type(self.body)} instead")

            return self.body

        return from_dict(data_class=klass, data=self.body, config=Config(cast=[RequestCode], check_types=False))
