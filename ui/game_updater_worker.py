from PyQt5.QtCore import pyqtSignal, QObject
import time
import os
from dataclass.player import Player
from enums.game_status import GameStatus

from game_client import GameClient
from helpers.socket_helpers import SERVER_ADDRESS, SERVER_PORT

os.sys.path.append("..")
# This class is used to receive the game updates from the server and emit the signals to update the GUI.
class GameUpdaterWorker(QObject):
    # Receives connection with main thread methods to emit signals.
    finished = pyqtSignal()
    open_cell = pyqtSignal(int, int, int)
    new_game = pyqtSignal(tuple, dict, tuple)
    start_game = pyqtSignal()
    next_turn = pyqtSignal(Player)
    show_turn_info = pyqtSignal()
    close_loading_game_dialog = pyqtSignal()
    left_click = pyqtSignal(int, int)
    update_turn_widgets = pyqtSignal(Player)
    eliminate_player = pyqtSignal(Player)
    end_game = pyqtSignal()
    show_result_dialog = pyqtSignal()
    set_join_button_enabled = pyqtSignal(bool)
    update_scoreboard = pyqtSignal(tuple)

    def run(self, minesweeper_gui):
        client = GameClient(SERVER_ADDRESS, SERVER_PORT)
        flag = 0
        current_player = None
        while True:
            
            result = client.request_game_status()
            if(result.is_ok_response()):
                if(result.body.status != GameStatus.ended and result.body.status != GameStatus.ended_due_inactivity):
                    if result.body.status == GameStatus.running:
                        flag += 1
                        #When the game starts
                        if flag == 1:
                            board_size = {"rows" : len(result.body.minesweeper.board), "columns" : len(result.body.minesweeper.board[0])}
                            self.new_game.emit(result.body.minesweeper.board, board_size, result.body.players)
                            self.start_game.emit()
                            self.next_turn.emit(result.body.player_of_the_round)
                            self.show_turn_info.emit()
                            self.close_loading_game_dialog.emit()
                            if result.body.player_of_the_round != current_player:
                                current_player = result.body.player_of_the_round
                        
                        else:
                            self.update_scoreboard.emit(result.body.players)
                            self.update_turn_widgets.emit(result.body.player_of_the_round)
                            open_coordinates = result.body.minesweeper.coordinates
                            if len(open_coordinates) > 0:
                                for cell in open_coordinates:
                                    if(result.body.minesweeper.board[cell[0]][cell[1]] != 9):
                                        self.open_cell.emit(cell[0], cell[1], result.body.minesweeper.board[cell[0]][cell[1]])
                            for player in result.body.inactive_players:
                                self.eliminate_player.emit(player)
                            if result.body.player_of_the_round != current_player:
                                current_player = result.body.player_of_the_round
                                self.next_turn.emit(result.body.player_of_the_round)
                                       
                else:
                    for player in result.body.players:
                        if player == minesweeper_gui.player_name:
                            self.show_result_dialog(player.score, True if player.name == result.body.winner.name else False)
                    board = result.body.minesweeper.board
                    for row_index, row in enumerate(board):
                        for column_index, column in enumerate(row):
                            self.open_cell.emit(row_index, column_index, board[row_index][column_index])
                    self.end_game.emit()
                    self.set_join_button_enabled.emit(True)
                    flag=0
                    self.finished.emit()
            
            time.sleep(2)