

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from uisource import Ui_CiscoWipe

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    CiscoWipe = QtWidgets.QMainWindow()
    ui = Ui_CiscoWipe()
    ui.setupUi(CiscoWipe)
    CiscoWipe.show()
