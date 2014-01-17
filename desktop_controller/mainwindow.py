"""
A sample desktop application using the raumfeld library
"""
import time
import raumfeld
from PySide.QtCore import QThread, Signal, Slot
from PySide.QtGui import QMainWindow
from .mainwindow_ui import Ui_MainWindow as Ui

__version__ = '0.3'


class SearchThread(QThread):

    devices_found = Signal(list)

    def run(self):
        devices = raumfeld.discover()
        self.devices_found.emit(devices)


class DeviceControlThread(QThread):

    volume_infos = Signal(bool, int)

    def __init__(self, device):
        super(DeviceControlThread, self).__init__()
        self.device = device
        self._needs_update_flag = False
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            if self._needs_update_flag:
                self.device.set_volume(self._volume)
                # self.device.set_mute(self._mute)
            else:
                self._mute = self.device.get_mute()
                self._volume = self.device.get_volume()
                self.volume_infos.emit(self._mute, self._volume)

            self._needs_update_flag = False
            time.sleep(1.0)

    def set_volume(self, volume):
        self._volume = volume
        self._needs_update_flag = True

    def set_mute(self, mute):
        self._mute = mute
        self._needs_update_flag = True


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
        self.setWindowTitle('Raumfeld v%s' % __version__)
        self.setEnabled(False)

        # the dial has factor 10 more ticks than the slider
        self.ui.dialVolume.setMinimum(0)
        self.ui.dialVolume.setMaximum(1000)
        self.ui.dialVolume.setTicksPerRotation(100)

        # search for devices in a separate thread
        self.search_thread = SearchThread()
        self.search_thread.devices_found.connect(self.devices_found)
        self.search_thread.start()

    @Slot(list)
    def devices_found(self, devices):
        """
        Is called when the search thread finishes searching
        """
        try:
            self.device = devices[0]
            self.ui.lblConnection.setText(self.device.friendly_name)
            self.setEnabled(True)

            self.device_thread = DeviceControlThread(self.device)
            self.device_thread.volume_infos.connect(self.volume_infos)
            self.device_thread.start()
        except IndexError:
            # no devices found, search again
            self.search_thread.start()

    @Slot(bool, int)
    def volume_infos(self, mute, volume):
        self.ui.btnMute.setChecked(not mute)
        self.ui.btnMute.setEnabled(True)
        self.ui.sliderVolume.setValue(volume)

    @Slot(int)
    def on_dialVolume_valueChanged(self, value):
        self.ui.sliderVolume.setValue(value // 10)

    @Slot(int)
    def on_sliderVolume_valueChanged(self, value):
        self.device_thread.set_volume(value)

    @Slot()
    def on_btnMute_clicked(self):
        self.device.set_mute(self.ui.btnMute.isChecked())
        self.ui.btnMute.setEnabled(False)

    def closeEvent(self, event):
        self.search_thread.quit()
        self.device_thread.exit_flag = True
        self.device_thread.wait()
