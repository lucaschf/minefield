import logging
import multiprocessing
from dataclasses import asdict

from Exceptions import PlayerOutOfTurn
from game import Game
from game_server import GameServer
from json_helpers import dataclass_from_dict
from player import Player
from request import Request
from request_code import RequestCode
from response import Response
from response_code import ResponseCode
from socket_helpers import send_data, receive_data, SERVER_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("")


def answer(connection, data: Response, request):
    send_data(asdict(data), connection)
    logger.info("Request: '{}'\n\t\t  Response: {}".format(str(request), str(data)))
    #logger.info("Closing connection.")
    #connection.close()


def handle(connection, address, game_data):
    try:
        logger.info(f"Connection from {address} has been established.")

        while True:
            request = dataclass_from_dict(Request, receive_data(connection))

            if request == "":
                answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request)
                break

            print(dataclass_from_dict(Request, dataclass_from_dict(Request, request)))

            if not isinstance(request, Request):
                answer(connection, Response(ResponseCode.BAD_REQUEST, "Bad request"), request)
                break
            if request.code == RequestCode.get_in_line.value:
                answer(connection, handle_queue_request(request, game_data), request)
                break
            elif request.code == RequestCode.take_guess.value:
                answer(connection, handle_guess(request, game_data), request)
                break
            else:
                answer(connection, Response(ResponseCode.UNSUPPORTED, "Unsupported operation"), request)
                break

    except RuntimeError:
        answer(connection, Response(ResponseCode.ERROR, "Can't handle request"), "")


def handle_queue_request(request: Request, game_data: Game) -> Response:
    player = dataclass_from_dict(Player, request.body)

    if not isinstance(player, Player):
        return Response(ResponseCode.ERROR, "Invalid player data")

    if game_data.is_player_queue_full():
        return Response(ResponseCode.DENIED, "Queue is full")

    check = [p for p in game_data.players_as_list if p.name == player.name]

    # check = filter(lambda p: p.name == player.name, game_data.players_as_list)
    if check:
        return Response(ResponseCode.BAD_REQUEST,
                        f"That's is already a player with the name '{player.name}' on the queue.")

    print(player.name)
    game_data.add_player(player)

    return Response(ResponseCode.OK, game_data.players_as_list)


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


def kill_proccess():
    for process in multiprocessing.active_children():
        logging.info("Shutting down process %r", process)
        process.terminate()
        process.join()


if __name__ == "__main__":

    game = Game()
    server = GameServer('', SERVER_PORT, game)

    try:
        server.start(handle)
    except RuntimeError:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        kill_proccess()
    logging.info("All done")
