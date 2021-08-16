
# -*- coding: utf-8 -*-


from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QMessageBox
from PySide6.QtGui import QPainter, QPaintEvent, QAction, QIcon, QColor, QMouseEvent
from PySide6.QtCore import QPoint, QRect, QSize, Signal, QObject
from tic_tac_toe_core import TicTacToeCore
import mainWindowResources


class MainWindow(QMainWindow):

    def __init__(self, control):
        super().__init__()
        self.controller = control
        self.setWindowTitle("Tic-Tac-Toe")

        # We create the menu Bar
        self.menu_bar = QMenuBar()

        file = self.menu_bar.addMenu("File")
        new_game = QAction("New Game", self)
        new_game.triggered.connect(self.on_click_new_game)
        _open = QAction(QIcon(":/menu_icons/openFolder.png"), "Open", self)
        save = QAction(QIcon(":/menu_icons/save.png"), "Save", self)
        save_as = QAction(QIcon(":/menu_icons/save.png"), "Save As", self)
        _exit = QAction("exit", self)
        _exit.triggered.connect(QApplication.quit)

        file.addAction(new_game)
        file.addAction(_open)
        file.addAction(save)
        file.addAction(save_as)
        file.addAction(_exit)

        edit = self.menu_bar.addMenu("Edit")
        undo = QAction(QIcon(":/menu_icons/undo.png"), "Cancel Your Last Move", self)
        edit.addAction(undo)

        game_help = self.menu_bar.addMenu("Help")
        rules = QAction(QIcon(":/menu_icons/rules.png"), "Rules", self)
        about = QAction(QIcon(":/menu_icons/about.png"), "About", self)
        about.triggered.connect(self.on_click_about)
        game_help.addAction(rules)
        game_help.addAction(about)

        self.setMenuBar(self.menu_bar)

        main_layout = QHBoxLayout()
        label_layout = QVBoxLayout()
        self.game_time = QLabel()
        self.current_player = QLabel()
        self.player_turn_time = QLabel()  # The player's turn time

        label_layout.addWidget(self.game_time)
        label_layout.addWidget(self.current_player)
        label_layout.addWidget(self.player_turn_time)

        self.canvas = Canvas(self)
        self.canvas.game_end.game_state.connect(self.end_of_game)

        main_layout.addWidget(self.canvas)
        main_layout.addLayout(label_layout)
        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def on_click_new_game(self) -> None:
        res = QMessageBox(self)
        res.setWindowTitle("New Game")
        res.setText("The unsaved game will be lost. Do you want to continue anyway ?")
        res.setIcon(QMessageBox.Information)
        res.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        res_state = res.exec()
        if res_state == QMessageBox.Yes:
            self.controller.get_model().reset()
            self.canvas.update()

    def on_click_about(self):
        about = QMessageBox(self)
        about.setWindowTitle("About")
        about.setText(
            "Author: Sop Karl \nGithub: https://github.com/Indecis1 \n" +
            "Images source: https://icones8.fr/"
        )
        about.exec()

    def end_of_game(self, state: int) -> None:
        msg = ""
        if state == TicTacToeCore.DRAW:
            msg = "Draw"
        elif state == TicTacToeCore.PLAYER_X_WIN:
            msg = "Player X Wins the game"
        elif state == TicTacToeCore.PLAYER_O_WIN:
            msg = "Player O Wins the game"
        else:
            return
        QMessageBox.information(self, "End of game", msg)


class Canvas(QWidget):

    def __init__(self, parent: MainWindow = None):
        super().__init__()
        self.game_end = EndOfGame()
        self.PADDING = 20
        self.PEN_WIDTH = 3
        self.widget_width = 0
        self.widget_height = 0
        self.cell_width = 0
        self.cell_height = 0
        self.game: TicTacToeCore = parent.controller.get_model()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(300, 300)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.widget_width = self.width()
        self.widget_height = self.height()
        self.cell_width = (self.widget_width - 2 * self.PADDING) // 3
        self.cell_height = (self.widget_height - 2 * self.PADDING) // 3
        padding = self.PADDING
        painter = QPainter(self)
        if event.rect().size() == QSize(self.widget_width, self.widget_height):
            p = painter.pen()
            p.setWidth(self.PEN_WIDTH)
            p.setColor(QColor("black"))
            painter.setPen(p)
            # We draw vertical lines
            for i in range(2):
                painter.drawLine(QPoint(padding + self.cell_width * (i + 1), padding),
                                 QPoint(padding + self.cell_width * (i + 1), self.widget_height - padding))
            # We draw horizontal line
            for i in range(2):
                painter.drawLine(QPoint(padding, padding + self.cell_height * (i + 1)),
                                 QPoint(self.widget_width - padding, padding + self.cell_height * (i + 1)))
            if self.game.cells != " " * 9:
                for i, cell in enumerate(self.game.cells):
                    position_x = i // 3
                    position_y = i % 3
                    top_left_corner = self.calculate_top_lef_corner_from_cell_position(position_x, position_y)
                    if cell.lower() == "x":
                        self.draw_x(top_left_corner.x(), top_left_corner.y())
                    elif cell.lower() == "o":
                        self.draw_o(QRect(top_left_corner.x(), top_left_corner.y(), self.cell_width - 5, self.cell_height - 5))
        else:
            if self.game.player.lower() == "x":
                self.draw_x(event.rect().x(), event.rect().y())
            else:
                self.draw_o(event.rect())
            self.game.change_player()
        painter.end()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x = event.pos().x()
        y = event.pos().y()
        if self.PADDING <= x <= self.widget_width - self.PADDING and \
                self.PADDING <= y <= self.widget_height - self.PADDING:

            cell_position_x, cell_position_y = self.transform_coords_to_number(x, y)
            top_left_corner = self.calculate_top_lef_corner_from_cell_position(cell_position_x, cell_position_y)
            area_height_to_update = self.cell_height - self.PEN_WIDTH * 2
            area_width_to_update = self.cell_width - self.PEN_WIDTH * 2

            game_state = self.game.check_winner_gui()
            if game_state == TicTacToeCore.GAME_CONTINUE:
                cell_input = self.game.input_gui(cell_position_x, cell_position_y)
                if cell_input == TicTacToeCore.INPUT_OK:
                    self.update(QRect(top_left_corner, QSize(area_width_to_update, area_height_to_update)))
                    self.game_end.game_state.emit(self.game.check_winner_gui())

    def transform_coords_to_number(self, x: int, y: int) -> (int, int):
        position_x = (x - self.PADDING) // (self.cell_width + self.PEN_WIDTH)
        position_y = (y - self.PADDING) // (self.cell_height + self.PEN_WIDTH)
        return position_x, position_y

    def calculate_top_lef_corner_from_cell_position(self, position_x: int, position_y: int) -> QPoint:
        return QPoint(self.PADDING + self.PEN_WIDTH * position_x + self.cell_width * position_x,
                      self.PADDING + self.PEN_WIDTH * position_y + self.cell_height * position_y
                      )

    def draw_x(self, x: int, y: int) -> None:
        top_left_corner = QPoint(x, y)
        top_right_corner = QPoint(x + self.cell_width, y)
        bottom_left_corner = QPoint(x, y + self.cell_height)
        bottom_right_corner = QPoint(x + self.cell_width, y + self.cell_height)
        painter = QPainter(self)
        p = painter.pen()
        p.setWidth(self.PEN_WIDTH)
        p.setColor(QColor("black"))
        painter.setPen(p)
        painter.drawLine(top_left_corner, bottom_right_corner)
        painter.drawLine(top_right_corner, bottom_left_corner)
        painter.end()

    def draw_o(self, rect: QRect) -> None:
        painter = QPainter(self)
        p = painter.pen()
        p.setWidth(self.PEN_WIDTH )
        p.setColor(QColor("green"))
        painter.setPen(p)
        painter.drawEllipse(rect)
        painter.end()


class EndOfGame(QObject):
    """
        This class defines signal for the end of the game. It return the state of the game
    """
    game_state = Signal(int)
