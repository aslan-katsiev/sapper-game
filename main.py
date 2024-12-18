import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QWidget,
    QInputDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt  # Импортируем Qt


class GameLogic:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.generate_mines()
