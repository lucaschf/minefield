import json

from helpers.enum_encoder import EnumEncoder

SERVER_PORT = 12000


def send_data(data, socket):
    msg = json.dumps(data, cls=EnumEncoder)
    socket.sendall(msg.encode())


def receive_data(conn):
    msg = json.loads(conn.recv(1024).decode())
    return msg
