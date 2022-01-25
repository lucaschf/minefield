from dataclasses import dataclass
from typing import Optional

from game import Status
from player import Player


@dataclass(unsafe_hash=True)
class GameInfo(object):
    players: tuple[Player]
    status: Status
    player_of_the_round: Optional[Player]
    # minesweeper: Optional[Minesweeper]


@dataclass(unsafe_hash=True)
class PlayerQueueInfo:
    players: tuple[Player]
