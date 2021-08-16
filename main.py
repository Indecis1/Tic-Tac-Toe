
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication
from gui import MainWindow
from tic_tac_toe_core import TicTacToeCore


class Controller(object):
    def __init__(self):
        self.app = QApplication([])
        self.game = TicTacToeCore()
        self.window = MainWindow(self)
        self.window.show()

        self.app.exec()

    def get_model(self) -> TicTacToeCore:
        return self.game


control = Controller()
