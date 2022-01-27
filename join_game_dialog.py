from gui_constants import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class JoinGameDialog(QDialog):
    def setupUi(self, parent):
        self.parent = parent

        self.setObjectName("Dialog")
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setEnabled(True)
        self.setFixedSize(450, 130)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setAcceptDrops(False)

        self.playerNameLineEdit = QtWidgets.QLineEdit(self)
        self.playerNameLineEdit.setGeometry(QtCore.QRect(10, 30, 430, 40))
        self.playerNameLineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.playerNameLineEdit.setStyleSheet("padding: 0 5%;")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.playerNameLineEdit.setFont(font)
        self.playerNameLineEdit.setObjectName("playerNameLineEdit")
        self.playerNameLabel = QtWidgets.QLabel(self)
        self.playerNameLabel.setGeometry(QtCore.QRect(10, 10, 400, 20))
        self.playerNameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.playerNameLabel.setFont(font)
        self.playerNameLabel.setObjectName("playerNameLabel")
        self.actionsWidget = QtWidgets.QWidget(self)
        self.actionsWidget.setGeometry(QtCore.QRect(0, 80, 450, 50))
        self.actionsWidget.setStyleSheet("#actionsWidget{\n"
                                            "    border-top: 1px solid gray;\n"
                                            "}")
        self.actionsWidget.setObjectName("actionsWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.actionsWidget)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.errorLabel = QtWidgets.QLabel(self.actionsWidget)
        self.errorLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.errorLabel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.errorLabel.setStyleSheet("border: 1px solid transparent;\n"
                                        "color: #842029;\n"
                                        "background-color: #f8d7da;\n"
                                        "border-color: #f5c2c7")
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setMargin(5)
        self.horizontalLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okPushButton = QtWidgets.QPushButton(self.actionsWidget, clicked=self.join_game)
        self.okPushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.okPushButton.setObjectName("okPushButton")
        self.horizontalLayout.addWidget(self.okPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(self.actionsWidget, clicked=self.close)
        self.cancelPushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Entrar na Partida"))
        self.playerNameLabel.setText(_translate("Dialog", "Nome do Jogador:"))
        self.okPushButton.setText(_translate("Dialog", "Entrar"))
        self.cancelPushButton.setText(_translate("Dialog", "Cancelar"))


    #TODO: Implement this method to try to join the game and show the error message if it fails.
    def join_game(self):

        #TODO: Change to the name returned by the server.
        self.parent.player_name = self.playerNameLineEdit.text()

        self.parent.start_GameUpdaterWorker()
        self.parent.show_loading_game_dialog()
        self.close()      

        #self.show_errorLabel("Já existe um usuário com esse nome na partida!");

    def show_errorLabel(self, error_message=None):
        if error_message is not None:
            self.errorLabel.setText(error_message)
        self.errorLabel.show()

