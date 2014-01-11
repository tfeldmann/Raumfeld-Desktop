import time
from PySide.QtCore import QObject, QThread, Signal, Slot
from PySide.QtGui import QMainWindow
import raumfeld
from .mainwindow_ui import Ui_MainWindow as Ui

__version__ = '0.2'


class RaumfeldWrapper(QObject):

    devices_found = Signal(list)

    def __init__(self, parent=None):
        #super(raumfeld.RaumfeldDevice, self).__init__(parent)
        super(RaumfeldWrapper, self).__init__(parent)

    @Slot()
    def discover(self):
        devices = raumfeld.discover()
        self.devices_found.emit(devices)


class MainWindow(QMainWindow):

    """
    Raumfeld Desktop Application
    """

    search_for_devices = Signal()

    def __init__(self, application=None):
        """
        Initializes the application's UI
        """
        super(MainWindow, self).__init__()
        self.ui = Ui()
        self.ui.setupUi(self)
        self.ui.dialVolume.setMinimum(0)
        self.ui.dialVolume.setMaximum(100)
        self.ui.dialVolume.setTicksPerRotation(20)
        self.setWindowTitle('Raumfeld v%s' % __version__)
        self.setEnabled(False)

        # create worker thread for device communication
        self.thread = QThread()
        self.device = RaumfeldWrapper()
        self.device.devices_found.connect(self.devices_found)
        self.search_for_devices.connect(self.device.discover)

        self.device.moveToThread(self.thread)
        self.thread.start()

        self.search_for_devices.emit()

        # interconnect sliders
        self.ui.dialVolume.valueChanged.connect(self.ui.sliderVolume.setValue)
        self.ui.sliderVolume.valueChanged.connect(self.ui.dialVolume.setValue)

    @Slot(int)
    def on_dialVolume_valueChanged(self, value):
        self.device.set_volume(value)

    @Slot()
    def on_btnMute_clicked(self):
        self.device.set_mute(True)

    @Slot(list)
    def devices_found(self, devices):
        print(devices)

    def closeEvent(self, event):
        self.thread.quit()
