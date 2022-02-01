import socket
from dataclass.guess import Guess
from enums.game_status import GameStatus
from game_client import GameClient
from helpers.socket_helpers import SERVER_PORT
from ui.gui_constants import *
from os import environ
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtCore import QThread
from ui.dialogs.join_game_dialog import JoinGameDialog
from ui.dialogs.loading_dialog import LoadingDialog
from ui.dialogs.result_dialog import ResultDialog
from ui.game_updater_worker import GameUpdaterWorker
from functools import partial
import time

class MinesweeperGuiWindow(QWidget):
    gameUpdaterThread = None
    loading_game_dialog = None
    h_name = socket.gethostname()
    RPC_SERVER_ADDRESS = socket.gethostbyname(h_name)
    client = GameClient(RPC_SERVER_ADDRESS, SERVER_PORT)

    def setupUi(self, MainWindow, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}, players=[]):

        # Timers counter font and stylesheet.
        timers_font = QtGui.QFont()
        timers_font.setFamily(TIMERS_FONT_FAMILY)
        timers_font.setPointSize(TIMERS_FONT_SIZE)
        timers_styleSheet = "*{background-color: " + TIMERS_BACKGROUND_COLOR + "; color: " + TIMERS_COLOR + "}"

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        MainWindow.setStyleSheet("background-color: " + WINDOW_BACKGROUND_COLOR)
        MainWindow.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # GameInfo. Top widget.
        self.actionsWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.actionsWidget.sizePolicy().hasHeightForWidth())
        self.actionsWidget.setSizePolicy(sizePolicy)
        self.actionsWidget.setMinimumSize(QtCore.QSize(0, 50))
        self.actionsWidget.setStyleSheet("#actionsWidget{\n"
                                         "    border: 3px groove rgb(145, 139, 140);\n"
                                         "}")
        self.actionsWidget.setObjectName("actionsWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.actionsWidget)
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gameActionPushButton = QtWidgets.QPushButton(self.actionsWidget)
        self.gameActionPushButton.setIcon(QtGui.QIcon(SMILE_ICON))
        self.gameActionPushButton.setIconSize(QtCore.QSize(20, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gameActionPushButton.sizePolicy().hasHeightForWidth())
        self.gameActionPushButton.setSizePolicy(sizePolicy)
        self.gameActionPushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.gameActionPushButton.setObjectName("gameActionPushButton")
        self.horizontalLayout.addWidget(self.gameActionPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        
        self.elapsedTimeLabel = QtWidgets.QLabel(self.actionsWidget)
        self.elapsedTimeLabel.setMinimumSize(QtCore.QSize(60, 0))
        self.elapsedTimeLabel.setMaximumSize(QtCore.QSize(60, 30))
        self.elapsedTimeLabel.setFont(timers_font)
        self.elapsedTimeLabel.setStyleSheet(timers_styleSheet)
        self.elapsedTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.elapsedTimeLabel.setObjectName("elapsedTimeLabel")
        self.horizontalLayout.addWidget(self.elapsedTimeLabel)
        self.verticalLayout.addWidget(self.actionsWidget)

        # Content. Central widget.
        self.contentWidget = QtWidgets.QWidget(self.centralwidget)
        self.contentWidget.setObjectName("contentWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.contentWidget)
        self.horizontalLayout_3.setContentsMargins(0, 9, 0, 9)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Scoreboard. Left side.
        self.scoreboardWidget = QtWidgets.QWidget(self.contentWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scoreboardWidget.sizePolicy().hasHeightForWidth())
        self.scoreboardWidget.setSizePolicy(sizePolicy)
        self.scoreboardWidget.setMinimumSize(QtCore.QSize(125, 0))
        self.scoreboardWidget.setStyleSheet("#scoreboardWidget{\n"
                                            "        border: 3px groove rgb(145, 139, 140);\n"
                                            "}")
        self.scoreboardWidget.setObjectName("scoreboardWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scoreboardWidget)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scoreboardLabel = QtWidgets.QLabel(self.scoreboardWidget)
        font = QtGui.QFont()
        font.setFamily(SCOREBOARD_TITLE_FONT_FAMILY)
        font.setPointSize(SCOREBOARD_TITLE_FONT_SIZE)
        font.setBold(True)
        self.scoreboardLabel.setFont(font)
        self.scoreboardLabel.setStyleSheet("padding-bottom: 1;\n"
                                           "border-bottom: 3px groove rgb(145, 139, 140);")
        self.scoreboardLabel.setObjectName("scoreboardLabel")
        self.verticalLayout_3.addWidget(self.scoreboardLabel)
        self.scoreboardListWidget = QtWidgets.QListWidget(
            self.scoreboardWidget)
        self.scoreboardListWidget.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scoreboardListWidget.sizePolicy().hasHeightForWidth())
        self.scoreboardListWidget.setSizePolicy(sizePolicy)
        self.scoreboardListWidget.setStyleSheet("border: 0;\n"
                                                "color: rgb(0, 0, 0);")
        self.scoreboardListWidget.setProperty("showDropIndicator", True)
        self.scoreboardListWidget.setObjectName("scoreboardListWidget")

        font = QtGui.QFont()
        font.setFamily(SCOREBOARD_FONT_FAMILY)
        font.setPointSize(SCOREBOARD_FONT_SIZE)

        self.scoreboardListWidget.setFont(font)

        self.verticalLayout_3.addWidget(self.scoreboardListWidget)
        self.horizontalLayout_3.addWidget(self.scoreboardWidget)

        # Board. Main widget.
        self.boardWidget = QtWidgets.QWidget(self.contentWidget)
        self.boardWidget.setStyleSheet("#boardWidget{\n"
                                       "        border: 3px groove rgb(145, 139, 140);\n"
                                       "}")
        self.boardWidget.setObjectName("boardWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.boardWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.boardScrollArea = QtWidgets.QScrollArea(self.boardWidget)
        self.boardScrollArea.setWidgetResizable(True)
        self.boardScrollArea.setObjectName("boardScrollArea")
        self.boardScrollAreaWidgetContents = QtWidgets.QWidget()
        self.boardScrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, 363, 386))
        self.boardScrollAreaWidgetContents.setObjectName(
            "boardScrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.boardScrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        self.new_game([], board_size, players)

        self.boardScrollArea.setWidget(self.boardScrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.boardScrollArea)
        self.horizontalLayout_3.addWidget(self.boardWidget)
        self.verticalLayout.addWidget(self.contentWidget)

        # Turn Infos. Bottom widget.
        self.turnInfoWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.turnInfoWidget.sizePolicy().hasHeightForWidth())
        self.turnInfoWidget.setSizePolicy(sizePolicy)
        self.turnInfoWidget.setMinimumSize(QtCore.QSize(0, 50))
        self.turnInfoWidget.setBaseSize(QtCore.QSize(0, 0))
        self.turnInfoWidget.setStyleSheet("#turnInfoWidget{\n"
                                          "    border: 3px groove rgb(145, 139, 140);\n"
                                          "}")
        self.turnInfoWidget.setObjectName("turnInfoWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.turnInfoWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.playerTurnLabel = QtWidgets.QLabel(self.turnInfoWidget)
        font = QtGui.QFont()
        font.setFamily(PLAYER_TURN_FONT_FAMILY)
        font.setPointSize(PLAYER_TURN_FONT_SIZE)
        self.playerTurnLabel.setFont(font)
        self.playerTurnLabel.setObjectName("playerTurnLabel")
        self.horizontalLayout_2.addWidget(self.playerTurnLabel)
        self.playerTurnLineEdit = QtWidgets.QLineEdit(self.turnInfoWidget)
        self.playerTurnLineEdit.setEnabled(True)
        self.playerTurnLineEdit.setFont(font)
        self.playerTurnLineEdit.setReadOnly(True)
        self.playerTurnLineEdit.setObjectName("playerTurnLineEdit")
        self.horizontalLayout_2.addWidget(self.playerTurnLineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.turnTimeLabel = QtWidgets.QLabel(self.turnInfoWidget)
        self.turnTimeLabel.setMinimumSize(QtCore.QSize(60, 0))
        self.turnTimeLabel.setMaximumSize(QtCore.QSize(60, 30))
        self.turnTimeLabel.setFont(timers_font)
        self.turnTimeLabel.setStyleSheet(timers_styleSheet)
        self.turnTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.turnTimeLabel.setObjectName("turnTimeLabel")
        self.horizontalLayout_2.addWidget(self.turnTimeLabel)
        self.verticalLayout.addWidget(self.turnInfoWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setStyleSheet("background-color: " + MENU_BAR_BACKGROUND_COLOR)
        self.menubar.setObjectName("menubar")
        self.menuJogo = QtWidgets.QMenu(self.menubar)
        self.menuJogo.setObjectName("menuJogo")
        MainWindow.setMenuBar(self.menubar)
        self.actionEntrar_na_Partida = QtWidgets.QAction(MainWindow)
        self.actionEntrar_na_Partida.setObjectName("actionEntrar_na_Partida")
        self.menuJogo.addAction(self.actionEntrar_na_Partida)
        self.actionEntrar_na_Partida.triggered.connect(self.show_join_game_dialog)
        self.menubar.addAction(self.menuJogo.menuAction())

        self.isGameRunnig = False
        self.startTime = None
        self.turnStartTime = None
        self.timer = QtCore.QTimer(self.centralwidget)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(0)

        self.hide_turn_info()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.elapsedTimeLabel.setText(_translate("MainWindow", "000"))
        self.scoreboardLabel.setText(_translate("MainWindow", "Scoreboard:"))
        __sortingEnabled = self.scoreboardListWidget.isSortingEnabled()
        self.scoreboardListWidget.setSortingEnabled(False)

        self.scoreboardListWidget.setSortingEnabled(__sortingEnabled)
        self.playerTurnLabel.setText(
            _translate("MainWindow", "Vez do Jogador: "))
        self.playerTurnLineEdit.setText(_translate("MainWindow", "Caren"))
        self.turnTimeLabel.setText(_translate("MainWindow", "000"))
        self.menuJogo.setTitle(_translate("MainWindow", "Jogo"))
        self.actionEntrar_na_Partida.setText(_translate("MainWindow", "Entrar na Partida"))


    #--------------------------------------------------------------------------------
    # Custom Methods

    #TODO: Connect the methods that will be used in the worker.
    def start_GameUpdaterWorker(self):
        if self.gameUpdaterThread is None or self.gameUpdaterThread.isFinished():
            self.gameUpdaterThread = QThread()
            self.gameUpdaterWorker = GameUpdaterWorker()
            #self.gameUpdaterWorker.minesweeper_gui = self
            self.gameUpdaterWorker.moveToThread(self.gameUpdaterThread)

            self.gameUpdaterThread.started.connect(partial(self.gameUpdaterWorker.run, self))
            self.gameUpdaterWorker.finished.connect(self.gameUpdaterThread.quit)
            self.gameUpdaterWorker.finished.connect(self.gameUpdaterWorker.deleteLater)
            self.gameUpdaterThread.finished.connect(self.gameUpdaterThread.deleteLater)

            # Connect the methods here, as the one bellow.
            #self.gameUpdaterWorker.open_cell.connect(self.open_cell)
            self.gameUpdaterWorker.open_cell.connect(self.open_cell)
            self.gameUpdaterWorker.new_game.connect(self.new_game)
            self.gameUpdaterWorker.start_game.connect(self.start_game)
            self.gameUpdaterWorker.next_turn.connect(self.next_turn)
            self.gameUpdaterWorker.show_turn_info.connect(self.show_turn_info)
            self.gameUpdaterWorker.close_loading_game_dialog.connect(self.close_loading_game_dialog)
            self.gameUpdaterWorker.update_turn_widgets.connect(self.update_turn_widgets)
            self.gameUpdaterWorker.end_game.connect(self.end_game)
            self.gameUpdaterWorker.eliminate_player.connect(self.eliminate_player)
            self.gameUpdaterWorker.show_result_dialog.connect(self.show_resut_dialog)
            self.gameUpdaterWorker.set_join_button_enabled.connect(self.actionEntrar_na_Partida.setEnabled)
            self.gameUpdaterWorker.update_scoreboard.connect(self.update_scoreboard)
            self.gameUpdaterThread.start()
            return True
        return False

    # Show the dialog to type your name and join the game.
    def show_join_game_dialog(self):
        join_game_dialog = JoinGameDialog()
        join_game_dialog.setupUi(self)
        join_game_dialog.setModal(True)
        join_game_dialog.exec()

    # Show the loading dialog.
    def show_loading_game_dialog(self):
        self.loading_game_dialog = LoadingDialog()
        self.loading_game_dialog.setupUi()
        self.loading_game_dialog.setModal(True)
        self.loading_game_dialog.show()

    # Close the loading dialog.
    def close_loading_game_dialog(self):
        if self.loading_game_dialog is not None:
            self.loading_game_dialog.close()

    # Show your result in a dialog.
    # @param score: The score of the player.
    # @param winner: If the player won the game.
    def show_resut_dialog(self, score, winner=False):
        self.resut_dialog = ResultDialog()
        self.resut_dialog.setupUi(score, winner)
        self.resut_dialog.setModal(True)
        self.resut_dialog.show()

    # Close the result dialog.
    def close_result_dialog(self):
        if self.resut_dialog is not None:
            self.resut_dialog.close()

    # Create a new board and scoreboard.
    def new_game(self, result_board, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}, players=[]):
        self.result_board = result_board
        self.new_scoreboard(players)
        self.new_board(board_size)

    # Create a new board.
    def new_board(self, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}):
        # TODO: Delete the print.
        print("New board. Size: {} x {}".format(board_size['rows'], board_size['columns']))

        # Delete the old board widgets.
        if(self.verticalLayout_4.itemAt(0)):
            self.verticalLayout_4.removeItem(self.verticalLayout_4.itemAt(0))
            for row in range(self.gridLayout.rowCount()):
                for column in range(self.gridLayout.columnCount()):
                    item = self.gridLayout.itemAtPosition(row, column).widget()
                    self.gridLayout.removeWidget(item)
                    item.deleteLater()
            self.gridLayout.deleteLater()

        # New board grid.
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(CELL_MARGIN)
        self.gridLayout.setObjectName("gridLayout")

        self.board_size = board_size

        # Create the new cells.
        self.board = []
        for row in range(self.board_size['rows']):
            self.board.append([])
            for column in range(self.board_size['columns']):
                pushButton = QtWidgets.QPushButton(self.boardWidget)
                pushButton.installEventFilter(self)
                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(1)
                sizePolicy.setVerticalStretch(1)
                sizePolicy.setHeightForWidth(
                    pushButton.sizePolicy().hasHeightForWidth())
                pushButton.setSizePolicy(sizePolicy)
                font=QtGui.QFont()
                font.setFamily(CELL_FONT_FAMILY)
                font.setBold(True)
                font.setPointSize(CELL_FONT_SIZE)
                pushButton.setFont(font)
                pushButton.setMinimumSize(QtCore.QSize(25, 25))
                pushButton.setIconSize(QtCore.QSize(25, 25))
                pushButton.setText("")
                pushButton.setObjectName(
                    "pushButton_" + str(row) + "_" + str(column))
                self.gridLayout.addWidget(pushButton, row, column)
                self.board[row].append(pushButton)

        # Add the grid to the layout.
        self.verticalLayout_4.addLayout(self.gridLayout)

    # Create a new scoreboard.
    def new_scoreboard(self, players=[]):
        self.players = players
        self.scoreboardListWidget.clear()
        for player in self.players:
            item = QtWidgets.QListWidgetItem()
            item.setText(player.name)
            self.scoreboardListWidget.addItem(item)

    # Return the index of the player or None if the player is not in the game.
    def find_player_index(self, player):
        for player_index, i in enumerate(self.players):
            if i.name == player.name:
                return player_index
        return None

    # Add a player to the game.
    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            item = QtWidgets.QListWidgetItem()
            item.setText(player)
            self.scoreboardListWidget.addItem(item)
            return True
        return False

    # Remove a player from the game.
    def remove_player(self, player):
        index = self.find_player_index(player)
        if index != None:
            self.players.remove(player)
            self.scoreboardListWidget.takeItem(index)

    # Strike out the name of the player who lost the game.
    def eliminate_player(self, player):
        player_index = self.find_player_index(player)
        if player_index != None:
            font = QtGui.QFont()
            font.setFamily(SCOREBOARD_FONT_FAMILY)
            font.setPointSize(SCOREBOARD_FONT_SIZE)
            font.setStrikeOut(True)
            self.scoreboardListWidget.item(player_index).setFont(font)

    # Start game and the timers.
    def start_game(self):
        self.startTime = time.time()
        self.turnStartTime = time.time()
        self.isGameRunnig = True

    # Stop game and the timers.
    def end_game(self):
        self.isGameRunnig = False

    def hide_turn_info(self):
        self.turnInfoWidget.hide()

    def show_turn_info(self):
        self.turnInfoWidget.show()

    # Updates the turn widgets
    def update_turn_widgets(self, player):
        _translate = QtCore.QCoreApplication.translate
        player_index = self.find_player_index(player)
        if player_index != None:
            self.scoreboardListWidget.setCurrentRow(player_index)
            self.playerTurnLineEdit.setText(_translate("MainWindow", player.name))

    # Reset the turn timer and select the next player.
    def next_turn(self, player):
        # _translate = QtCore.QCoreApplication.translate
        # self.turnInfoWidget.show()
        self.turnStartTime = time.time()
        self.update_turn_widgets(player)
        # player_index = self.find_player_index(player)
        # if player_index != None:
        #     self.scoreboardListWidget.setCurrentRow(player_index)
        #     self.playerTurnLineEdit.setText(_translate("MainWindow", player.name))

    # Get curret game time.
    def get_game_time(self):
        if self.startTime != None:
            return time.time() - self.startTime
        else:
            return 0

    # Update the scoreboard.
    # players: a list of dicts containing the players and their scores in the format: {"name": str, "score": int}.
    def update_scoreboard(self, players):
        _translate = QtCore.QCoreApplication.translate
        for player in players:
            index = self.find_player_index(player)
            if index != None:
                item = self.scoreboardListWidget.item(index)
                item.setText(_translate("MainWindow", player.name + " (Você)" + " - " + str(player.score) if player.name == self.player_name else player.name + " - " + str(player.score)))

    # TODO: Implement this method according to the data received from the server and the board stored in the GUI.
    # Open all cells that haven't been opened yet in the GUI.
    def update_board(self, board):
        pass

    # TODO: Implement this method according to the data received from the server and the board stored in the GUI.
    # Open a cell.
    def open_cell(self, row, column, value, exploded=False):
        # print("Abriu -> {} - {}".format(row, column))
        cell = self.board[row][column]
        if not cell.isFlat():
            if(value != 9):
                self.open_cell_number(row, column, value)
            else:
                self.open_cell_bomb(row, column, exploded)
        # pass
    
    # Open and draw the number in a cell.
    def open_cell_number(self, row, column, value):
        cell = self.board[row][column]
        cell.setFlat(True)
        if(value > 0 and value < 9):
            cell.setText(str(value))
            cell.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR + ";color: " + NUMBERS_COLORS[value - 1] + ";")
        else:
            cell.setText("")
            cell.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR)

    # Open and draw the bomb in a cell.
    # exploded: True if the bomb was exploded by this player.
    def open_cell_bomb(self, row, column, exploded=False):
        cell = self.board[row][column]
        cell.setFlat(True)
        cell.setIcon(QtGui.QIcon(BOMB_ICON))
        cell.setText("")
        if exploded == True:
            cell.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR + ";background-color: " + BOMB_EXPLODED_BACKGROUND_COLOR)
        else:
            cell.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR)

    # Executed automatically by the QTimer: "self.timer". Update the timers.
    def update_time(self):
        if self.isGameRunnig:
            now = time.time()
            self.elapsedTimeLabel.setText(str(int(now - self.startTime)).zfill(3))
            self.turnTimeLabel.setText(str(int(now - self.turnStartTime)).zfill(3))


    # Methods to handle the clicks on the cells.

    # Handle the clicks in each cell.
    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress and self.isGameRunnig == True:
            if event.button() == Qt.RightButton or event.button() == Qt.LeftButton or event.button() == Qt.MiddleButton:
                for row, buttons in enumerate(self.board):
                    for column, button in enumerate(buttons):
                        if button == QObject:
                            if not button.isFlat():
                                if event.button() == Qt.RightButton:
                                    self.right_click(row, column);
                                elif event.button() == Qt.LeftButton:
                                    self.left_click(row, column);
                                elif event.button() == Qt.MiddleButton:
                                    self.middle_click(row, column);
        return False


    # TODO: Implement the following methods to send the guesses to the server.

    # Called when the user right clicks on a cell.
    def right_click(self, row, column):
        # Testing.
        print("Right Click: " + str(row) + " " + str(column))

    # Called when the user left clicks on a cell.
    def left_click(self, row, column):
        # Testing.
        print("Left Click: " + str(row) + " " + str(column))
        result = self.client.request_game_status()
        # current_player = result.body.player_of_the_round
        # If the game is running and it is the clicking player's turn, send the clicked coordinates to the server to make a guess
        if(result.body.status == GameStatus.running and result.body.player_of_the_round.name == self.player_name):
            result_guess = self.client.request_take_guess(Guess(result.body.player_of_the_round, row, column))
            if result_guess.is_ok_response():
                if(result_guess.body.bomb == True):
                    self.open_cell(row, column, 9, True)
                    self.eliminate_player(result.body.player_of_the_round)
                    self.show_resut_dialog(result.body.player_of_the_round.score)
                    self.end_game()
                if(result_guess.body.won == True):
                    self.show_resut_dialog(result.body.player_of_the_round.score, True)
        else:
            print('voce não clicou na hora certa')

    # Called when the user middle clicks on a cell.
    def middle_click(self, row, column):
        # Testing.
        print("Middle Click: " + str(row) + " " + str(column))

        
#-----------------------------------------------------------------------------------------------------------------------

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == "__main__":
    import sys
    suppress_qt_warnings()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MinesweeperGuiWindow()
    ui.setupUi(MainWindow, {"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS})
    MainWindow.show()
    sys.exit(app.exec_())
