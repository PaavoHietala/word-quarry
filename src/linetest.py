import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton('Button 1', self)
        self.button2 = QPushButton('Button 2', self)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        self.setLayout(layout)

        self.setStyleSheet('''
                            QPushButton { background-color: rgba(0, 0, 0, 0%) }
                           QLineEdit { border-radius: 5px; }
                           ''')

        self.button1.clicked.connect(self.update)
        self.button2.clicked.connect(self.update)

        self.line_drawn = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.line_drawn:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            # Set RGBA color (e.g., semi-transparent red)
            pen_color = QColor(255, 0, 0, 128)  # Red with 50% opacity
            pen = QPen(pen_color, 5, Qt.SolidLine)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)

            button1_rect = self.button1.geometry()
            button2_rect = self.button2.geometry()

            start_point = button1_rect.center()
            middle_point = QPoint((button1_rect.center().x() + button2_rect.center().x()) // 2 + 50, 
                                  button1_rect.center().y() - 50)  # Custom middle point
            end_point = button2_rect.center()

            points = [start_point, middle_point, end_point]

            painter.drawPolyline(*points)

    def update(self):
        self.line_drawn = True
        self.repaint()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Draw Line Over Buttons')

        self.custom_widget = CustomWidget()
        self.setCentralWidget(self.custom_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
