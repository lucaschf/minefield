from dataclasses import dataclass


@dataclass
class Player(object):
    name: str
    score: float
    correct_guesses: int
    incorrect_guesses: int
