import sys, os
import signal

from PyQt4 import QtGui
from PyQt4 import QtCore

import ui_mainwindow


class MainWindow(QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow):
    """ Main configuration window """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Signal connection
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), self.proceed)
        self.connect(self.refreshButton, QtCore.SIGNAL("clicked()"), self.refresh)

    def proceed(self):
        pass


    def refresh(self):
        pass
        

  

def main(args=None):

    if args is None : args = sys.argv
    
    # Restore default signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
       
    app = QtGui.QApplication(args)

    win = MainWindow()
    win.show()
    
    return app.exec_()



if __name__ == "__main__":


    main(sys.argv)
    
