from dataclasses import dataclass

from player import Player


@dataclass()
class Guess(object):
    player: Player
    line: int
    column: int
