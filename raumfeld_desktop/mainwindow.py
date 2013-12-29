from PySide.QtCore import Slot, QTimer
from PySide.QtGui import QMainWindow
import raumfeld
from .mainwindow_ui import Ui_MainWindow as Ui

__version__ = '0.1'


class MainWindow(QMainWindow):

    """
    Photonix Application
    """

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
        self.ui.dialVolume.setNotchesVisible(True)
        self.setWindowTitle('Raumfeld Desktop v%s' % __version__)
        self.setEnabled(False)

        QTimer.singleShot(500, self.connect)

        # interconnect sliders
        self.ui.dialVolume.valueChanged.connect(self.ui.sliderVolume.setValue)
        self.ui.sliderVolume.valueChanged.connect(self.ui.dialVolume.setValue)

    def connect(self):
        self.device = raumfeld.discover()[0]
        self.ui.lblConnection.setText(self.device.friendly_name)
        self.setEnabled(True)

    @Slot(int)
    def on_dialVolume_valueChanged(self, value):
        self.device.set_volume(value)

    @Slot()
    def on_btnMute_clicked(self):
        self.device.set_mute(True)
