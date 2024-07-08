from PyQt5.QtWidgets import QStackedWidget, QWidget, QApplication
from PyQt5.QtCore import Qt

from .gameui import GameUI
from .endgame import EndGame

class UIHandler(QWidget):
    def __init__(self, board):
        super().__init__()

        self.stack = QStackedWidget()

        self.stack.setWindowTitle('Word Quarry')

        self.gameUI = GameUI(board, self)
        self.gameUI.setAttribute(Qt.WA_StyledBackground, True)

        self.endgame = EndGame(self)

        self.stack.addWidget(self.gameUI)
        self.stack.addWidget(self.endgame)

        self.stack.setCurrentWidget(self.gameUI)

        self.stack.show()

        frame_gm = self.stack.frameGeometry()
        cursor_pos = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(cursor_pos)
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.stack.move(frame_gm.topLeft())
    
    def show_endgame(self):
        self.stack.setCurrentWidget(self.endgame)
    
    def show_gameui(self):
        self.stack.setCurrentWidget(self.gameUI)