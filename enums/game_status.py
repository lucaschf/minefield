from enum import Enum


class GameStatus(Enum):
    waiting_players = 0
    running = 1
    ended = 2
    ended_due_inactivity = 3
