import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.gameui import GameUI
from src.board import Board

if __name__ == "__main__":
    board_size = [6, 5]
    board = Board(board_size, 'finwords_noCompounds.txt')
    board.fill_board()

    app = QApplication(sys.argv)
    icon = QIcon(os.path.join(Path(__file__).with_name('img'), 'icon.jpg'))
    app.setWindowIcon(icon)
    game = GameUI(board)
    sys.exit(app.exec_())
