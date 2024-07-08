'''
TODO: Accepted words on the bottom of the screen
TODO: Hint functionality
TODO: End game button which shows the correct result
TODO: End game when the last word is correct
TODO: Timer for end screen
TODO: Config file with board size
TODO: Clean up word list
'''

from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QPushButton,
                             QFrame,
                             QSpacerItem,
                             QLabel,
                             QSizePolicy,
                             QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QPainter, QPen, QColor

from pathlib import Path

from .popup import FadePopup

class GameUI(QWidget):
    '''
    A PyQt5 class for the Word Quarry UI and game functionality. 

    Parameters
    ----------
    QWidget : PyQt5.QWidgets.QWidget
        The base class of all PyQt UI objects
    '''

    def __init__(self, board, uihandler):
        '''
        Initialize the Word Quarry UI with given pre-populated board.

        Parameters
        ----------
        board : board.Board
            The game board which contains the letter grid and the wordlist

        Attributes
        ----------
        board : board.Board
            The game board which contains the letter grid and the wordlist
        buttons : list of list of PyQt5.QtWidgets.QPushButton
            The grid of letter buttons arranged in a list of rows of buttons
        selected_letters : str
            The selected letters as displayed over the line on the top. The
            blinking cursor is also contained on this line as well as a hidden
            spacer character in the beginning of the string to center the string
        clicked_buttons : list of tuple of int
            A list of currently selected letter buttons as a list of 2D coords
            in the format of (row, col)
        lines : list of list of tuple of int
            A list of correct words as a list of 2D coordinate tuples. The
            coordinates correspond to the button indices as (row, col)
        '''

        super().__init__()

        self.board = board
        self.uihandler = uihandler

        self.buttons = []
        self.selected_letters = '|'
        self.clicked_buttons = []
        self.lines = []
        self.update_allowed()
        
        self.initUI()

    def initUI(self):
        '''
        Build the user interface from widgets.
        '''

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        h_spacer = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Load stylesheet
        qss_fpath = Path(__file__).with_name('style.qss')
        with open(qss_fpath, "r") as fh:
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
        '''
        Toggles the blinking cursor on or off.
        Driven by the QTimer started in the initUI method.
        '''

        self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            self.selected_letters = ("<span style='color: white;'>|</span>"
                                    + f"{self.selected_letters}|")
        else:
            self.selected_letters = self.selected_letters[36:-1]

        self.updateLetterLine()

    def updateLetterLine(self):
        '''
        Update the letter display on the top of the window.
        '''

        self.letter_display.setText(self.selected_letters)
    
    def updateWidgetStyle(self, widget, name):
        '''
        Update the style of given widget by changing the objectName. This
        changes the style based on the style.qss file.

        Parameters
        ----------
        widget : PyQt5.QtWidgets.QWidget
            The target widget, the objectName of which will be changed
        name : str
            The objectName to be given for the widget
        '''

        widget.setObjectName(name)
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def button_clicked(self):
        '''
        A handler method for the letter grid buttons.
        '''

        button = self.sender()

        if button.objectName() == 'CorrectLetter':
            self.correct_clicked(button)
        elif button.property('index') not in self.allowed_letters:
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
        '''
        Actions taken if the user clicked the same letter grid button as last
        time. The last selected letter is de-selected.

        Parameters
        ----------
        button : PyQt5.QtWidgets.QPushButton
            The letter grid button clicked by the user
        '''

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
        '''
        Actions taken when the user clicks an allowed button. Allowed buttons
        include all letters if the board is empty, or the 3x3 grid of buttons
        around the last selected buttons that have not been previously connected
        into a correct word.

        Parameters
        ----------
        button : PyQt5.QtWidgets.QPushButton
            The letter grid button clicked by the user
        '''

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
    
    def correct_clicked(self, button):
        '''
        Actions taken when the user clicks a letter that has been previously
        connected as a correct word. The word is removed from the board and the
        related button styles are reverted to the base configuration.

        Parameters
        ----------
        button : PyQt5.QtWidgets.QPushButton
            The letter grid button clicked by the user
        '''

        for line in self.lines:
            if button.property('index') in line:
                for idx in line:
                    self.updateWidgetStyle(self.buttons[idx[0]][idx[1]],
                                           'LetterButton')
                self.lines.remove(line)
                self.repaint()
                break

    def update_allowed(self, idx = None):
        '''
        Update allowed letters based on the last selected letter in idx. If
        idx is None, the whole board is reset in an allowed state.

        Parameters
        ----------
        idx : tuple of int or None, optional
            The (row, col) index of the letter button that has been clicked or
            None if the whole board is empty, by default None
        '''

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
    
    def paintEvent(self, event):
        '''
        PyQt5 paintEvent, which is used to draw the lines connecting the letters
        of a correct word. All words are repainted each time this event is run.
        Triggering this event is mainly controlled by PyQt and it's done e.g. on
        window resize. Triggered manually when a word is correct or a correct
        word is removed.

        Parameters
        ----------
        event : PyQt5.QtGui.QPaintEvent
            The QPaintEvent class contains event parameters for paint events
        '''

        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing, True)

        pen_color = QColor(204, 216, 255)
        pen = QPen(pen_color, 30, Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        for line in self.lines:
            points = [QPoint(self.buttons[i][j].geometry().center().x(),
                             self.buttons[i][j].geometry().center().y())
                      for i, j in line]

            painter.drawPolyline(*points)

    def reset_board(self):
        '''
        Reset the board by removing all selections and placing new words on the
        board.
        '''

        self.selected_letters = ''
        self.clicked_buttons = []
        self.lines = []

        self.repaint()
        self.updateLetterLine()
        self.update_allowed()

        self.board.fill_board()

        for i in range(self.board.board.shape[0]):
            for j in range(self.board.board.shape[1]):
                self.buttons[i][j].setText(self.board.board[i, j].upper())
                self.updateWidgetStyle(self.buttons[i][j], 'LetterButton')
    
    def remove_pending_word(self, correct = False):
        '''
        Removes the selected letters from the board (which are not a part of an
        accepted word). If correct == True, the selection is frozen as an
        accepted word and connected by a line. Otherwise the selection is removed.

        Parameters
        ----------
        correct : bool, optional
            Indicates if the pending word is correct, in which case it should
            be accepted and the letters connected by a line, by default False
        '''

        for idx in self.clicked_buttons:
            if correct:
                self.updateWidgetStyle(self.buttons[idx[0]][idx[1]],
                                       'CorrectLetter')
            else:
                self.updateWidgetStyle(self.buttons[idx[0]][idx[1]],
                                       'LetterButton')
            self.clicked_buttons = []
            self.selected_letters = ''
            self.updateLetterLine()
            self.update_allowed()
    
    def hint(self):
        '''
        A hint method, which gives one starting letter of a word at a time. TODO
        '''

        pass

    def check(self):
        '''
        Check if the selected letters form an accepted word which is found from
        the board.wordlist. If the word is accepted, the letters are connected
        by a line. If the word is not found, the selected letters are de-selected.
        '''

        if not self.cursor_visible:
            word = self.selected_letters
        else:
            word = self.selected_letters[36:-1]
        
        if word.lower() in self.board.wordlist['word'].values:
            self.lines.append(self.clicked_buttons)
            self.repaint()
            self.remove_pending_word(correct = True)

            cells = self.board.size[0] * self.board.size[1]
            if sum(len(line) for line in self.lines) == cells:
                self.uihandler.show_endgame()
        else:
            if len(word) == 0:
                self.show_fade_popup("Click letters to form a word")
            else:
                self.show_fade_popup("Invalid word")

            self.remove_pending_word()            
    
    def show_fade_popup(self, message):
        '''
        Show a fade in and fade out popup with given message.

        Parameters
        ----------
        message : str
            The text to be shown for the user
        '''

        self.popup = FadePopup(message, self)
        self.popup.show()
