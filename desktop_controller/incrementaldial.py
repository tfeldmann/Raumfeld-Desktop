from PySide.QtGui import QWidget, QDial, QVBoxLayout
from PySide.QtCore import Signal, Slot


class IncrementalDial(QWidget):

    """
    A dial that works incrementally instead of having a minimum and maximum.
    """

    valueChanged = Signal(int)
    dialReleased = Signal()

    def __init__(self, parent=None):
        super(IncrementalDial, self).__init__(parent)
        self.dial = QDial()
        layout = QVBoxLayout()
        layout.addWidget(self.dial)
        self.setLayout(layout)

        self.dial.setWrapping(True)
        self.dial.setMaximum(100)
        self.dial.setMinimum(0)
        self.dial.setValue(0)

        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        self.dial.sliderReleased.connect(self.on_dial_sliderReleased)

        self._value = 0
        self._previous = 0
        self._current = 0

        self._minimum = None
        self._maximum = None

    @Slot(int)
    def on_dial_valueChanged(self, value):
        self._previous = self._current
        self._current = value

        a, b = self._previous, self._current
        delta_right = b - a if b > a else b - a + self.dial.maximum()
        delta_left = delta_right - self.dial.maximum()

        if abs(delta_right) <= abs(delta_left):
            delta = delta_right
        else:
            delta = delta_left

        if delta != 0:
            self._value += delta

            # apply boundaries
            if self._maximum is not None and self._value > self._maximum:
                self._value = self._maximum
            elif self._minimum is not None and self._value < self._minimum:
                self._value = self._minimum

            self.valueChanged.emit(self._value)

    @Slot()
    def on_dial_sliderReleased(self):
        self.dialReleased.emit()

    def setTicksPerRotation(self, ticks):
        self.dial.setMaximum(ticks)

    def setNotchesVisible(self, visible):
        self.dial.setNotchesVisible(visible)

    def setValue(self, value):
        self._value = value

        # apply boundaries
        if self._maximum is not None and self._value > self._maximum:
            self._value = self._maximum
        elif self._minimum is not None and self._value < self._minimum:
            self._value = self._minimum

        self.valueChanged.emit(self._value)

    def value(self):
        return self._value

    def setMinimum(self, value):
        self._minimum = value

    def minimum(self):
        return self._minimum

    def setMaximum(self, value):
        self._maximum = value

    def maximum(self):
        return self._maximum
