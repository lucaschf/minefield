import socket
import time
from dataclasses import asdict

from dacite import from_dict, Config

from dataclass.game_info import PlayerQueueInfo, GameInfo
from dataclass.guess import Guess
from dataclass.minesweeper_DTO import MinesweeperDTO
from dataclass.player import Player
from dataclass.request import Request
from dataclass.request import RequestCode
from dataclass.response import Response, ResponseCode
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
        send_data(asdict(args), sock)

        response_as_dict = receive_data(sock)
        sock.close()
        return from_dict(data_class=Response, data=response_as_dict,
                         config=Config(cast=[ResponseCode], check_types=False))

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
    print("CASE 1 - add player to queue - SHOULD RETURN OK")
    result = client.request_queue_entry("Iasmina")
    print("I: ", result)
    if result.is_ok_response():
        player_queue = result.content(PlayerQueueInfo)
        print("I: ", player_queue)
    else:
        print("E: ", result.error_body)

    # Not OK reponse - Applies to all not ok response. In this case a Bad request
    print("\nCASE 1 - add player to queue - SHOULD RETURN BAD REQUEST")
    result = client.request_queue_entry("Iasmina")
    print("I: ", result)
    if result.is_ok_response():
        player_queue = result.content(PlayerQueueInfo)
        print("I: ", player_queue)
    else:
        print("E: ", result.error_body)

    # 2 take guess
    #
    # OK Response
    print("\nCASE 3 - take guees - SHOULD RETURN bad request with No game started")
    result = client.request_take_guess(Guess(Player.with_not_statistics("Iasmina"), 0, 0))
    print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.content(MinesweeperDTO))
    else:
        print("E: ", result.error_body)

    # 3 Get game status Info
    #
    # OK Response with game waiting players
    print("\nCASE 3 - Get game status Info - SHOULD RETURN OK with game WAITING PLAYERS")
    result = client.request_game_status()
    print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.content(GameInfo))
    else:
        print("E: ", result.error_body)

    # OK Response with game started
    time.sleep(QUEUE_WAITING_TIME)
    print("\nCASE 3 - Get game status Info - SHOULD RETURN OK with game started")
    result = client.request_game_status()
    print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.content(GameInfo))
    else:
        print("E: ", result.error_body)

    # 2 take guess
    #
    # OK Response
    print("\nCASE 2 - take guees - SHOULD RETURN OK with board info")
    result = client.request_take_guess(Guess(Player.with_not_statistics("Iasmina"), 0, 0))
    print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.content(MinesweeperDTO))
    else:
        print("E: ", result.error_body)

    # OK Response with game ended due innactivity
    time.sleep(GUESS_WAITING_TIME)
    print("\nCASE 3 - Get game status Info - SHOULD RETURN OK with game ended due innactivity")
    result = client.request_game_status()
    print("I: ", result)
    if result.is_ok_response():
        print("I: ", result.content(GameInfo))
    else:
        print("E: ", result.error_body)
