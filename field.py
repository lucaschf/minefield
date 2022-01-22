from dataclasses import dataclass
from xmlrpc.client import Boolean

@dataclass
class Field:
    bomb: Boolean
    positions: list
    won: Boolean
