from PySide.QtGui import QProgressDialog
from controllers.mainwindow import mainwindow, database_settings

__author__ = 'anton'

import sys
from PySide import QtGui, QtCore

def main():
    app = QtGui.QApplication(sys.argv)

    ex = mainwindow()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()