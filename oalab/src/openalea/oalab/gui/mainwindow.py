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
        
        # interpreter
        interpreter = Interpreter()
        
        # dock widget => Shell IPython
        shellDockWidget = qt.QDockWidget("IPython Shell", self)
        shellDockWidget.setObjectName("Shell")
        shellDockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, shellDockWidget)
        
        shellwdgt = ShellWidget(interpreter)
        shellDockWidget.setWidget(shellwdgt)
        
        # status bar
        self.sizeLabel = qt.QLabel()     
        self.sizeLabel.setFrameStyle(qt.QFrame.StyledPanel|qt.QFrame.Sunken)
        status = self.statusBar()     
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)     
        status.showMessage("OALab is ready!", 10000)
        
        # window title    
        self.setWindowTitle("Open Alea Virtual Laboratory")


def main():
    app = qt.QApplication(sys.argv)
    app.setStyle('Plastique')
    MainW = MainWindow()
    MainW.resize(1000, 800)
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()