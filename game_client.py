import socket
import time
from dataclasses import asdict

from dacite import from_dict, Config

from game import QUEUE_WAITING_TIME, GUESS_WAITING_TIME
from player import Player
from request import Request
from request import RequestCode
from response import Response, ResponseCode
from socket_helpers import send_data, receive_data, SERVER_PORT


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

    def request_take_guess(self, player_name: str) -> Response:
        return self.__send_request(Request(RequestCode.take_guess, Player.with_not_statistics(player_name)))


if __name__ == "__main__":
    # TODO change ip address to server. Currently used this way since is programmed in same machine using DHCP
    h_name = socket.gethostname()
    RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)

    client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)

    (client.request_queue_entry("Iasmina"))
    (client.request_queue_entry("Lucas"))
    time.sleep(QUEUE_WAITING_TIME)
    time.sleep(GUESS_WAITING_TIME)

    print(client.request_game_status())
    time.sleep(GUESS_WAITING_TIME)
    print(client.request_game_status())

    #
    # print("1")
    # time.sleep(QUEUE_WATING_TIME + 1)
    # print(client.request_game_status())

    # print(r.successful)
    # print(r.content(list[Player]))
    # print(client.request_queue_entry(""))
    # print(client.request_queue_entry("Lucas"))
    #
    # print("SHOULD NOT ENTER")
    # print(client.request_queue_entry("asdasd"))

    # print("STATUS")
    # r: Response = client.request_game_status()
    # if r.successful:
    #     print(r.content(GameInfo))
    # else:
    #     print(r.error_body)
    #
    # time.sleep(QUEUE_WATING_TIME + 1)
    # r: Response = client.request_game_status()
    # if r.successful:
    #     print(r.content(GameInfo))
    # else:
    #     print(r.error_body)
