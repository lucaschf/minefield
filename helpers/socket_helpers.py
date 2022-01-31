import json


SERVER_PORT = 12000


def send_data(data, socket):
    msg = json.dumps(data)
    socket.sendall(msg.encode())


def receive_data(conn):
    msg = json.loads(conn.recv(1024 * 10).decode())
    return msg
