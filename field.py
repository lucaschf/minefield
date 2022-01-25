from dataclasses import dataclass

@dataclass
class Field:
    bomb: bool
    positions: list
    won: bool
