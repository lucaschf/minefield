from ui.gui_constants import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class LoadingDialog(QDialog):
    def setupUi(self):
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.setObjectName("Dialog")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))

        self.imgLabel = QtWidgets.QLabel(self)
        self.imgLabel.setGeometry(QtCore.QRect(10, 10, 380, 220))
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.movie = QtGui.QMovie(LOADING_GIF)
        self.imgLabel.setMovie(self.movie)
        self.movie.start()

        self.textLabel = QtWidgets.QLabel(self)
        self.textLabel.setGeometry(QtCore.QRect(10, 230, 380, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textLabel.setFont(font)
        self.textLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel.setObjectName("textLabel")
        self.textLabel.setStyleSheet("border-top: 1px solid #ccc;")

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Aguardando Jogadores"))
        self.textLabel.setText(_translate("Dialog", "Aguardando Jogadores ..."))
