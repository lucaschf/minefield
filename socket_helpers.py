import json

from response_code import EnumEncoder


def send_data(data, socket):
    msg = json.dumps(data, cls=EnumEncoder)
    socket.sendall(msg.encode())


def receive_data(conn):
    msg = json.loads(conn.recv(1024).decode())
    return msg
