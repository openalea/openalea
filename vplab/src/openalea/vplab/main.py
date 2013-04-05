# -----------------------------------------------
# -------Start VirtualPlantLaboratory here-------
# -----------------------------------------------


import sys
from openalea.vpltk.qt import qt
from openalea.vplab.gui.mainwindow import MainWindow

def main():
    """
    VirtualPlantsLaboratory starts here
    """
    app = qt.QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    MainW = MainWindow()
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()
