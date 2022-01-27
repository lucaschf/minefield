from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Player(object):
    name: str
    score: float
    correct_guesses: int
    incorrect_guesses: int
    lost_rounds: int

    @property
    def reset_stattiscs(self):
        self.incorrect_guesses = 0
        self.correct_guesses = 0
        self.score = 0
        self.lost_rounds = 0
        return self

    def clone(self):
        return Player(self.name, self.score, self.correct_guesses, self.incorrect_guesses, self.lost_rounds)

    @staticmethod
    def with_not_statistics(name: str):
        return Player(name, 0, 0, 0, 0)
