import socket
from dataclasses import asdict
from time import sleep

from game import GUESS_WATING_TIME
from player import Player
from request import Request
from request_code import RequestCode
from socket_helpers import send_data, receive_data, SERVER_PORT


class GameClient(object):

    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

    def __create_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_address, self.__server_port))
        return sock

    def send_request(self, args: Request):
        sock = self.__create_connection()
        send_data(asdict(args), sock)

        result = receive_data(sock)
        sock.close()
        return result


if __name__ == "__main__":
    # TODO change ip address to server. Currently used this way since is programmed in same machine using DHCP
    h_name = socket.gethostname()
    RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)

    client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)

    p = Player('Iasmina', 10, 1, 0)
    a = client.send_request(Request(RequestCode.get_in_line, p))
    print(a)

    p = Player('Lucas', 10, 1, 0)
    a = client.send_request(Request(RequestCode.get_in_line, p))
    print(a)

    p = Player('Ursula', 10, 1, 0)
    a = client.send_request(Request(RequestCode.get_in_line, p))
    print(a)

    p = Player('Nazare', 10, 1, 0)
    a = client.send_request(Request(RequestCode.get_in_line, p))
    print(a)

    p = Player('Erin', 10, 1, 0)
    a = client.send_request(Request(RequestCode.get_in_line, p))
    print(a)

    #
    # p = Player('Ursula', 10, 1, 0)
    # a = client.send_request(Request(RequestCode.get_in_line, p))
    # print(a)

    p = Player('Iasmina', 11, 1, 2)
    a = client.send_request(Request(RequestCode.take_guess, p))
    print(a)

    sleep(GUESS_WATING_TIME)

    p = Player('Lucas', 11, 1, 2)
    a = client.send_request(Request(RequestCode.take_guess, p))
    print(a)

    # p = Player('Nazare', 10, 1)
    # a = client.send_request(Request(RequestCode.get_in_line, p))
    # print(a)

    # p = Player('Dayana', 10, 1)
    # a = client.send_request(Request(RequestCode.get_in_line, p))
    # print(a)
    #
    # p = Player('Iasmina', 11, 1)
    # a = client.send_request(Request(RequestCode.take_guess, p))
    # print(a)

    # p = Player('Lowrena', 11, 1)
    # a = client.send_request(Request(RequestCode.take_guess, p))
    # print(a)
