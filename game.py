# import queue
import threading
import time
from enum import Enum
from multiprocessing import Queue
from typing import Optional

from Exceptions import PlayerOutOfTurn
from minesweeper import Minesweeper
from player import Player

PLAYER_QUEUE_SIZE = 4
QUEUE_WATING_TIME = 10  # seconds
GUESS_WATING_TIME = 3  # seconds


class Status(Enum):
    waiting_players = 0
    running = 1
    ended = 2


class Game(object):

    def __init__(self):
        self.__players = Queue(maxsize=PLAYER_QUEUE_SIZE)
        # self.__players = queue.Queue(maxsize=PLAYER_QUEUE_SIZE)
        self.__player_of_the_round = None
        self.__last_player_who_guessed: Optional[Player] = None
        self.__last_player_joined_in: time = None
        self.__last_guess_received_at: time = None
        self.__minesweeper: Optional[Minesweeper] = None
        self.__status: Status = Status.waiting_players
        self.__aux_players: {Player} = set()

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
    def status(self) -> Status:
        return self.__status

    @property
    def queueing_timeout(self):
        return self.__timeout(QUEUE_WATING_TIME, self.__last_player_joined_in)

    @property
    def guessing_timeout(self):
        timeout = self.__timeout(GUESS_WATING_TIME, self.__last_guess_received_at)
        return timeout

    @property
    def players_as_tuple(self) -> tuple:
        s = tuple(self.__aux_players)
        print(type(s), " ", s)
        return s

    @property
    def minesweeper(self):
        return self.__minesweeper

    def add_player_to_queue(self, player: Player):
        if self.__players.empty():
            thSt = threading.Thread(target=self.start_game_if_requirements_met)
            thSt.start()

        self.__last_player_joined_in = time.time()
        self.__players.put_nowait(player.with_not_statistics(player.name))
        print("TUPLA ANTES", self.__aux_players)
        self.__aux_players.add(player)
        print("TUPLA DEPOIS", self.__aux_players)

    def get_current_player(self, generate_if_none: bool = True) -> Player:
        if not generate_if_none:
            return self.__player_of_the_round

        if self.guessing_timeout or not self.__player_of_the_round or self.__last_player_who_guessed == \
                self.__player_of_the_round:
            self.__get_player_of_the_turn()

        # if self.guessing_timeout:
        #     self.__get_player_of_the_turn()
        # else:
        #     if not self.__player_of_the_round:
        #         self.__get_player_of_the_turn()
        #     elif self.__last_player_who_guessed == self.__player_of_the_round:
        #         self.__get_player_of_the_turn()

        return self.__player_of_the_round

    def __get_player_of_the_turn(self, timeout: bool = False):
        if not self.__players.empty():
            self.__player_of_the_round = self.__players.get_nowait()

            if not timeout:
                self.add_player_to_queue(self.__player_of_the_round)
            else:
                ls_aux = list(self.__aux_players)
                ls_aux.remove(self.__player_of_the_round)
                self.__aux_players = tuple(ls_aux)

            self.__start_guess_timeout_checker()
        else:
            self.__player_of_the_round = None

        self.__update_guess_time()

    def __is_player_turn(self, player: Player):
        p = self.get_current_player()
        return p is not None and p.name == player.name

    def take_guess(self, player: Player, guess):
        if not self.__is_player_turn(player):
            err = "it is not your turn"
            raise PlayerOutOfTurn(err, err)
        else:
            # TODO  guess logic here
            self.__last_player_who_guessed = self.__player_of_the_round
            self.__get_player_of_the_turn()

        return self.__last_player_who_guessed

    def __update_guess_time(self):
        if self.__player_of_the_round is None:
            self.__last_guess_received_at = None
        else:
            self.__last_guess_received_at = time.time()

    @staticmethod
    def __timeout(maximum_time: float, last_event_time: time) -> bool:
        if not last_event_time:
            return False

        diff = time.time() - last_event_time
        return diff >= maximum_time

    def start(self):
        self.__status = Status.running
        self.reset_queue_timeout()
        self.__minesweeper = Minesweeper(self.__players.qsize())
        self.__get_player_of_the_turn()

    def start_game_if_requirements_met(self):
        while self.status == Status.waiting_players:
            if self.queueing_timeout or self.is_player_queue_full:
                self.start()

    def reset_queue_timeout(self):
        self.__last_player_joined_in = None

    def __start_guess_timeout_checker(self):
        th_timeout: threading.Thread = threading.Thread(target=self.__pass_the_turn_if_inactive_player,
                                                        args=[self.__player_of_the_round])
        th_timeout.start()

    def __pass_the_turn_if_inactive_player(self, expected_player: Player):
        while self.__player_of_the_round is not None and self.__player_of_the_round == expected_player:
            if self.guessing_timeout:
                print("TIMED OUT FOR", self.__player_of_the_round.name)
                self.__get_player_of_the_turn(True)
                print("NEW PLATER")
                print(self.__player_of_the_round)
