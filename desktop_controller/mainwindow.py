"""
A sample desktop application using the raumfeld library
"""
import time
from PySide import QtCore, QtGui
import raumfeld

__version__ = '0.3'


class SearchThread(QtCore.QThread):

    devices_found = QtCore.Signal(list)

    def run(self):
        devices = raumfeld.discover()
        self.devices_found.emit(devices)
        for device in devices:
            print(device.location)


class DeviceControlThread(QtCore.QThread):

    volume_infos = QtCore.Signal(bool, int)

    def __init__(self):
        super(DeviceControlThread, self).__init__()
        self.device = None
        self._needs_update_flag = False
        self.exit_flag = False

    def run(self):
        """
        Poll volume and mute setting
        """
        while not self.exit_flag:
            if self.device is None:
                continue

            if self._needs_update_flag:
                self.device.volume = self._volume
            else:
                self.volume_infos.emit(self.device.mute, self.device.volume)

            self._needs_update_flag = False
            time.sleep(1.0)

    def set_volume(self, volume):
        self._volume = volume
        self._needs_update_flag = True

    def set_mute(self, mute):
        self._mute = mute
        self._needs_update_flag = True


class MainWindow(QtGui.QMainWindow):

    """
    Raumfeld Desktop Application
    """

    search_for_devices = QtCore.Signal()

    def __init__(self, parent=None):
        """
        Initializes the application's UI
        """
        from .mainwindow_ui import Ui_MainWindow as Ui
        super(MainWindow, self).__init__()
        self.ui = Ui()
        self.ui.setupUi(self)
        self.setWindowTitle('Raumfeld v%s' % __version__)
        self.setEnabled(False)

        # the dial has factor 10 more ticks than the slider
        self.ui.dialVolume.setMinimum(0)
        self.ui.dialVolume.setMaximum(1000)
        self.ui.dialVolume.setTicksPerRotation(100)

        # open a thread to search for devices
        self.search_thread = SearchThread()
        self.search_thread.devices_found.connect(self.devices_found)
        self.search_thread.start()

        # create a worker thread to communicate with the device
        self.device_thread = DeviceControlThread()
        self.device_thread.volume_infos.connect(self.volume_infos)
        # the device thread is started as soon as a device is found

    def devices_found(self, devices):
        """Is called when the search thread finishes searching
        """
        try:
            device = devices[0]
            self.ui.lblConnection.setText(device.friendly_name)
            self.setEnabled(True)

            self.device_thread.device = device
            self.device_thread.start()
        except IndexError:
            # no devices found, search again
            self.search_thread.start()

    def volume_infos(self, mute, volume):
        self.ui.dialVolume.setValue(volume * 10)

    #
    # View Callbacks
    #

    @QtCore.Slot(int)
    def on_dialVolume_valueChanged(self, value):
        self.ui.sliderVolume.setValue(value // 10)
        self.device_thread.set_volume(value // 10)

    @QtCore.Slot(int)
    def on_sliderVolume_sliderMoved(self, value):
        self.ui.dialVolume.setValue(value * 10)

    @QtCore.Slot(bool)
    def on_btnMute_toggled(self, checked):
        self.device_thread.set_mute(checked)
        self.ui.btnMute.setEnabled(False)

    def closeEvent(self, event):
        self.search_thread.wait()
        self.device_thread.exit_flag = True
        self.device_thread.wait()
