from dataclasses import dataclass

from dataclass.game_info import GameInfo


@dataclass
class GuessResult:
    bomb: bool
    positions: list
    won: bool
    score: int
    game_info: GameInfo = None
