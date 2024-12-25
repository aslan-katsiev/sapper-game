# 1 Создать игровое поле, а именно двумерный массив заполненный нулями
# 2 Создать реакцию на первое нажатие пользователя: открытие клеток вокруг первой клетки и более, генерация мин
# 3 Создать механику показа бомб вокруг клетки
# 4 Создать функцию открытия клетки и поставить флажок
# 5 Создать интерфейс - главное меню (выбор сложности) и главное поле
# 6 Создать реакцию на победу или поражение пользователя

from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QGridLayout, QButtonGroup, QMessageBox,
                             QInputDialog, QWidget)

import sys
import random
from pprint import pprint


class GameStructure:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.generate_mines()
        self.update_board()

    def generate_mines(self):
        mine_pos = set()
        while len(mine_pos) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) not in mine_pos:
                mine_pos.add((r, c))
                self.board[r][c] = -1

    def count_mines_around(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        mine_count = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.board[nx][ny] == -1:
                    mine_count += 1

        return mine_count

    def update_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1:
                    self.board[r][c] = self.count_mines_around(r, c)

    def flag(self):
        pass


class GameWindow(QMainWindow):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()

        game = GameStructure(rows=8, cols=8, mines=10)

        self.setWindowTitle("Сапёр")
        self.setFixedSize(600, 500)

        self.initUI()

    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
