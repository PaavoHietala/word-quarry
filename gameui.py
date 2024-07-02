from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QPushButton,
                             QFrame,
                             QSpacerItem,
                             QLabel,
                             QSizePolicy,
                             QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class GameUI(QWidget):
    def __init__(self, board):
        super().__init__()
        self.clicked_letters = '|'
        self.board = board
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add spacing between the line and the grid
        main_layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))
        
        # Label to display clicked letters
        self.letter_display = QLabel(self.clicked_letters)
        self.letter_display.setFont(QFont('Arial', 18))
        self.letter_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.letter_display)

        # Blinking cursor
        self.cursor_visible = True
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.toggleCursor)
        self.cursor_timer.start(500)

        # Black line under the QLabel
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(self.line)

        # Set the length of the line to 80% of window width
        self.line.setMinimumWidth(int(self.width() * 0.8))

        # Add spacing between the line and the grid
        main_layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Grid layout for buttons
        grid = QGridLayout()
        grid.setSpacing(20)  # Add 50px spacing between buttons
        main_layout.addLayout(grid)

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
    
    def toggleCursor(self):
        # Toggle cursor visibility
        self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            self.clicked_letters = ' ' + self.clicked_letters + '|'
        else:
            self.clicked_letters = self.clicked_letters[1:-1]

        self.updateLetterLine()

    def updateLetterLine(self):
        self.letter_display.setText(self.clicked_letters)

    def buttonClicked(self):
        button = self.sender()

        if self.cursor_visible == True:
            self.clicked_letters = self.clicked_letters[:-1] + button.text() + '|'
        else:
            self.clicked_letters += button.text()

        self.updateLetterLine()

    def resetBoard(self):
        self.board.fill_board()
        self.clicked_letters = ''
        self.updateLetterLine()
        for i in range(self.board.board.shape[0]):
            for j in range(self.board.board.shape[1]):
                self.buttons[i][j].setText(self.board.board[i, j].upper())
