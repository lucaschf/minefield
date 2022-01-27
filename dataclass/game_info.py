from dataclasses import dataclass
from typing import Optional

from dataclass.minesweeper_DTO import MinesweeperDTO
from dataclass.player import Player
from game import GameStatus


@dataclass(unsafe_hash=True)
class GameInfo(object):
    status: GameStatus
    players: tuple[Player]
    player_of_the_round: Optional[Player]
    minesweeper: Optional[MinesweeperDTO]


@dataclass(unsafe_hash=True)
class PlayerQueueInfo:
    players: tuple[Player]
