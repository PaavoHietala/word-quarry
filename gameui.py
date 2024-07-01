from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

class GameUI(QWidget):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(20)
        self.setLayout(grid)

        sshFile = "style.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.buttons = []

        for i in range(self.board.board.shape[0]):
            row = []

            for j in range(self.board.board.shape[1]):
                button = QPushButton(self.board.board[i, j].upper())

                button.setFont(QFont('Arial', 18))
                button.setObjectName("LetterButton")

                button.clicked.connect(self.buttonClicked)
                grid.addWidget(button, i, j)
                row.append(button)

            self.buttons.append(row)

        reset_button = QPushButton("Reset")
        reset_button.setFont(QFont('Arial', 18, QFont.Bold))
        reset_button.setObjectName("ResetButton")

        reset_button.clicked.connect(self.resetBoard)
        grid.addWidget(reset_button, self.board.board.shape[0], 0, 1,
                       self.board.board.shape[1])

        self.setWindowTitle('Word Quarry')
        self.show()

    def buttonClicked(self):
        button = self.sender()
        QMessageBox.information(self, "Info", f"You clicked: {button.text()}")

    def resetBoard(self):
        self.board.fill_board()
        for i in range(self.board.board.shape[0]):
            for j in range(self.board.board.shape[1]):
                self.buttons[i][j].setText(self.board.board[i, j].upper())
