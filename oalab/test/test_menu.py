from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.menu import PanedMenu
import sys

def test_create_paned_menu():
    app = QtGui.QApplication(sys.argv)
    mainW = QtGui.QMainWindow()
    
    menu = PanedMenu()
    menu.addBtn(pane_name="Test Pane", group_name="Test Group", btn_name="Test Button", btn_icon=QtGui.QIcon(""), btn_type=0) 
    mainW.setCentralWidget(menu)
    
    mainW.show()

    app.exit(0)

