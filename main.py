# 1 Создать игровое поле, а именно двумерный массив заполненный нулями
# 2 Создать реакцию на первое нажатие пользователя: открытие клеток вокруг первой клетки и более, генерация мин
# 3 Создать механику показа бомб вокруг клетки
# 4 Создать функцию открытия клетки и поставить флажок
# 5 Создать интерфейс - главное меню (выбор сложности) и главное поле
# 6 Создать реакцию на победу или поражение пользователя

from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QGridLayout, QButtonGroup, QMessageBox,
                             QInputDialog, QWidget, QVBoxLayout, QDialog)

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
    def __init__(self, difficulty='easy'):
        super().__init__()

        self.setWindowTitle("Сапёр")

        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        # Создание окна выбора сложности
        dialog = QDialog(self)
        dialog.setWindowTitle("Выберите уровень сложности")
        dialog.setGeometry(100, 100, 200, 200)

        layout = QVBoxLayout(dialog)

        easy_button = QPushButton("Легкий")
        medium_button = QPushButton("Средний")
        hard_button = QPushButton("Сложный")

        easy_button.clicked.connect(lambda: self.start_game('easy', dialog))
        medium_button.clicked.connect(lambda: self.start_game('medium', dialog))
        hard_button.clicked.connect(lambda: self.start_game('hard', dialog))

        layout.addWidget(easy_button)
        layout.addWidget(medium_button)
        layout.addWidget(hard_button)

        dialog.exec()

    def start_game(self, difficulty, dialog):
        dialog.accept()
        self.init_game(difficulty)

    def init_game(self, difficulty):
        if difficulty == 'easy':
            rows, cols, mines = 8, 8, 10
            self.setGeometry(100, 100, 300, 300)
        elif difficulty == 'medium':
            rows, cols, mines = 16, 16, 40
            self.setGeometry(100, 100, 400, 400)
        elif difficulty == 'hard':
            rows, cols, mines = 24, 24, 99
            self.setGeometry(100, 100, 500, 500)

        self.game = GameStructure(rows=rows, cols=cols, mines=mines)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setSpacing(0)
        central_widget.setLayout(layout)

        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                but = QPushButton()
                but.setFixedSize(30, 30)

                but.clicked.connect(self.open_cell)

                layout.addWidget(but, i, j)

    def open_cell(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
