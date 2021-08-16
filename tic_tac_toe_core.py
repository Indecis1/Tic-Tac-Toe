# -*- coding: utf-8 -*-


class TicTacToeCore(object):
    """
        This is the model of the tic-tac-toe game
    """
    INPUT_OK = 2
    CELL_NOT_SPARE = -1
    INPUT_ERROR = -2
    PLAYER_X_WIN = 88
    PLAYER_O_WIN = 79
    DRAW = 1
    GAME_CONTINUE = 0

    def __init__(self):
        self.cells = " " * 9
        self.player = ""
        self.players = ["X", "O"]
        self.set_first_player("X")

    def reset(self):
        self.cells = " " * 9
        self.players = ["X", "O"]
        self.set_first_player("X")

    def change_player(self) -> None:
        if self.player == self.players[0]:
            self.player = self.players[1]
        else:
            self.player = self.players[0]

    def set_first_player(self, player: str) -> None:
        if player in self.players:
            self.player = player
        else:
            print("This player is not in the list")

    def input_gui(self, x: int, y: int) -> int:
        """ Input from gui """

        if not (0 <= x <= 2 and 0 <= y <= 2):
            return TicTacToeCore.INPUT_ERROR
        coordx = [0, 3, 6]
        if self.cells[coordx[x] + y] == " ":
            self.cells = self.cells[:coordx[x] + y] + self.player + self.cells[coordx[x] + y + 1:]
            return TicTacToeCore.INPUT_OK
        else:
            return TicTacToeCore.CELL_NOT_SPARE

    def input_(self) -> None:
        """ We input a position from commabd line """

        player = self.player
        x, y = input("Enter the coordinates:").split()
        try:
            x, y = int(x) - 1, int(y) - 1
        except:
            print("You should enter numbers!")
        finally:
            if not (0 <= x <= 2 and 0 <= y <= 2):
                print("Coordinates should be from 1 to 3!")
            else:
                coordx = [0, 3, 6]
                if self.cells[coordx[x] + y] == " ":
                    self.cells = self.cells[:coordx[x] + y] + player + self.cells[coordx[x] + y + 1:]
                else:
                    print("This cell is occupied! Choose another one!")

    def check_winner_gui(self) -> int:
        """ This function check the winner if you play from the GUI version """

        cells = self.cells
        _num = cells.count(" ")
        winner = []
        for i in range(3):
            if cells[i] == cells[i + 3] and cells[i] == cells[i + 6] and cells[i] != " ":
                winner.append(cells[i])
        for i in range(0, 7, 3):
            if cells[i] == cells[i + 1] and cells[i] == cells[i + 2] and cells[i] != " ":
                winner.append(cells[i])
        if cells[0] == cells[4] and cells[0] == cells[8] and cells[0] != " ":
            winner.append(cells[0])
        if cells[2] == cells[4] and cells[2] == cells[6] and cells[2] != " ":
            winner.append(cells[2])
        if len(winner) == 1:
            return ord(winner[0])
        if not _num > 0:
            return TicTacToeCore.DRAW
        return TicTacToeCore.GAME_CONTINUE
        # print("Game not finished")

    def check_winner_cmd(self):
        """ We check the state of the game if we play from the command line """

        cells = self.cells
        _num = cells.count(" ")
        winner = []
        for i in range(3):
            if cells[i] == cells[i + 3] and cells[i] == cells[i + 6] and cells[i] != " ":
                winner.append(cells[i])
        for i in range(0, 7, 3):
            if cells[i] == cells[i + 1] and cells[i] == cells[i + 2] and cells[i] != " ":
                winner.append(cells[i])
        if cells[0] == cells[4] and cells[0] == cells[8] and cells[0] != " ":
            winner.append(cells[0])
        if cells[2] == cells[4] and cells[2] == cells[6] and cells[2] != " ":
            winner.append(cells[2])
        if len(winner) == 1:
            print(winner[0], "wins")
            return 1
        if not _num > 0:
            print("Draw")
            return 0
        return -1
        # print("Game not finished")

    def printer(self) -> None:
        """ We print the field. We could use it to display the current game using the command line """
        cells = self.cells
        print("---------", end="\n")
        for i in range(0, 7, 3):
            print("|", end=" ")
            for cell in cells[i:i + 3]:
                print(cell, end=" ")
            print("|", end="\n")
        print("---------")
