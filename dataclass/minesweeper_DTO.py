from dataclasses import dataclass


@dataclass
class MinesweeperDTO(object):
    board_config: dict
    coordinates: tuple
    board: tuple
    # TODO include all needed attributes
