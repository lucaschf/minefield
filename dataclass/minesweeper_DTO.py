from dataclasses import dataclass


@dataclass
class MinesweeperDTO(object):
    config: dict
    coordinates: tuple
    # TODO include all needed attributes
