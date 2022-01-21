from dataclasses import dataclass
from typing import Optional

from game import Status
from minesweeper import Minesweeper
from player import Player


@dataclass
class GameInfo(object):
    players: [Player]
    status: Status
    player_of_the_round: Optional[Player]
    minesweeper: Optional[Minesweeper]
