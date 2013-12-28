import sys
from PySide.QtGui import *
from PySide.QtCore import *


class IncrementalDial(QWidget):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(IncrementalDial, self).__init__(parent)
        self.dial = QDial()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dial)

        self.dial.setWrapping(True)
        self.dial.setMaximum(360)
        self.dial.setMinimum(0)
        self.dial.setValue(0)

        self.dial.valueChanged.connect(self.on_dial_valueChanged)

        self.value = 0
        self.previous = 0
        self.current = 0

    def on_dial_valueChanged(self, value):
        self.previous = self.current
        self.current = value

        a, b = self.previous, self.current
        delta_right = b - a if b > a else b - a + self.dial.maximum()
        delta_left = delta_right - self.dial.maximum()

        if abs(delta_right) <= abs(delta_left):
            delta = delta_right
        else:
            delta = delta_left

        if delta != 0:
            self.value += delta
            self.valueChanged.emit(self.value)

    def setTicksPerRotation(self, ticks):
        self.dial.setMaximum(ticks)

    def setNotchesVisible(self, visible):
        self.dial.setNotchesVisible(visible)


class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Incremental Dial")
        self.setMinimumSize(200, 200)
        self.dial = IncrementalDial()
        self.dial.setTicksPerRotation(60 * 5)
        self.dial.valueChanged.connect(self.dialValue)
        self.setCentralWidget(self.dial)
        self.show()

    @Slot(int)
    def dialValue(self, value):
        print value


def demo():
    application = QApplication(sys.argv)
    app = Main()
    app.raise_()
    application.exec_()

if __name__ == '__main__':
    demo()
