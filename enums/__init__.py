# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("QThread Example")
        self.thread = Worker()
        self.listFile = QListWidget()
        self.btnStart = QPushButton("start")
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)
        self.btnStart.clicked.connect(self.slotStart)
        self.thread.sinout.connect(self.slotAdd)

    def slotStart(self):
        self.btnStart.setEnabled(False)
        self.thread.start()

    def slotAdd(self, file_inf):
        self.listFile.addItem(file_inf)


class Worker(QThread):
    sinout = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            file_str = "File index {0} ".format(self.num)
            self.num += 1
            # Transmitting signal
            self.sinout.emit(file_str)
            # Thread hibernates for 2 seconds
            self.sleep(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())
