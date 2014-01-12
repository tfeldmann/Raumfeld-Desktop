from PySide.QtCore import QThread, Signal, Slot
from PySide.QtGui import QMainWindow
import raumfeld
from .mainwindow_ui import Ui_MainWindow as Ui

__version__ = '0.2'


class SearchThread(QThread):

    devices_found = Signal(list)

    def run(self):
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

        # interconnect sliders
        self.ui.dialVolume.valueChanged.connect(self.ui.sliderVolume.setValue)
        self.ui.sliderVolume.valueChanged.connect(self.ui.dialVolume.setValue)

        # create worker thread for device communication
        self.search_thread = SearchThread()
        self.search_thread.devices_found.connect(self.devices_found)
        self.search_thread.start()

    @Slot(list)
    def devices_found(self, devices):
        try:
            self.device = devices[0]
            self.ui.sliderVolume.setValue(self.device.get_volume())
            self.ui.lblConnection.setText(self.device.friendly_name)

            self.setEnabled(True)
        except:
            # no devices found, search again
            self.search_thread.start()

    @Slot(int)
    def on_dialVolume_valueChanged(self, value):
        self.device.set_volume(value)

    @Slot()
    def on_btnMute_clicked(self):
        self.device.set_mute(False)

    def closeEvent(self, event):
        self.search_thread.quit()
