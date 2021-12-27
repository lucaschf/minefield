import socket
from dataclasses import asdict

from player import Player
from request import Request
from request_code import RequestCode
from socket_helpers import send_data, receive_data


class ClientTest(object):

    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

    def __create_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_address, self.__server_port))
        return sock

    def send_request(self, args):
        sock = self.__create_connection()
        send_data(args, sock)

        result = receive_data(sock)
        sock.close()
        return result


RPC_SERVER = "10.0.1.28"
RPC_PORT = 12000

client = ClientTest(RPC_SERVER, RPC_PORT)

p = Player('Iasmina', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Elias', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Livia', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Ursula', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Nazare', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Dayana', 10, 1)
a = client.send_request(asdict(Request(RequestCode.get_in_line, p)))
print(a)

p = Player('Lowrena', 11, 1)
a = client.send_request(asdict(Request(RequestCode.take_guess, p)))
print(a)

p = Player('Lowrena', 11, 1)
a = client.send_request(asdict(Request(RequestCode.take_guess, p)))
print(a)
