#---------------------------------------------
# Main Window class
# 
# OALab start here with the 'main' function
#---------------------------------------------

import sys

import qt
from openalea.oalab.editor.text_editor import PythonCodeEditor as Editor
from openalea.oalab.shell.shell import ShellWidget
from openalea.oalab.shell.interpreter import Interpreter

class MainWindow(qt.QMainWindow):
    def __init__(self, parent=None):
        super(qt.QMainWindow, self).__init__(parent)
        
        # central widget => Editor
        self.centralWidget = Editor()
        self.setCentralWidget(self.centralWidget)
        
        # dock widget => Shell IPython
        self.interpreter = Interpreter()# interpreter
        shellDockWidget = qt.QDockWidget("IPython Shell", self)
        shellDockWidget.setObjectName("Shell")
        shellDockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, shellDockWidget)
        
        self.shellwdgt = ShellWidget(self.interpreter)
        shellDockWidget.setWidget(self.shellwdgt)
        
        # top buttons
        
        self.CodeBar = qt.QToolBar(self)
        # self.CodeBar.setWindowTitle(qt.QApplication.translate("MainWindow", "Code Bar", None, qt.QApplication.UnicodeUTF8))
        self.CodeBar.setToolButtonStyle(qt.Qt.ToolButtonTextBesideIcon)
        # self.CodeBar.setObjectName(_fromUtf8("CodeBar"))
        self.addToolBar(qt.Qt.TopToolBarArea, self.CodeBar)
        
        self.actionRun = qt.QAction(self)
        # icon8 = QtGui.QIcon()
        # icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icons/run.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.actionRun.setIcon(icon8)
        self.actionRun.setText(qt.QApplication.translate("MainWindow", "Run", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setObjectName("actionRun")
        
                   
        qt.QObject.connect(self.actionRun, qt.SIGNAL('triggered(bool)'),self.run)     

        self.CodeBar.addAction(self.actionRun)
        
        # status bar
        self.sizeLabel = qt.QLabel()     
        self.sizeLabel.setFrameStyle(qt.QFrame.StyledPanel|qt.QFrame.Sunken)
        status = self.statusBar()     
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)     
        status.showMessage("OALab is ready!", 10000)
        
        # window title    
        self.setWindowTitle("Open Alea Virtual Laboratory")
        
    def run(self):
        code = self.centralWidget.text()
        interp = self.get_interpreter()
        interp.runsource(code)

    def get_interpreter(self):
        return self.interpreter


def main():
    app = qt.QApplication(sys.argv)
    app.setStyle('Plastique')
    MainW = MainWindow()
    MainW.resize(1000, 800)
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()