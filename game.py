from multiprocessing import Queue

from Exceptions import PlayerOutOfTurn
from player import Player

PLAYER_QUEUE_SIZE = 4


class Game(object):

    def __init__(self):
        self.__players = Queue(maxsize=PLAYER_QUEUE_SIZE)
        self.__player_of_the_round = None
        self.__last_player = None

    def is_player_queue_full(self):
        return self.__players.qsize() == PLAYER_QUEUE_SIZE

    @property
    def players_as_list(self) -> []:
        player_list = []
        temp = Queue(self.__players.qsize())

        while not self.__players.empty():
            p = self.__players.get_nowait()
            player_list.insert(len(player_list), p)
            temp.put_nowait(p)

        while not temp.empty():
            self.__players.put_nowait(temp.get_nowait())

        return player_list

    def add_player(self, player: Player):
        self.__players.put_nowait(player)

    def get_current_player(self) -> Player:
        if not self.__player_of_the_round:
            self.__player_of_the_round = self.__players.get_nowait()

        if not self.__last_player:
            return self.__player_of_the_round

        if self.__last_player == self.__player_of_the_round:
            self.__player_of_the_round = self.__players.get_nowait()

        return self.__player_of_the_round

    def __is_player_turn(self, player: Player):
        return self.get_current_player().name == player.name

    def take_guess(self, player: Player, guess):
        if not self.__is_player_turn(player):
            raise PlayerOutOfTurn(f"it is {self.get_current_player().name}'s turn",
                                  f"it is {self.get_current_player().name}'s turn")

        # TODO guess logic here
        self.__last_player = self.get_current_player()
        return player
