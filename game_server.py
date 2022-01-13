from datetime import datetime
import logging
import multiprocessing
import socket
import time

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
        
        start = time.time()
        diff = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            diff = time.time() - start

            if diff < 120: ### 120sec/2min to start
                if not self.game.is_player_queue_full(): ### only accepts new connections if not full
                    conn, address = self.socket.accept()
                    self.logger.info("Connection accepted...")
                    _process = multiprocessing.Process(target=handle_function, args=(conn, address, self.game))
                    _process.daemon = True
                    _process.start()
                    self.logger.debug("Started process %r", _process)

                    if self.game.is_player_queue_full():
                        print("Players limit reached, starting game...")
                        ##start_game()
            else:
                print("Time wait reached, starting game...")
                ##start_game()
                
                
