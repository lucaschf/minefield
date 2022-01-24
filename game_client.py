import socket
import time
from dataclasses import asdict

from game import QUEUE_WATING_TIME
from player import Player
from request import Request
from request import RequestCode
from response import Response
from socket_helpers import send_data, receive_data, SERVER_PORT


class GameClient(object):

    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

    def __create_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_address, self.__server_port))
        # sock.bind((self.__server_address, self.__server_port))
        return sock

    def __send_request(self, args: Request):
        sock = self.__create_connection()
        send_data(asdict(args), sock)

        result = receive_data(sock)
        sock.close()
        return result

    def request_queue_entry(self, player_name: str) -> Response:
        """ Sends a request to add a new player to the queue.

            :parameter
                player_name (str): the target player name

            :returns
                Response ('~Response'): A reponse with a response code and a result body:

                OK -> The request was sucessfully answered;
                body -> list of all players in the queue sorted by order of entry;

                DENIED -> If the queue is already full or the game has already started;
                body -> str message with the reason for denial

                BAD_REQUEST-> If the request data is invalid such as player already in the queue or empty name;
                body -> message with the cause

                ERROR -> If there is an error processing the request.
                body -> message with the error.
         """
        return self.__send_request(Request(RequestCode.get_in_line, Player.with_not_statistics(player_name)))

    def request_game_status(self) -> Response:
        """ Sends a request to get the running game info.

            :returns
                Response ('~Response'): A reponse with a response code and a result body:

                OK -> The request was sucessfully answered;
                body -> ('~GameInfo') containg all game info;

                ERROR -> If there is an error processing the request.
                body -> message with the error.
         """
        return self.__send_request(Request(RequestCode.game_status, None))

    def send_request2(self, args):
        sock = self.__create_connection()
        send_data(args, sock)

        result = receive_data(sock)
        sock.close()
        return result

    def send_empty(self):
        return self.send_request2(None)


if __name__ == "__main__":
    # TODO change ip address to server. Currently used this way since is programmed in same machine using DHCP
    h_name = socket.gethostname()
    RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)

    client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)

    print(client.send_empty())

    print(client.request_queue_entry("Iasmina"))
    print(client.request_queue_entry("Lucas"))
    time.sleep(QUEUE_WATING_TIME + 1)

    print("SHOULD NOT ENTER")

    print(client.request_queue_entry("juca"))
    print(client.request_queue_entry("asdasd"))

    print("STATUS")
    print(client.request_game_status())

    # print(client.request_queue_entry(None))
    # print(client.request_queue_entry(""))
    # print(client.request_queue_entry("Iasmina"))
    # print(client.request_game_status())
    # print(client.request_game_status())
    # print(client.request_queue_entry(""))
