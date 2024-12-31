# 1 Создать игровое поле, а именно двумерный массив заполненный нулями
# 2 Создать реакцию на первое нажатие пользователя: открытие клеток вокруг первой клетки и более, генерация мин
# 3 Создать механику показа бомб вокруг клетки
# 4 Создать функцию открытия клетки и поставить флажок
# 5 Создать интерфейс - главное меню (выбор сложности) и главное поле
# 6 Создать реакцию на победу или поражение пользователя

from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QGridLayout, QMessageBox,
                             QWidget, QVBoxLayout, QDialog)
from PyQt6.QtCore import Qt
import sys
import random


class GameStructure:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.game_started = False

    def generate_mines(self, first_click_x, first_click_y):
        mine_pos = set()

        while len(mine_pos) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) not in mine_pos and (r, c) != (first_click_x, first_click_y):
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

    def first_click(self, x, y):
        if not self.game_started:
            self.game_started = True
            self.generate_mines(x, y)
            self.update_board()


class GameWindow(QMainWindow):
    def __init__(self, difficulty='easy'):
        super().__init__()
        self.setWindowTitle("Сапёр")
        self.buttons = []
        self.show_difficulty_selection()
        self.is_flagged = False
        self.first_click_done = False

    def show_difficulty_selection(self):
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
        self.clear_ui()
        self.init_game(difficulty)

    def clear_ui(self):
        for row in self.buttons:
            for button in row:
                button.deleteLater()

        self.buttons.clear()
        self.first_click_done = False

    def init_game(self, difficulty):
        if difficulty == 'easy':
            rows, cols, mines = 8, 8, 10
            self.setFixedSize(250, 250)
        elif difficulty == 'medium':
            rows, cols, mines = 16, 16, 40
            self.setFixedSize(500, 500)
        elif difficulty == 'hard':
            rows, cols, mines = 24, 24, 99
            self.setFixedSize(750, 750)

        self.game = GameStructure(rows=rows, cols=cols, mines=mines)

        self.buttons.clear()

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setSpacing(0)
        central_widget.setLayout(layout)

        for i in range(len(self.game.board)):
            row_buttons = []
            for j in range(len(self.game.board[0])):
                but = QPushButton()
                but.setFixedSize(30, 30)

                but.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                but.customContextMenuRequested.connect(lambda pos, button=but: self.toggle_flag(button))

                but.clicked.connect(lambda checked, x=i, y=j: self.open_cell(x, y))

                layout.addWidget(but, i, j)
                row_buttons.append(but)

            self.buttons.append(row_buttons)

    def mousePressEvent(self, event):
        button = self.sender()
        if event.button() == Qt.MouseButton.RightButton:
            self.toggle_flag(button)
        elif event.button() == Qt.MouseButton.LeftButton:
            if button.text() == '🚩':
                return
            else:
                super().mousePressEvent(event)

    def toggle_flag(self, button):
        if button is None:
            return

        if button.text() == '🚩':
            button.setText("")
            button.setStyleSheet("")
        else:
            button.setText("🚩")
            button.setStyleSheet("color: red;")

        if self.check_win_condition():
            self.check_win()

    def open_cell(self, x, y):
        button = self.buttons[x][y]

        if button.text() == '🚩':
            return

        if not self.first_click_done:
            self.first_click_done = True
            self.game.first_click(x, y)
            self.game.update_board()

        value = self.game.board[x][y]

        if value == -1:
            button.setText('💣')
            button.setStyleSheet('color: black; font-size: 17px;')
            self.check_loose()
            return

        button.setText(str(value) if value > 0 else '')

        button.setEnabled(False)

        if value == 0:
            self.open_adjacent_cells(x, y)

        color_map = {
            1: ('blue', 'bold'),
            2: ('green', 'bold'),
            3: ('red', 'bold'),
            4: ('purple', 'bold'),
            5: ('brown', 'bold'),
            6: ('yellow', 'bold'),
            7: ('orange', 'bold'),
            8: ('pink', 'bold')
        }
        if value in color_map:
            color, weight = color_map[value]
            button.setStyleSheet(f'color: {color}; font-size: 25px; font-weight: {weight};')

        if self.check_win_condition():
            self.check_win()

    def open_adjacent_cells(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(self.game.board)) and (0 <= ny < len(self.game.board[0])):
                adjacent_button = self.buttons[nx][ny]

                if adjacent_button.isEnabled():
                    adjacent_value = self.game.board[nx][ny]
                    adjacent_button.setText(str(adjacent_value))

                    if adjacent_value == -1:
                        adjacent_button.setText('💣')
                        adjacent_button.setStyleSheet('color: black; font-size: 17px;')
                        continue

                    if adjacent_value == 0:
                        adjacent_button.setText('')
                        adjacent_button.setEnabled(False)
                        self.open_adjacent_cells(nx, ny)
                    else:
                        color_map = {
                            1: ('blue', 'bold'),
                            2: ('green', 'bold'),
                            3: ('red', 'bold'),
                            4: ('purple', 'bold'),
                            5: ('brown', 'bold'),
                            6: ('yellow', 'bold'),
                            7: ('orange', 'bold'),
                            8: ('pink', 'bold')
                        }
                        color, weight = color_map[adjacent_value]
                        adjacent_button.setStyleSheet(f'color: {color}; font-size: 25px; font-weight: {weight};')

                    adjacent_button.setEnabled(False)

    def check_win_condition(self):
        total_safe_cells = sum(1 for row in self.game.board for cell in row if cell != -1)
        opened_cells = sum(1 for row in self.buttons for button in row if not button.isEnabled())
        flagged_cells = sum(1 for row in self.buttons for button in row if button.text() == '🚩')

        return opened_cells == total_safe_cells and flagged_cells == self.game.mines

    def check_win(self):
        win = QMessageBox()
        win.setWindowTitle('Победа')
        win.setText('Поздравляем! Вы разминировали все бомбы! Хотите начать заново?')
        win.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if win.exec() == QMessageBox.StandardButton.Yes:
            self.show_difficulty_selection()
        else:
            QApplication.quit()

    def check_loose(self):
        loose = QMessageBox()
        loose.setWindowTitle('Поражение')
        loose.setText('Вы попали на бомбу. Хотите начать заново?')
        loose.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if loose.exec() == QMessageBox.StandardButton.Yes:
            self.show_difficulty_selection()
        else:
            QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
