from dataclasses import dataclass
from typing import Optional

from dataclass.minesweeper_DTO import MinesweeperDTO
from dataclass.player import Player
from enums.game_status import GameStatus


@dataclass(unsafe_hash=True)
class GameInfo(object):
    status: GameStatus
    players: tuple
    player_of_the_round: Optional[Player]
    minesweeper: Optional[MinesweeperDTO]
    inactive_players: set
    winner: Optional[Player]


@dataclass(unsafe_hash=True)
class PlayerQueueInfo:
    players: list
