import logging
import socket
import threading
from json.decoder import JSONDecodeError

import jsonpickle

from dataclass.game_info import GameInfo, PlayerQueueInfo
from dataclass.guess import Guess
from dataclass.request import Request
from dataclass.request import RequestCode
from dataclass.response import Response, bad_request_response, denied_response, ok_response, error_response, \
    unsupported_response
from enums.game_status import GameStatus
from exceptions.player_out_of_turn import PlayerOutOfTurn
from game import Game
from helpers.socket_helpers import send_data, receive_data, SERVER_PORT

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

        th = threading.Thread(target=self.handle_requests, args=(conn, address, self.__game, lock))
        th.start()
        th.join()

    @staticmethod
    def start_game_if_requirements_met(game_data: Game):
        if game_data.status == GameStatus.waiting_players and (
                game_data.queueing_timeout or game_data.is_player_queue_full):
            game_data.start()

    @staticmethod
    def answer(connection, response: Response, request):
        response_as_json = jsonpickle.encode(response)

        send_data(response_as_json, connection)

        logger.info("Request:  '{}'\n\t\t  Response: '{}'".format(str(request), str(response)))
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
                    request = jsonpickle.decode(request_data)
                except JSONDecodeError:
                    GameServer.answer(connection, bad_request_response("FAILED TO LOAD"), request_data)
                    break
                if not isinstance(request, Request):
                    GameServer.answer(connection, bad_request_response(), request)
                    break
                if request.code == RequestCode.get_in_line:
                    GameServer.answer(connection, GameServer.handle_queue_request(request, game_data), request)
                    break
                elif request.code == RequestCode.take_guess:
                    GameServer.answer(connection, GameServer.handle_guess(request, game_data), request)
                    break
                elif request.code == RequestCode.game_status:
                    GameServer.answer(connection, GameServer.handle_status_request(game_data), request)
                    break
                else:
                    GameServer.answer(connection, unsupported_response(), request)
                    break
        except RuntimeError as e:
            print(e)
            GameServer.answer(connection, error_response(), "")
        finally:
            lock.release()

    @staticmethod
    def handle_queue_request(request: Request, game_data: Game) -> Response:
        try:
            if game_data.status == GameStatus.running:
                return denied_response("The game has already started")

            try:
                player = request.body
            except AttributeError:
                return bad_request_response("Invalid player data")

            if player is None or player.name is None or player.name == "":
                return bad_request_response("Invalid player data")

            if game_data.is_player_queue_full:
                return denied_response("Queue is full")

            found = [p for p in game_data.players_as_tuple if p.name == player.name]
            if found:
                return bad_request_response(f"That's is already a player with the name '{player.name}' on the queue.")

            game_data.add_player_to_queue(player)
            return ok_response(PlayerQueueInfo(game_data.players_as_tuple))
        except RuntimeError:
            return error_response()

    @staticmethod
    def handle_guess(request: Request, game_data: Game) -> Response:

        if game_data.status != GameStatus.running:
            return bad_request_response("No game running")

        guess = request.body
        if guess is None or not isinstance(guess, Guess) or guess.player is None:
            return bad_request_response("Invalid guess data")

        try:
            result = game_data.take_guess(guess)
            result.game_info = GameServer.get_game_info(game_data)
            return ok_response(result)
        except PlayerOutOfTurn as e:
            return denied_response(str(e.errors))

    @staticmethod
    def handle_status_request(game_data: Game) -> Response:
        return ok_response(GameServer.get_game_info(game_data))

    @staticmethod
    def get_game_info(game_data: Game) -> GameInfo:
        return GameInfo(
            game_data.status,
            game_data.players_as_tuple,
            game_data.get_current_player(generate_if_none=False),
            None if game_data.minesweeper is None else game_data.minesweeper.to_dto(),
            game_data.inactive_players,
            game_data.winner
        )


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
