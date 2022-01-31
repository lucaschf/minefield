import socket
import time

import jsonpickle

from dataclass.guess import Guess
from dataclass.player import Player
from dataclass.request import Request
from dataclass.request import RequestCode
from dataclass.response import Response
from game import QUEUE_WAITING_TIME, GUESS_WAITING_TIME
from helpers.socket_helpers import send_data, receive_data, SERVER_PORT


class GameClient(object):

    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

    def __create_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_address, self.__server_port))
        return sock

    def __send_request(self, args: Request):
        sock = self.__create_connection()
        send_data(jsonpickle.encode(args), sock)

        response = receive_data(sock)
        # print(response)
        sock.close()

        return jsonpickle.decode(response)

    def request_queue_entry(self, player_name: str) -> Response:
        """ Sends a request to add a new player to the queue.

            :parameter
                player_name (str): the target player name

            :returns
                Response ('~Response'): A reponse with a response code and a result body:

                OK -> The request was sucessfully answered;
                body -> list of all players in the queue sorted by order of entry;
                error_body -> None.

                DENIED -> If the queue is already full or the game has already started;
                body -> None;
                error_body -> str message with the reason for denial.

                BAD_REQUEST-> If the request data is invalid such as player already in the queue or empty name;
                body -> None.
                error_body -> str message with the error.

                ERROR -> If there is an error processing the request.
                body -> None
                error_body -> str message with the error.
         """
        return self.__send_request(Request(RequestCode.get_in_line, Player.with_not_statistics(player_name)))

    def request_game_status(self) -> Response:
        """ Sends a request to get the running game info.

            :returns
                Response ('~Response'): A reponse with a response code and a result body:

                OK -> The request was sucessfully answered;
                body -> ('~GameInfo') containg all game info;
                error_body -> None

                ERROR -> If there is an error processing the request.
                body -> None;
                error_body -> str message with the error.
         """
        return self.__send_request(Request(RequestCode.game_status, None))

    def request_take_guess(self, guess: Guess) -> Response:
        return self.__send_request(Request(RequestCode.take_guess, guess))
