'''
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

        self.board = board

        self.buttons = []
        self.selected_letters = '|'
        self.clicked_buttons = []
        self.update_allowed()
        
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
        self.letter_display = QLabel(self.selected_letters)
        self.letter_display.setFont(QFont('Roboto', 20))
        self.letter_display.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
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

                button.clicked.connect(self.button_clicked)
                grid.addWidget(button, i, j)
                row.append(button)

            self.buttons.append(row)
        
        # Add spacing between the letter grid and the bottom buttons
        #grid.addSpacerItem(h_spacer)

        reset_button = QPushButton("Reset")
        reset_button.setFont(QFont('Roboto', 18))
        reset_button.setObjectName("ResetButton")

        reset_button.clicked.connect(self.reset_board)
        grid.addWidget(reset_button, self.board.board.shape[0], 0, 1, 1)

        hint_button = QPushButton("Hint")
        hint_button.setFont(QFont('Roboto', 18))
        hint_button.setObjectName("HintButton")

        hint_button.clicked.connect(self.hint)
        grid.addWidget(hint_button, self.board.board.shape[0], 2, 1, 1)

        check_button = QPushButton("Check")
        check_button.setFont(QFont('Roboto', 18))
        check_button.setObjectName("CheckButton")

        check_button.clicked.connect(self.check)
        grid.addWidget(check_button, self.board.board.shape[0], 4, 1, 1)

        self.setWindowTitle('Word Quarry')
        self.show()
    
    def toggleCursor(self):
        self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            self.selected_letters = ("<span style='color: white;'>|</span>"
                                    + f"{self.selected_letters}|")
        else:
            self.selected_letters = self.selected_letters[36:-1]

        self.updateLetterLine()

    def updateLetterLine(self):
        self.letter_display.setText(self.selected_letters)
    
    def updateWidgetStyle(self, widget, name):
        widget.setObjectName(name)
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def button_clicked(self):
        button = self.sender()

        if button.property('index') not in self.allowed_letters:
            # A blocked letter is clicked
            return
        elif (len(self.clicked_buttons) > 0 
            and button.property('index') == self.clicked_buttons[-1]):
            # The last selected letter is clicked
            self.last_clicked(button)
        else:
            # An allowed letter is clicked
            self.allowed_clicked(button)
    
    def last_clicked(self, button):
        if self.cursor_visible:
            self.selected_letters = self.selected_letters[:-2] + '|'
        else:
            self.selected_letters = self.selected_letters[:-1]

        self.clicked_buttons.pop()

        if len(self.clicked_buttons) > 0:
            prev_idx = self.clicked_buttons[-1]
            prev_btn = self.buttons[prev_idx[0]][prev_idx[1]]
            self.updateWidgetStyle(prev_btn, 'LetterSelectedLast')

        self.updateWidgetStyle(button, 'LetterButton')
        self.updateLetterLine()
        self.update_allowed(button.property('index'))
    
    def allowed_clicked(self, button):
        if self.cursor_visible == True:
            self.selected_letters = self.selected_letters[:-1] + button.text() + '|'
        else:
            self.selected_letters += button.text()

        self.updateLetterLine()

        if len(self.clicked_buttons) > 0:
            for idx in self.clicked_buttons:
                self.updateWidgetStyle(self.buttons[idx[0]][idx[1]],
                                       'LetterSelected') 

        self.updateWidgetStyle(button, 'LetterSelectedLast')

        self.clicked_buttons.append(button.property('index'))
        self.update_allowed(button.property('index'))

    def update_allowed(self, idx = None):
        if len(self.clicked_buttons) == 0 or idx == None:
            self.allowed_letters = [(x, y) for x in range(self.board.size[0])
                                           for y in range(self.board.size[1])]
        else:
            self.allowed_letters = [(idx[0] + dx, idx[1] + dy)
                                    for dx in (-1, 0, 1)
                                    for dy in (-1, 0, 1)
                                    if (idx[0] + dx, idx[1] + dy)
                                    not in self.clicked_buttons
                                    or (idx[0] + dx, idx[1] + dy)
                                    == self.clicked_buttons[-1]]

    def reset_board(self):
        self.selected_letters = ''
        self.clicked_buttons = []

        self.updateLetterLine()
        self.update_allowed()
        self.board.fill_board()

        for i in range(self.board.board.shape[0]):
            for j in range(self.board.board.shape[1]):
                self.buttons[i][j].setText(self.board.board[i, j].upper())
                self.updateWidgetStyle(self.buttons[i][j], 'LetterButton')
    
    def hint(self):
        pass

    def check(self):
        pass
