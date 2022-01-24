import logging
import socket
import threading
from dataclasses import asdict
from json.decoder import JSONDecodeError

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
        self.__game = Game()

        lock = threading.Lock()

        while True:
            self.listen_requests(lock)

    def listen_requests(self, lock):
        conn, address = self.__socket.accept()
        self.__logger.info("Connection accepted...")
        # _process = multiprocessing.Process(target=self.handle_requests, args=(conn, address, self.__game))
        # _process.daemon = True
        # _process.start()
        # _process.join()
        # self.__logger.debug("Started process %r", _process)

        th = threading.Thread(target=self.handle_requests, args=(conn, address, self.__game, lock))
        th.start()
        th.join()

        # self.handle_requests(conn, address, self.__game)

    @staticmethod
    def start_game_if_requirements_met(game_data: Game):
        if game_data.status == Status.waiting_players and (
                game_data.queueing_timeout or game_data.is_player_queue_full):
            game_data.start()

    @staticmethod
    def answer(connection, data: Response, request):
        dict_response = asdict(data)

        send_data(dict_response, connection)

        try:
            request = asdict(request)
        except TypeError:
            request = str(request)

        logger.info("Request: '{}'\n\t\t  Response: {}".format(request, dict_response))
        logger.info("Closing connection.")
        connection.close()

    @staticmethod
    def handle_requests(connection, address, game_data: Game, lock):
        try:
            logger.info(f"Connection from {address} has been established.")

            while True:
                request_data = receive_data(connection)

                lock.acquire()

                try:
                    request = dataclass_from_dict(Request, request_data)
                except JSONDecodeError:
                    GameServer.answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request_data)
                    break
                if not isinstance(request, Request):
                    GameServer.answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request)
                    break
                if request.code == RequestCode.get_in_line.value:
                    GameServer.answer(connection, GameServer.handle_queue_request(request, game_data), request)
                    break
                elif request.code == RequestCode.take_guess.value:
                    GameServer.answer(connection, GameServer.handle_guess(request, game_data), request)
                    break
                elif request.code == RequestCode.game_status.value:
                    GameServer.answer(connection, GameServer.handle_status_request(game_data), request)
                    break
                else:
                    GameServer.answer(connection, Response(ResponseCode.UNSUPPORTED, "Unsupported operation"), request)
                    break
        except RuntimeError:
            GameServer.answer(connection, Response(ResponseCode.ERROR, "Can't handle request"), "")
        finally:
            lock.release()

    @staticmethod
    def handle_queue_request(request: Request, game_data: Game) -> Response:
        if game_data.status == Status.running:
            return Response(ResponseCode.DENIED, "The game has already started")

        player = dataclass_from_dict(Player, request.body)

        if not isinstance(player, Player):
            return Response(ResponseCode.BAD_REQUEST, "Invalid player data")

        if player.name is None or player.name == "":
            return Response(ResponseCode.BAD_REQUEST, "Invalid player data")

        if game_data.is_player_queue_full:
            return Response(ResponseCode.DENIED, "Queue is full")

        check = [p for p in game_data.players_as_list if p.name == player.name]
        if check:
            return Response(ResponseCode.BAD_REQUEST,
                            f"That's is already a player with the name '{player.name}' on the queue.")

        game_data.add_player_to_queue(player)

        return Response(ResponseCode.OK, game_data.players_as_list)

    @staticmethod
    def handle_guess(request: Request, game_data: Game) -> Response:
        player = dataclass_from_dict(Player, request.body)

        # TODO use tuple for player - guess

        if not isinstance(player, Player):
            return Response(ResponseCode.ERROR, "Invalid player data")

        try:
            # TODO format to Response
            return game_data.take_guess(player, None)
        except PlayerOutOfTurn as e:
            return Response(ResponseCode.DENIED, e.errors)

    @staticmethod
    def handle_status_request(game_data: Game) -> Response:
        info: GameInfo = GameInfo(
            game_data.players_as_list,
            game_data.status,
            game_data.get_current_player(generate_if_none=False),
            # game_data.minesweeper
        )
        return Response(ResponseCode.OK, info)


if __name__ == "__main__":
    game = Game()
    server = GameServer('', SERVER_PORT)

    try:
        server.start_server()
    except RuntimeError:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")

    logging.info("All done")
