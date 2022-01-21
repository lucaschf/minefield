import queue
import time
from enum import Enum
# from multiprocessing import Queue
from typing import Optional

from Exceptions import PlayerOutOfTurn
from minesweeper import Minesweeper
from player import Player

PLAYER_QUEUE_SIZE = 4
QUEUE_WATING_TIME = 5  # seconds
GUESS_WATING_TIME = 3  # seconds


class Status(Enum):
    waiting_players = 0
    running = 1
    ended = 2


class Game(object):

    def __init__(self):
        # self.__players = Queue(maxsize=PLAYER_QUEUE_SIZE)
        self.__players = queue.Queue(maxsize=PLAYER_QUEUE_SIZE)
        self.__player_of_the_round = None
        self.__last_player_who_guessed: Optional[Player] = None
        self.__last_player_joined_in: time = None
        self.__last_guess_received_at: time = None
        self.__minesweeper: Optional[Minesweeper] = None
        self.__status: Status = Status.waiting_players

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
    def players_as_list(self) -> []:
        player_list = []
        temp = queue.Queue(self.__players.qsize())

        while not self.__players.empty():
            p = self.__players.get_nowait()
            player_list.insert(len(player_list), p)
            temp.put_nowait(p)

        while not temp.empty():
            self.__players.put_nowait(temp.get_nowait())

        return player_list

    @property
    def minesweeper(self):
        return self.__minesweeper

    def add_player_to_queue(self, player: Player):
        self.__last_player_joined_in = time.time()
        self.__players.put_nowait(player.with_not_statistics(player.name))

    def get_current_player(self, generate_if_none: bool = True) -> Player:
        if not generate_if_none:
            return self.__player_of_the_round

        if self.guessing_timeout:
            self.__get_next_player_from_queue()
            self.__update_guess_time()
        else:
            if not self.__player_of_the_round:
                self.__get_next_player_from_queue()
            elif self.__last_player_who_guessed == self.__player_of_the_round:
                self.__get_next_player_from_queue()
                self.__update_guess_time()

        return self.__player_of_the_round

    def __get_next_player_from_queue(self):
        self.__player_of_the_round = self.__players.get_nowait()
        self.add_player_to_queue(self.__player_of_the_round)

    def __is_player_turn(self, player: Player):
        p = self.get_current_player()
        print("CURRENT PLAYER: " + p.name)
        return p.name == player.name

    def take_guess(self, player: Player, guess):
        if not self.__is_player_turn(player):
            err = f"it is {self.get_current_player().name}'s turn"
            raise PlayerOutOfTurn(err, err)
        else:
            # TODO  guess logic here
            self.__last_player_who_guessed = self.__player_of_the_round
            self.__get_next_player_from_queue()
            self.__update_guess_time()

        return self.__last_player_who_guessed

    def __update_guess_time(self):
        self.__last_guess_received_at = time.time()

    @staticmethod
    def __timeout(maximum_time: float, last_event_time: time) -> bool:
        if not last_event_time:
            return False

        diff = time.time() - last_event_time
        return diff >= maximum_time

    def start(self):
        self.__status = Status.running
        self.__update_guess_time()
        self.reset_queue_timeout()
        self.__minesweeper = Minesweeper(self.__players.qsize())
        # TODO ADD rest of logic here

    def reset_queue_timeout(self):
        self.__last_player_joined_in = None
