# import queue
import threading
import time
# from multiprocessing import Queue
from typing import Optional
import queue

from dataclass.guess import Guess
from dataclass.player import Player
from enums.game_status import GameStatus
from exceptions.player_out_of_turn import PlayerOutOfTurn
from minesweeper import Minesweeper

PLAYER_QUEUE_SIZE = 4
QUEUE_WAITING_TIME = 15  # seconds

GUESS_WAITING_TIME = 20  # seconds
MAXIMUM_TOLERANCE_OF_LOST_ROUNDS = 1
WAIT_TO_RESTART = 15  # seconds


class Game(object):

    def __init__(self):
        self.__players = queue.Queue(maxsize=PLAYER_QUEUE_SIZE)
        self.__player_of_the_round: Optional[Player] = None
        self.__last_player_who_guessed: Optional[Player] = None
        self.__last_player_joined_in: time = None
        self.__last_player_interaction: time = None
        self.__minesweeper: Optional[Minesweeper] = None
        self.__status: GameStatus = GameStatus.waiting_players
        self.__aux_players: [Player] = list()
        self.__timeout_check = False
        self.__inactive_players: [Player] = list()
        self.__winner: Optional[Player] = None
        self.__changing = False

    @property
    def is_player_queue_full(self) -> bool:
        return self.__players.full()

    @property
    def is_player_queue_empty(self) -> bool:
        return self.__players.empty()

    @property
    def last_player_entry_time(self) -> time:
        return self.__last_player_joined_in

    @property
    def status(self) -> GameStatus:
        return self.__status

    @property
    def queueing_timeout(self):
        return self.__timeout(QUEUE_WAITING_TIME, self.__last_player_joined_in)

    @property
    def guessing_timeout(self):
        timeout = self.__timeout(GUESS_WAITING_TIME, self.__last_player_interaction)
        return timeout

    @property
    def players_as_tuple(self) -> tuple:
        return tuple(self.__aux_players)

    @property
    def minesweeper(self):
        return self.__minesweeper

    @property
    def inactive_players(self) -> list:
        return self.__inactive_players

    @property
    def winner(self) -> Optional[Player]:
        return self.__winner

    def add_player_to_queue(self, player: Player, reset_statistics=True):
        if self.__players.empty() and not GameStatus.running == self.status:
            thSt = threading.Thread(target=self.__start_game_if_requirements_met)
            thSt.start()

        self.__last_player_joined_in = time.time()
        if reset_statistics:
            self.__players.put(player.with_not_statistics(player.name))
            self.__aux_players.append(player.with_not_statistics(player.name))
        else:
            self.__players.put(player)
            self.__aux_players.append(player)

    def get_current_player(self, generate_if_none: bool = True) -> Player:
        if not generate_if_none:
            return self.__player_of_the_round

        if self.guessing_timeout or not self.__player_of_the_round or self.__last_player_who_guessed == \
                self.__player_of_the_round:
            self.__change_player()

        return self.__player_of_the_round

    def __change_player(self, by_timeout: bool = False, bomb_triggered: bool = False):
        self.__changing = True
        if self.__player_of_the_round is None:
            if self.is_player_queue_empty:
                self.__aux_players.clear()
            else:
                self.__player_of_the_round = self.__players.get()

            self.__update_guess_time()
        else:
            self.__aux_players = [p for p in self.__aux_players if p.name != self.__player_of_the_round.name]

            if by_timeout:
                self.__player_of_the_round.lost_rounds += 1
            else:
                self.__player_of_the_round.lost_rounds = 0

            if self.__player_of_the_round.lost_rounds > MAXIMUM_TOLERANCE_OF_LOST_ROUNDS or bomb_triggered:
                self.__inactive_players.append(self.__player_of_the_round)
            else:
                self.add_player_to_queue(self.__player_of_the_round, reset_statistics=False)

            if self.__players.empty():
                self.__aux_players.clear()
                self.__player_of_the_round = None
                if bomb_triggered:
                    self.__status = GameStatus.ended
            else:
                self.__player_of_the_round = self.__players.get()

            self.__update_guess_time()
        self.__changing = False

    def __is_player_turn(self, player: Player):
        p = self.get_current_player()
        return p is not None and p.name == player.name

    def take_guess(self, guess: Guess):
        self.__changing = True
        if not self.__is_player_turn(guess.player):
            err = "it is not your turn"
            raise PlayerOutOfTurn(err, err)

        self.__last_player_who_guessed = self.__player_of_the_round
        result = self.__minesweeper.verify_position(guess.line, guess.column)

        self.__player_of_the_round.score += result.score
        if result.bomb:
            self.__player_of_the_round.incorrect_guesses += 1
        else:
            self.__player_of_the_round.correct_guesses += 1

        if result.won:
            self.__on_board_cleared(result)
        else:
            self.__change_player(bomb_triggered=result.bomb)

        return result

    def __update_guess_time(self):
        if self.__player_of_the_round is None:
            self.__last_player_interaction = None
        else:
            self.__last_player_interaction = time.time()

    def __on_board_cleared(self, result):
        self.__winner = self.__player_of_the_round if result.won else None
        self.__players.put(self.__player_of_the_round)

        while not self.is_player_queue_empty:
            p = self.__players.get()
            self.__inactive_players.append(p)

    @staticmethod
    def __timeout(maximum_time: float, last_event_time: time) -> bool:
        if not last_event_time:
            return False

        diff = time.time() - last_event_time
        return diff >= maximum_time

    def start(self):
        self.__status = GameStatus.running
        self.__reset_queue_timeout()
        self.__minesweeper = Minesweeper(self.__players.qsize())
        self.__change_player()
        self.__start_guess_timeout_checker()
        self.__thread_restart()

    def __start_game_if_requirements_met(self):
        while self.status == GameStatus.waiting_players:
            if self.queueing_timeout or self.is_player_queue_full:
                self.start()

    def __reset_queue_timeout(self):
        self.__last_player_joined_in = None

    def __start_guess_timeout_checker(self):
        th_timeout: threading.Thread = threading.Thread(target=self.__pass_the_turn_if_inactive_player)
        th_timeout.start()

    def __restart_game(self):
        while True:
            if self.__status == GameStatus.ended or self.__status == GameStatus.ended_due_inactivity:
                time.sleep(WAIT_TO_RESTART)
                self.__players = queue.Queue(maxsize=PLAYER_QUEUE_SIZE)
                self.__player_of_the_round: Optional[Player] = None
                self.__last_player_who_guessed: Optional[Player] = None
                self.__last_player_joined_in: time = None
                self.__last_player_interaction: time = None
                self.__minesweeper: Optional[Minesweeper] = None
                self.__status: GameStatus = GameStatus.waiting_players
                self.__aux_players: [Player] = list()
                self.__timeout_check = False
                self.__aux_score = 0
                self.__inactive_players: [Player] = list()
                self.__winner: Optional[Player] = None
                break

    def __thread_restart(self):
        th_restart: threading.Thread = threading.Thread(target=self.__restart_game)
        th_restart.start()

    def __pass_the_turn_if_inactive_player(self):
        while GameStatus.running == self.status:
            if self.guessing_timeout:
                self.__change_player(True)
            if not self.__changing:
                if len(self.__aux_players) == 0 and self.status == GameStatus.running and \
                        self.__player_of_the_round is None and self.is_player_queue_empty:
                    self.__status = GameStatus.ended_due_inactivity
                    break
