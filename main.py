#!/usr/bin/env python2
import sys
from PySide.QtGui import QApplication
from desktop_application.mainwindow import MainWindow


def main():
    application = QApplication(sys.argv)
    app = MainWindow(application)
    app.show()
    app.raise_()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
