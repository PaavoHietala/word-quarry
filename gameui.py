'''
TODO: Combine clicked_letters and selected_letters
TODO: Add all functionality to buttonClicked() (blocked squares)
TODO: Create "check word"-button based on code in linetest.py
'''

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

        self.buttons = []
        self.clicked_letters = '|'
        self.selected_letters = []
        self.allowed_letters = []

        self.board = board

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        h_spacer = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Load stylesheet
        sshFile = "style.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        # Add spacing between title bar and selected letters
        main_layout.addSpacerItem(h_spacer)
        
        # Label to display clicked letters on the top
        self.letter_display = QLabel(self.clicked_letters)
        self.letter_display.setFont(QFont('Roboto', 20))
        self.letter_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.letter_display)

        # Blinking cursor parameters
        self.cursor_visible = True
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.toggleCursor)
        self.cursor_timer.start(500)

        # Black line under the clicked letter display
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setMinimumWidth(int(self.width() * 0.8))
        main_layout.addWidget(self.line)

        # Add spacing between the line and the letter grid
        main_layout.addSpacerItem(h_spacer)

        # Grid layout for buttons
        grid = QGridLayout()
        grid.setSpacing(20)
        main_layout.addLayout(grid)

        for i in range(self.board.board.shape[0]):
            row = []

            for j in range(self.board.board.shape[1]):
                button = QPushButton(self.board.board[i, j].upper())

                button.setFont(QFont('Roboto', 18))
                button.setObjectName("LetterButton")
                button.setProperty('index', (i,j))

                button.clicked.connect(self.buttonClicked)
                grid.addWidget(button, i, j)
                row.append(button)

            self.buttons.append(row)

        reset_button = QPushButton("Reset")
        reset_button.setFont(QFont('Roboto', 18))
        reset_button.setObjectName("ResetButton")

        reset_button.clicked.connect(self.resetBoard)
        grid.addWidget(reset_button, self.board.board.shape[0], 0, 1,
                       self.board.board.shape[1])

        self.setWindowTitle('Word Quarry')
        self.show()
    
    def toggleCursor(self):
        self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            self.clicked_letters = ("<span style='color: white;'>|</span>"
                                    + f"{self.clicked_letters}|")
        else:
            self.clicked_letters = self.clicked_letters[36:-1]

        self.updateLetterLine()

    def updateLetterLine(self):
        self.letter_display.setText(self.clicked_letters)
    
    def updateWidgetStyle(self, widget, name):
        widget.setObjectName(name)
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def buttonClicked(self):
        button = self.sender()

        # Blocked is clicked

        # Last selected is clicked
        if len(self.selected_letters) > 0 and \
           button.property('index') == self.selected_letters[-1]:
            if self.cursor_visible:
                self.clicked_letters = self.clicked_letters[:-2] + '|'
            else:
                self.clicked_letters = self.clicked_letters[:-1]

            self.selected_letters.pop()

            if len(self.selected_letters) > 0:
                prev_idx = self.selected_letters[-1]
                prev_btn = self.buttons[prev_idx[0]][prev_idx[1]]
                self.updateWidgetStyle(prev_btn, 'LetterSelectedLast')

            self.updateWidgetStyle(button, 'LetterButton')
            self.updateLetterLine()

            return

        # Available is clicked
        if self.cursor_visible == True:
            self.clicked_letters = self.clicked_letters[:-1] + button.text() + '|'
        else:
            self.clicked_letters += button.text()

        self.updateLetterLine()

        if len(self.selected_letters) > 0:
            for idx in self.selected_letters:
                self.updateWidgetStyle(self.buttons[idx[0]][idx[1]],
                                       'LetterSelected') 

        self.updateWidgetStyle(button, 'LetterSelectedLast')

        self.selected_letters.append(button.property('index'))

    def resetBoard(self):
        self.clicked_letters = ''
        self.selected_letters = []

        self.updateLetterLine()
        self.board.fill_board()

        for i in range(self.board.board.shape[0]):
            for j in range(self.board.board.shape[1]):
                self.buttons[i][j].setText(self.board.board[i, j].upper())
                self.updateWidgetStyle(self.buttons[i][j], 'LetterButton')
