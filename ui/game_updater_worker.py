import socket
from PyQt5.QtCore import pyqtSignal, QObject
import time
import random
import sys
import os
from dataclass.player import Player
from enums.game_status import GameStatus

from game_client import GameClient
from helpers.socket_helpers import SERVER_PORT

os.sys.path.append("..")
#TODO: Implement the communication with the server and the game updates.
# This class is used to receive the game updates from the server and emit the signals to update the GUI.
class GameUpdaterWorker(QObject):
    # Receives connection with main thread methods to emit signals.
    finished = pyqtSignal()
    open_cell = pyqtSignal(int, int)
    new_game = pyqtSignal(tuple, dict, tuple)
    start_game = pyqtSignal()
    next_turn = pyqtSignal(Player)
    show_turn_info = pyqtSignal()
    close_loading_game_dialog = pyqtSignal()

    def run(self, minesweeper_gui):
        h_name = socket.gethostname()
        RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)
        client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)
        flag = 0
        while True:
            # Receive the data form the server
            # Before start the game, add the name of the new players to the scoreboard to have a visual feedback.

            # When the server send the signal to start the game:
            # Call the method new_game() before start the game to configure the board and the players.
            # Call the start_game().
            # Call the next_turn() to configure the plaayer of the turn.
            # Call show_turn_info() to show the information of the turn.
            # Call close_loading_game_dialog() to close the loading game dialog.
            result = client.request_game_status()
            if(result.is_ok_response()):
                if(result.body.status != GameStatus.ended and result.body.status != GameStatus.ended_due_inactivity):
                    if result.body.status == GameStatus.running:
                        flag += 1
                        if flag == 1:
                            board_size = {"rows" : len(result.body.minesweeper.board), "columns" : len(result.body.minesweeper.board[0])}
                            self.new_game.emit(result.body.minesweeper.board, board_size, result.body.players)
                            self.start_game.emit()
                            self.next_turn.emit(result.body.player_of_the_round)
                            self.show_turn_info.emit()
                            self.close_loading_game_dialog.emit()
                        else:
                            pass
                    

                        
                else:
                    print('b')
                    print(result.body)

            
                
            # When the game is running:
            # Call the methods to update the GUI with the received data.
            # self.progress.emit(parametros)
            # self.open_cell.emit(random.randint(0, minesweeper_gui.board_size['rows'] - 1), random.randint(0, minesweeper_gui.board_size['columns'] - 1))
            
            time.sleep(2)

            # When the server send the signal to end the game:
            # Call the method end_game() to end the game.
            # Call the method show_resut_dialog() to show the winner.
            #self.finished.emit()  # Emit signal to main thread to finish the worker.