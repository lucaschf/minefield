from dataclasses import dataclass


@dataclass
class MinesweeperDTO(object):
    config: dict
    coordinates: tuple
