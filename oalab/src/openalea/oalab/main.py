# -----------------------------------------------
# -------Start VirtualPlantLaboratory here-------
# -----------------------------------------------


import sys
from openalea.oalab.gui import qt
from openalea.oalab.gui.mainwindow import MainWindow

def main():
    """ VirtualPlantsLaboratory starts here """
    app = qt.QApplication(sys.argv)
    app.setStyle('plastique')
    MainW = MainWindow()
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()