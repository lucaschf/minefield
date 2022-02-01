from ui.gui_constants import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class ResultDialog(QDialog):
    def setupUi(self, score, winner=False):
        self.score = score
        self.winner = winner
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.setObjectName("Dialog")
        self.setFixedSize(400, 150)
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        if self.winner is True:
            self.label.setStyleSheet("border: 1px solid transparent;\n"
            "color: #0f5132;\n"
            "background-color: #d1e7dd;\n"
            "border-color: #badbcc")
        else:
            self.label.setStyleSheet("border: 1px solid transparent;\n"
            "color: #842029;\n"
            "background-color: #f8d7da;\n"
            "border-color: #f5c2c7")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Resultado"))
        if self.winner == True:
            self.label.setText(_translate("Dialog", "Você venceu!\nScore: " + str(self.score)))
        else:
            self.label.setText(_translate("Dialog", "Você perdeu!\nScore: " + str(self.score)))
