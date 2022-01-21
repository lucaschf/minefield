import logging
import multiprocessing
import socket
from dataclasses import asdict

from Exceptions import PlayerOutOfTurn
from game import Game, Status
from game_info import GameInfo
from json_helpers import dataclass_from_dict
from player import Player
from request import Request
from request import RequestCode
from response import Response
from response import ResponseCode
from socket_helpers import send_data, receive_data, SERVER_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("")


class GameServer(object):

    def __init__(self, hostname, port):
        self.__logger = logging.getLogger("")
        self.__hostname = hostname
        self.__port = port
        self.__socket = None
        self.__game = Game()

    def start_server(self):
        self.__logger.info("Server ready...")
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__hostname, self.__port))
        self.__socket.listen(1)

        while True:
            self.start_game_if_requirements_met()
            self.listen_requests()

    def listen_requests(self):
        conn, address = self.__socket.accept()
        self.__logger.info("Connection accepted...")
        # _process = multiprocessing.Process(target=self.handle_requests, args=(conn, address))
        # _process.daemon = True
        # _process.start()
        # self.logger.debug("Started process %r", _process)
        self.handle_requests(conn, address)

    def start_game_if_requirements_met(self):
        if self.__game.status == Status.waiting_players and (
                self.__game.queueing_timeout or self.__game.is_player_queue_full):
            self.__game.start()

    @staticmethod
    def answer(connection, data: Response, request):
        send_data(asdict(data), connection)
        logger.info("Request: '{}'\n\t\t  Response: {}".format(str(request), str(data)))

    # logger.info("Closing connection.")
    # connection.close()

    def handle_requests(self, connection, address):
        try:
            logger.info(f"Connection from {address} has been established.")

            while True:
                request = dataclass_from_dict(Request, receive_data(connection))

                if request == "":
                    GameServer.answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request)
                    break
                if not isinstance(request, Request):
                    self.answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request)
                    break
                if request.code == RequestCode.get_in_line.value:
                    self.start_game_if_requirements_met()
                    self.answer(connection, self.handle_queue_request(request), request)
                    break
                elif request.code == RequestCode.take_guess.value:
                    self.answer(connection, self.handle_guess(request), request)
                    break
                elif request.code == RequestCode.game_status.value:
                    self.answer(connection, self.handle_status_request(), request)
                    break
                else:
                    self.answer(connection, Response(ResponseCode.UNSUPPORTED, "Unsupported operation"), request)
                    break
        except RuntimeError:
            GameServer.answer(connection, Response(ResponseCode.ERROR, "Can't handle request"), "")

    def handle_queue_request(self, request: Request) -> Response:
        if self.__game.status == Status.running:
            return Response(ResponseCode.DENIED, "The game has already started")

        player = dataclass_from_dict(Player, request.body)

        if not isinstance(player, Player):
            return Response(ResponseCode.ERROR, "Invalid player data")

        if self.__game.is_player_queue_full:
            return Response(ResponseCode.DENIED, "Queue is full")

        check = [p for p in self.__game.players_as_list if p.name == player.name]
        if check:
            return Response(ResponseCode.BAD_REQUEST,
                            f"That's is already a player with the name '{player.name}' on the queue.")

        self.__game.add_player_to_queue(player)

        return Response(ResponseCode.OK, self.__game.players_as_list)

    def handle_guess(self, request: Request) -> Response:
        player = dataclass_from_dict(Player, request.body)

        # TODO use tuple for player - guess

        if not isinstance(player, Player):
            return Response(ResponseCode.ERROR, "Invalid player data")

        try:
            # TODO format to Response
            return self.__game.take_guess(player, None)
        except PlayerOutOfTurn as e:
            return Response(ResponseCode.DENIED, e.errors)

    def handle_status_request(self) -> Response:
        info: GameInfo = GameInfo(
            self.__game.players_as_list,
            self.__game.status,
            self.__game.get_current_player(generate_if_none=False),
            self.__game.minesweeper
        )
        return Response(ResponseCode.OK, info)


def kill_proccess():
    for process in multiprocessing.active_children():
        logging.info("Shutting down process %r", process)
        process.terminate()
        process.join()


if __name__ == "__main__":
    game = Game()
    server = GameServer('', SERVER_PORT)

    try:
        server.start_server()
    except RuntimeError:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        kill_proccess()

    logging.info("All done")
