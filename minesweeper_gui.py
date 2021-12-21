from PyQt5 import QtCore, QtGui, QtWidgets
from os import environ
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, Qt
import time


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants for quick access.

WINDOW_WIDTH = 575
WINDOW_HEIGHT = 600

ICONS_FOLDER = './icons/'

WINDOW_ICON = ICONS_FOLDER + 'icon.png'
SMILE_ICON = ICONS_FOLDER + 'smile.png'
FLAG_ICON = ICONS_FOLDER + 'flag.png'
BOMB_ICON = ICONS_FOLDER + 'bomb.png'

WINDOW_BACKGROUND_COLOR = 'rgb(195, 195, 195)'
MENU_BAR_BACKGROUND_COLOR = 'rgb(235, 231, 219)'
TIMERS_COLOR = 'rgb(220, 0, 0)'
TIMERS_BACKGROUND_COLOR = 'rgb(0, 0, 0)'
NUMBERS_COLORS = ["blue", "green", "red", "purple", "maroon", "rgb(0,175,180)", "black", "gray"]
OPENED_CELL_BORDER_COLOR = 'rgb(125, 125, 125)'
BOMB_EXPLODED_BACKGROUND_COLOR = 'rgb(220, 30, 30)'

TIMERS_FONT_FAMILY = "Unispace"
SCOREBOARD_TITLE_FONT_FAMILY = "Arial"
SCOREBOARD_FONT_FAMILY = "MS Shell Dlg 2"
PLAYER_TURN_FONT_FAMILY = "MS Shell Dlg 2"
CELL_FONT_FAMILY = "Arial"

TIMERS_FONT_SIZE = 16
SCOREBOARD_TITLE_FONT_SIZE = 10
SCOREBOARD_FONT_SIZE = 10
PLAYER_TURN_FONT_SIZE = 12
CELL_FONT_SIZE = 12

CELL_MARGIN = 0
DEFAULT_BOARD_ROWS = 16
DEFAULT_BOARD_COLS = 16

#----------------------------------------------------------------------------------------------------------------------------------------------------------------

# For testing.
PLAYERS = ["Ailton", "Caren", "Giovanne", "Lucas", "Paulo", "Talita"]


class Ui_MainWindow(QWidget):

    def setupUi(self, MainWindow, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}, players=[]):

        # Timers and flags counter font and stylesheet.
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

        self.remainingFlagsLabel = QtWidgets.QLabel(self.actionsWidget)
        self.remainingFlagsLabel.setMinimumSize(QtCore.QSize(60, 30))
        self.remainingFlagsLabel.setMaximumSize(QtCore.QSize(60, 30))
        self.remainingFlagsLabel.setFont(timers_font)
        self.remainingFlagsLabel.setStyleSheet(timers_styleSheet)
        self.remainingFlagsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.remainingFlagsLabel.setObjectName("remainingFlagsLabel")
        self.horizontalLayout.addWidget(self.remainingFlagsLabel)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gameActionPushButton = QtWidgets.QPushButton(self.actionsWidget, clicked=self.teste)
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
        
        self.new_game(board_size, players)

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
        self.menuAjuda = QtWidgets.QMenu(self.menubar)
        self.menuAjuda.setObjectName("menuAjuda")
        MainWindow.setMenuBar(self.menubar)
        self.actionNovo_Jogo = QtWidgets.QAction(MainWindow)
        self.actionNovo_Jogo.setObjectName("actionNovo_Jogo")
        self.actionAjuda = QtWidgets.QAction(MainWindow)
        self.actionAjuda.setObjectName("actionAjuda")
        self.actionTeste = QtWidgets.QAction(MainWindow)
        self.actionTeste.setObjectName("actionTeste")
        self.menuJogo.addAction(self.actionNovo_Jogo)
        self.menuJogo.addSeparator()
        self.menuJogo.addAction(self.actionTeste)
        self.menuAjuda.addAction(self.actionAjuda)
        self.menubar.addAction(self.menuJogo.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())

        self.isGameRunnig = False
        self.startTime = None
        self.turnStartTime = None
        self.timer = QtCore.QTimer(self.centralwidget)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(0)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.elapsedTimeLabel.setText(_translate("MainWindow", "000"))
        self.remainingFlagsLabel.setText(_translate("MainWindow", "000"))
        self.scoreboardLabel.setText(_translate("MainWindow", "Scoreboard:"))
        __sortingEnabled = self.scoreboardListWidget.isSortingEnabled()
        self.scoreboardListWidget.setSortingEnabled(False)

        self.scoreboardListWidget.setSortingEnabled(__sortingEnabled)
        self.playerTurnLabel.setText(
            _translate("MainWindow", "Vez do Jogador: "))
        self.playerTurnLineEdit.setText(_translate("MainWindow", "Caren"))
        self.turnTimeLabel.setText(_translate("MainWindow", "000"))
        self.menuJogo.setTitle(_translate("MainWindow", "Jogo"))
        self.menuAjuda.setTitle(_translate("MainWindow", "Ajuda"))
        self.actionNovo_Jogo.setText(_translate("MainWindow", "Novo Jogo"))
        self.actionAjuda.setText(_translate("MainWindow", "Ajuda"))
        self.actionTeste.setText(_translate("MainWindow", "Teste"))


    #--------------------------------------------------------------------------------
    # Custom Methods

    # Create a new board and scoreboard.
    def new_game(self, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}, players=[]):
        self.new_scoreboard(players)
        self.new_board(board_size)

    # Create a new scoreboard.
    def new_scoreboard(self, players=[]):
        self.players = players
        self.scoreboardListWidget.clear()
        for player in self.players:
            item = QtWidgets.QListWidgetItem()
            item.setText(player)
            self.scoreboardListWidget.addItem(item)

    # Create a new board.
    def new_board(self, board_size={"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}):
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

    # Update all cells.
    # board: a matrix containing a dict with the informations about each cell in the format: {"opened": bool, "value": int, 'flagged': bool,"bomb": bool, "exploded": bool}.
    def update_board(self, board):
        for row in range(len(board)):
            for column in range(len(board[row])):
                self.update_cell(row, column, board[row][column])

    # Update a cell.
    # cell: a dict with the informations about the cell in the format: {"opened": bool, "value": int, 'flagged': bool,"bomb": bool, "exploded": bool}.
    def update_cell(self, row, column, cell):
        # Updating the numbers.
        field = self.board[row][column]
        if cell['opened'] == True:
            field.setFlat(True)
            if(cell['value'] > 0):
                field.setText(str(cell['value']))
                field.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR + ";color: " + NUMBERS_COLORS[cell['value'] - 1] + ";")
            else:
                field.setText("")
                field.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR)

        # Updating the icons.
        if cell['flagged'] == True:
            field.setIcon(QtGui.QIcon(FLAG_ICON))
            field.setText("")
        elif cell['bomb'] == True and cell['opened'] == True:
            field.setIcon(QtGui.QIcon(BOMB_ICON))
            field.setText("")
            if cell['exploded'] == True:
                field.setStyleSheet("border: 1px inset " + OPENED_CELL_BORDER_COLOR + ";background-color: " + BOMB_EXPLODED_BACKGROUND_COLOR)
        else:
            field.setIcon(QtGui.QIcon())
    
    # Executed automatically by the QTimer: "self.timer". Update the timers.
    def update_time(self):
        if self.isGameRunnig:
            now = time.time()
            self.elapsedTimeLabel.setText(str(int(now - self.startTime)).zfill(3))
            self.turnTimeLabel.setText(str(int(now - self.turnStartTime)).zfill(3))
            if(int(now - self.turnStartTime) == 10):
                # Testing
                self.next_turn(self.next_player(self.playerTurnLineEdit.text()))

    # Update the number of flags remaining.
    def update_remaining_flags(self, remaining_flags):
        self.remainingFlagsLabel.setText(str(remaining_flags).zfill(3))

    # Update the scoreboard.
    # players: a list of dicts containing the players and their scores in the format: {"name": str, "score": int}.
    def update_scoreboard(self, players):
        _translate = QtCore.QCoreApplication.translate
        for player in players:
            index = self.find_player_index(player['name'])
            if index != None:
                item = self.scoreboardListWidget.item(index)
                item.setText(_translate("MainWindow", player['name'] + " - " + str(player['score'])))

    # Return the index of the player or None if the player is not in the game.
    def find_player_index(self, player):
        try:
            return self.players.index(player)
        except ValueError:
            return None

    # Add a player to the game.
    def add_player(self, player):
        self.players.append(player)
        item = QtWidgets.QListWidgetItem()
        item.setText(player)
        self.scoreboardListWidget.addItem(item)

    # Remove a player from the game.
    def remove_player(self, player):
        index = self.find_player_index(player)
        self.players.remove(player)
        if index != None:
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
            
    # Reset the turn timer and select the next player.
    def next_turn(self, player):
        _translate = QtCore.QCoreApplication.translate
        self.turnStartTime = time.time()
        player_index = self.find_player_index(player)
        if player_index != None:
            self.scoreboardListWidget.setCurrentRow(player_index)
            self.playerTurnLineEdit.setText(_translate("MainWindow", player))

    # Get curret game time.
    def get_game_time(self):
        if self.startTime != None:
            return time.time() - self.startTime
        else:
            return 0

    # Handle the clicks in each cell.
    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress and self.isGameRunnig == True:
            if event.button() == Qt.RightButton or event.button() == Qt.LeftButton or event.button() == Qt.MiddleButton:
                for row, buttons in enumerate(self.board):
                    for column, button in enumerate(buttons):
                        if button == QObject:
                            if event.button() == Qt.RightButton:
                                self.mark_flag(row, column);
                            elif event.button() == Qt.LeftButton:
                                self.open_field(row, column);
                            elif event.button() == Qt.MiddleButton:
                                self.open_all_around(row, column);
        return False

    # Called when the user right clicks on a cell.
    def mark_flag(self, row, column):
        # Testing.
        self.update_cell(row, column, {'opened': False, 'flagged': True, 'value': 0})
        print("Flag: " + str(row) + " " + str(column))
        self.next_turn(self.next_player(self.playerTurnLineEdit.text()))

    # Called when the user left clicks on a cell.
    def open_field(self, row, column):
        # Testing.
        print("Open: " + str(row) + " " + str(column))
        self.next_turn(self.next_player(self.playerTurnLineEdit.text()))

    # Called when the user middle clicks on a cell.
    def open_all_around(self, row, column):
        # Testing.
        print("Open All Around: " + str(row) + " " + str(column))
        self.next_turn(self.next_player(self.playerTurnLineEdit.text()))


#----------------------------------------------------------------------------------------------------------------------
    # Testing the methods.

    def next_player(self, player):
        player_index = self.find_player_index(player)
        if player_index != None:
            player_index += 1
            if player_index >= len(self.players):
                player_index = 0
        else:
            player_index = 0

        return self.players[player_index]
        

    def teste(self):
        import random
        players = []
        for p in PLAYERS:
            player = {}
            player['score'] = random.randint(0, 100)
            player['name'] = p
            players.append(player)

        self.update_scoreboard(players)

        size = random.randint(1, 50)
        self.new_board({"rows": size, "columns": size})
        board = []
        exploded = False
        for row in range(self.board_size['rows']):
            board.append([])
            for column in range(self.board_size['columns']):
                opened = player['score'] = random.randint(0, 1)
                if random.randint(0, 1) == 1:
                    board[row].append({"opened": True, "value": 0, "bomb": True, "exploded": False})
                    if exploded == False:
                        if random.randint(0, 1) == 1:
                            exploded = True
                            board[row][column]["exploded"] = True
                else:
                    board[row].append({"opened": True if opened == 0 else False, "value": random.randint(0, 8), "bomb": False})
        
        for row in range(self.board_size['rows']):
            board.append([])
            for column in range(self.board_size['columns']):
                if board[row][column]['opened'] == False:
                    board[row][column]['flagged'] = True if random.randint(0, 1) == 1 else False
                else:
                    board[row][column]['flagged'] = False

        self.eliminate_player(self.players[random.randint(0, len(self.players) - 1)])
        self.update_board(board)
        self.update_remaining_flags(random.randint(0, 100))
        self.start_game()
        self.remove_player("Ailton")
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
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, {"rows": DEFAULT_BOARD_ROWS, "columns": DEFAULT_BOARD_COLS}, PLAYERS)
    MainWindow.show()
    sys.exit(app.exec_())
