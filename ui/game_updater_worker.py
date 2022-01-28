from PyQt5.QtCore import pyqtSignal, QObject
import time
import random

#TODO: Implement the communication with the server and the game updates.
# This class is used to receive the game updates from the server and emit the signals to update the GUI.
class GameUpdaterWorker(QObject):
    # Receives connection with main thread methods to emit signals.
    finished = pyqtSignal()
    open_cell = pyqtSignal(int, int)

    def run(self, minesweeper_gui):
        while True:
            # Receive the data form the server
            # Before start the game, add the name of the new players to the scoreboard to have a visual feedback.

            # When the server send the signal to start the game:
            # Call the method new_game() before start the game to configure the board and the players.
            # Call the start_game().
            # Call the next_turn() to configure the plaayer of the turn.
            # Call show_turn_info() to show the information of the turn.
            # Call close_loading_game_dialog() to close the loading game dialog.

            # When the game is running:
            # Call the methods to update the GUI with the received data.
            #self.progress.emit(parametros)
            self.open_cell.emit(random.randint(0, minesweeper_gui.board_size['rows'] - 1), random.randint(0, minesweeper_gui.board_size['columns'] - 1))
            time.sleep(10)

            # When the server send the signal to end the game:
            # Call the method end_game() to end the game.
            # Call the method show_resut_dialog() to show the winner.
            #self.finished.emit()  # Emit signal to main thread to finish the worker.