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
        print(response)
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


if __name__ == "__main__":
    # TODO change ip address to server. Currently used this way since is programmed in same machine using DHCP
    h_name = socket.gethostname()
    RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)

    client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)

    # USAGE EXAMPLES

    # 1 add player to queue
    #
    # Ok Response
    print("CASE 1 - add player to queue - should return OK")
    result = client.request_queue_entry("Iasmina")
    # print("I: ", result)
    if result.is_ok_response():
        player_queue = result.body
        print("I: ", player_queue)
    else:
        print("E: ", result.error_body)

    print("CASE 1 - add player to queue - should return OK")
    result = client.request_queue_entry("Iasmina2")
    # print("I: ", result)
    if result.is_ok_response():
        player_queue = result.body
        print("I: ", player_queue)
    else:
        print("E: ", result.error_body)

    # OK Response with game ended due innactivity
    time.sleep(QUEUE_WAITING_TIME)
    print("\nCASE 3 - Get game status Info")
    result = client.request_game_status()
    # print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.body)
    else:
        print("E: ", result.error_body)

    time.sleep(GUESS_WAITING_TIME)
    # OK Response with game ended due innactivity
    print("\nCASE 3 - Get game status Info")
    result = client.request_game_status()
    # print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.body)
    else:
        print("E: ", result.error_body)

    # # 2 take guess
    # #
    # # OK Response
    # print("\nCASE 3 - take guees - should return BAD REQUEST with no game running")
    # result = client.request_take_guess(Guess(Player.with_not_statistics("Iasmina"), 0, 0))
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)

    # 3 Get game status Info
    # #
    # # OK Response with game waiting players
    # print("\nCASE 3 - Get game status Info - should return OK with game WAITING PLAYERS")
    # result = client.request_game_status()
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)

    # # OK Response with game started
    # time.sleep(QUEUE_WAITING_TIME)
    # print("\nCASE 3 - Get game status Info - should return OK with game runnig")
    # result = client.request_game_status()
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)

    # # 2 take guess
    # #
    # # OK Response
    # print("\nCASE 2 - take guees - should return OK with board info")
    # result = client.request_take_guess(Guess(Player.with_not_statistics("Iasmina"), 0, 2))
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)
    #
    # # 2 take guess
    # #
    # # OK Response
    # print("\nCASE 2 - take guees - should return OK with board info")
    # result = client.request_take_guess(Guess(Player.with_not_statistics("Joan"), 0, 2))
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)

    # time.sleep(GUESS_WAITING_TIME)
    # time.sleep(GUESS_WAITING_TIME)
    # print("\nCASE 3 - Get game status Info")
    # result = client.request_game_status()
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)
    # time.sleep(GUESS_WAITING_TIME)
    # print("\nCASE 3 - Get game status Info")
    # result = client.request_game_status()
    # # print("I: ", result)
    # if result.is_ok_response():
    #     print("I: ", result.body)
    # else:
    #     print("E: ", result.error_body)
