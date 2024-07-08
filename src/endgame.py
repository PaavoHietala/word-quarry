from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QPushButton)

class EndGame(QWidget):
    def __init__(self, uihandler):
        super().__init__()

        self.uihandler = uihandler

        layout = QGridLayout()

        self.button = QPushButton('Go back to main window')
        self.button.clicked.connect(self.uihandler.show_gameui)

        layout.addWidget(self.button)

        self.setLayout(layout)