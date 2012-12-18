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

        self.current_path = None
        
        self.set_text_editor()
        self.set_shell()
        self.set_top_buttons()
        self.set_status_bar()
        
        # window title    
        self.setWindowTitle("Open Alea Virtual Laboratory")
    
    def set_text_editor(self):
        # central widget => Editor
        self.centralWidget = Editor()
        self.setCentralWidget(self.centralWidget)
    
    def set_shell(self):
        # dock widget => Shell IPython
        self.interpreter = Interpreter()# interpreter
        shellDockWidget = qt.QDockWidget("IPython Shell", self)
        shellDockWidget.setObjectName("Shell")
        shellDockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, shellDockWidget)
        
        self.shellwdgt = ShellWidget(self.interpreter)
        shellDockWidget.setWidget(self.shellwdgt)
    
    def set_top_buttons(self):
        # set top buttons
        self.CodeBar = qt.QToolBar(self)
        # self.CodeBar.setWindowTitle(qt.QApplication.translate("MainWindow", "Code Bar", None, qt.QApplication.UnicodeUTF8))
        self.CodeBar.setToolButtonStyle(qt.Qt.ToolButtonTextBesideIcon)
        # self.CodeBar.setObjectName(_fromUtf8("CodeBar"))
        self.addToolBar(qt.Qt.TopToolBarArea, self.CodeBar)
        # Create button
        self.actionOpen = qt.QAction(self)
        self.actionSave = qt.QAction(self)
        self.actionClose = qt.QAction(self)
        self.actionRun = qt.QAction(self)
        # Set title of buttons
        self.actionOpen.setText(qt.QApplication.translate("MainWindow", "Open", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setText(qt.QApplication.translate("MainWindow", "Save", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setText(qt.QApplication.translate("MainWindow", "Close", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setText(qt.QApplication.translate("MainWindow", "Run", None, qt.QApplication.UnicodeUTF8))
        # Shortcuts
        self.actionOpen.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+O", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+S", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+W", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QApplication.UnicodeUTF8))
        # icon8 = QtGui.QIcon()
        # icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icons/run.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.actionRun.setIcon(icon8)
        # Set names
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave.setObjectName("actionSave")
        self.actionClose.setObjectName("actionClose")
        self.actionRun.setObjectName("actionRun")
        # connect actions to buttons
        qt.QObject.connect(self.actionOpen, qt.SIGNAL('triggered(bool)'),self.open)
        qt.QObject.connect(self.actionSave, qt.SIGNAL('triggered(bool)'),self.save)     
        qt.QObject.connect(self.actionClose, qt.SIGNAL('triggered(bool)'),self.close) 
        qt.QObject.connect(self.actionRun, qt.SIGNAL('triggered(bool)'),self.run)     
        self.CodeBar.addAction(self.actionOpen)
        self.CodeBar.addAction(self.actionSave)
        self.CodeBar.addAction(self.actionClose)        
        self.CodeBar.addAction(self.actionRun)
   
    def set_status_bar(self):   
        # status bar
        self.sizeLabel = qt.QLabel()     
        self.sizeLabel.setFrameStyle(qt.QFrame.StyledPanel|qt.QFrame.Sunken)
        status = self.statusBar()     
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)     
        status.showMessage("OALab is ready!", 10000)    
        
    def open(self, fname = None):
        # TODO
        try:
            fname = qt.QFileDialog.getOpenFileName(self, 'Open file', self.current_path, "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
            f = open(fname, 'r')
            data = f.read() #.rstrip("\n\r")
            # self.current_path = f.filePath()
            f.close()
            # strdata = str(data)
            self.centralWidget.set_text(data)
        except:
            pass
        
    def save(self):
        # TODO
        fname = qt.QFileDialog.getSaveFileName(self, 'Save file', self.current_path, "Python File(*.py)")
        code = self.centralWidget.get_full_text() # type(code) = unicode
        # writeList = []
        # for line in code.rstrip("\n\r"):
            # writeList.append("%s" %line.encode("iso-8859-1","ignore")) #\u240D
        # f.writelines(writeList)
        # strcode = code.encode("utf8","ignore")
        code_enc = code.encode("iso-8859-1","ignore")
        
        f = open(fname, "w")
        # f.writelines("%s" %strcode)
        f.writelines(code_enc)
        f.close()

    def close(self):
        # TODO
        pass
        
    def run(self):
        code = self.centralWidget.get_full_text()
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