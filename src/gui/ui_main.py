

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from uisource import Ui_CiscoWipe
from tech.tech import Tech_stuff

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    CiscoWipe = QtWidgets.QMainWindow()
    ui = Ui_CiscoWipe()
    
    ui.setupUi(CiscoWipe)

    ui.techit.clicked.connect(Tech_stuff(ui.pallet, ui.process, ui.grade, ui.compliance, ui.asset))

    CiscoWipe.show()

    sys.exit(app.exec_())

main()
 