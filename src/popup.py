from pathlib import Path
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QGraphicsOpacityEffect

class FadePopup(QWidget):
    '''
    A pop-up widget to display fade in and fade out messages.

    Parameters
    ----------
    QWidget : PyQt5.QWidgets.QWidget
        The base class of all PyQt UI objects
    '''

    def __init__(self, message, callWidget, duration = 1000):
        '''
        Init the popup widget.

        Parameters
        ----------
        message : str
            Message to be displayed in the popup
        callWidget : PyQt5.QtWidgets.QWidget
            The calling widget which is used to position the popup
        duration : int, optional
            Duration of the popup between fade in and fade out, by default 1000
        '''

        super().__init__()
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        sshFile = Path(__file__).with_name('style.qss')
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())
        
        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setObjectName('Popup')
        self.label.setFont(QFont('Roboto', 18))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(250)
        
        self.timer = QTimer()
        self.timer.setInterval(duration)
        self.timer.timeout.connect(self.fade_out)

        # Set location based on calling window
        font_metrics = QFontMetrics(self.label.font())
        width = font_metrics.horizontalAdvance(message) + 100
        self.resize(width, self.height())

        point = callWidget.rect().center()
        global_point = callWidget.mapToGlobal(point)

        global_point.setX(global_point.x() - int(width / 2))
        global_point.setY(global_point.y() - 200)

        self.move(global_point)
    
    def showEvent(self, event):
        '''
        A modified .show() event to enable animations

        Parameters
        ----------
        event : QtGui.QShowEvent
            Parent event class to be overloaded
        '''

        self.fade_in()
    
    def fade_in(self):
        '''
        Fade in animation for the popup.
        '''

        self.effect.setOpacity(0)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.timer.start()
    
    def fade_out(self):
        '''
        Fade out animation for the popup.
        '''

        self.animation.finished.connect(self.close)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
