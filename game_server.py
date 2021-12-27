import logging
import multiprocessing
import socket

from game import Game


class GameServer(object):

    def __init__(self, hostname, port, game: Game):
        self.logger = logging.getLogger("")
        self.hostname = hostname
        self.port = port
        self.socket = None
        self.game = game

    def start(self, handle_function):
        self.logger.info("Server ready...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.info("Connection accepted...")
            _process = multiprocessing.Process(target=handle_function, args=(conn, address, self.game))
            _process.daemon = True
            _process.start()
            self.logger.debug("Started process %r", _process)
