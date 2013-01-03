#---------------------------------------------
# Main Window class
# 
# OALab start here with the 'main' function
#---------------------------------------------

import sys
import os

import qt
from openalea.oalab.editor.text_editor import PythonCodeEditor as Editor
from openalea.oalab.shell.shell import ShellWidget
from openalea.oalab.shell.interpreter import Interpreter

class MainWindow(qt.QMainWindow):
    def __init__(self, parent=None):
        super(qt.QMainWindow, self).__init__(parent)

        self.current_path = None
        self.current_file_name = None
        self.current_extension = None
        self.current_path_and_fname = None
        
        self.set_text_editor()
        self.set_shell()
        self.set_top_buttons()
        self.set_status_bar()
        self.set_menu_bar()
        self.set_menu_bar_actions() #TODO
        
        # window title    
        self.setWindowTitle("Open Alea Virtual Laboratory")
    
    def set_text_editor(self):
        # central widget => Editor
        self.centralWidget = Editor()
        self.setCentralWidget(self.centralWidget)
        self.set_language()
        
    def set_language(self, language='py'):
        if self.current_extension != None:
            self.centralWidget.set_language(self.current_extension)
        else:
            self.centralWidget.set_language(language)
    
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
        self.actionSaveAs = qt.QAction(self)
        self.actionClose = qt.QAction(self)
        self.actionRun = qt.QAction(self)
        # Set title of buttons
        self.actionOpen.setText(qt.QApplication.translate("MainWindow", "Open", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setText(qt.QApplication.translate("MainWindow", "Save", None, qt.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(qt.QApplication.translate("MainWindow", "Save As", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setText(qt.QApplication.translate("MainWindow", "Close", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setText(qt.QApplication.translate("MainWindow", "Run", None, qt.QApplication.UnicodeUTF8))
        # Shortcuts
        self.actionOpen.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+O", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+S", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+W", None, qt.QApplication.UnicodeUTF8))
        self.actionRun.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QApplication.UnicodeUTF8))
        # icon8 = qt.QIcon()
        # icon8.addPixmap(qt.QPixmap(_fromUtf8(":/images/icons/run.png")), qt.QIcon.Normal, qt.QIcon.Off)
        # self.actionRun.setIcon(icon8)
        # Set names
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionClose.setObjectName("actionClose")
        self.actionRun.setObjectName("actionRun")
        # connect actions to buttons
        qt.QObject.connect(self.actionOpen, qt.SIGNAL('triggered(bool)'),self.open)
        qt.QObject.connect(self.actionSave, qt.SIGNAL('triggered(bool)'),self.save) 
        qt.QObject.connect(self.actionSaveAs, qt.SIGNAL('triggered(bool)'),self.saveas)         
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

    def set_menu_bar(self):
        self.menubar = qt.QMenuBar()
        self.menubar.setGeometry(qt.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuPython = qt.QMenu(self.menubar)
        self.menuPython.setTitle(qt.QApplication.translate("MainWindow", "Python scripts", None, qt.QApplication.UnicodeUTF8))
        self.menuPython.setObjectName("menuPython")
        
        self.menuL_systems = qt.QMenu(self.menubar)
        self.menuL_systems.setTitle(qt.QApplication.translate("MainWindow", "L-systems", None, qt.QApplication.UnicodeUTF8))
        self.menuL_systems.setObjectName("menuL_systems")
        
        self.menuWorkflow = qt.QMenu(self.menubar)
        self.menuWorkflow.setTitle(qt.QApplication.translate("MainWindow", "Workflow", None, qt.QApplication.UnicodeUTF8))
        self.menuWorkflow.setObjectName("menuWorkflow")
        
        self.menuFile = qt.QMenu(self.menubar)
        self.menuFile.setTitle(qt.QApplication.translate("MainWindow", "File", None, qt.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName("menuFile")
        
        self.menuRecents = qt.QMenu(self.menuFile)
        self.menuRecents.setTitle(qt.QApplication.translate("MainWindow", "Recents", None, qt.QApplication.UnicodeUTF8))
        self.menuRecents.setObjectName("menuRecents")
        
        self.menuImport = qt.QMenu(self.menuFile)
        self.menuImport.setTitle(qt.QApplication.translate("MainWindow", "Import", None, qt.QApplication.UnicodeUTF8))
        self.menuImport.setObjectName("menuImport")
        
        self.menuEdit = qt.QMenu(self.menubar)
        self.menuEdit.setTitle(qt.QApplication.translate("MainWindow", "Edit", None, qt.QApplication.UnicodeUTF8))
        self.menuEdit.setObjectName("menuEdit")
        
        self.menuHelp = qt.QMenu(self.menubar)
        self.menuHelp.setTitle(qt.QApplication.translate("MainWindow", "Help", None, qt.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName("menuHelp")
        
        self.menuView = qt.QMenu(self.menubar)
        self.menuView.setTitle(qt.QApplication.translate("MainWindow", "View", None, qt.QApplication.UnicodeUTF8))
        self.menuView.setObjectName("menuView")
        
        self.setMenuBar(self.menubar)
        
    def set_menu_bar_actions(self):   
        self.menuPython.addAction(self.actionRun)
        self.menuPython.addSeparator()
        self.menuWorkflow.addSeparator()
        # self.menuL_systems.addAction(self.actionRun)
        # self.menuL_systems.addAction(self.actionAnimate)
        self.menuL_systems.addSeparator()
        # self.menuL_systems.addAction(self.actionStep)
        # self.menuL_systems.addAction(self.actionRewind)
        # self.menuL_systems.addAction(self.actionStop)
        # self.menuL_systems.addAction(self.actionStepInterpretation)
        self.menuL_systems.addSeparator()
        # self.menuL_systems.addAction(self.actionIterateTo)
        # self.menuL_systems.addAction(self.actionNextIterate)
        self.menuL_systems.addSeparator()
        # self.menuL_systems.addAction(self.actionAutoRun)
        self.menuL_systems.addSeparator()
        # self.menuL_systems.addAction(self.actionDebug)
        # self.menuL_systems.addAction(self.actionProfile)
        self.menuL_systems.addSeparator()
        # self.menuL_systems.addAction(self.actionRecord)
        # self.menuRecents.addAction(self.actionClear)
        # self.menuImport.addAction(self.actionImportCpfgProject)
        # self.menuImport.addAction(self.actionImportCpfgFile)
        # self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        # self.menuFile.addAction(self.actionSaveAll)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        # self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        # self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        # self.menuFile.addAction(self.menuRecents.menuAction())
        self.menuFile.addSeparator()
        # self.menuFile.addAction(self.actionExit)
        # self.menuEdit.addAction(self.actionUndo)
        # self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionCopy)
        # self.menuEdit.addAction(self.actionCut)
        # self.menuEdit.addAction(self.actionPaste)
        # self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionComment)
        # self.menuEdit.addAction(self.actionUncomment)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionInsertTab)
        # self.menuEdit.addAction(self.actionRemoveTab)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionFind)
        # self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionGoto)
        self.menuEdit.addSeparator()
        # self.menuEdit.addAction(self.actionPreferences)
        # self.menuHelp.addAction(self.actionAbout)
        # self.menuHelp.addAction(self.actionAboutQt)
        # self.menuHelp.addAction(self.actionAboutVPlants)
        self.menuHelp.addSeparator()
        # self.menuHelp.addAction(self.actionOnlineHelp)
        # self.menuHelp.addAction(self.actionSubmitBug)
        self.menuHelp.addSeparator()
        # self.menuView.addAction(self.actionZoomIn)
        # self.menuView.addAction(self.actionZoomOut)
        # self.menuView.addAction(self.actionNoZoom)
        self.menuView.addSeparator()
        # self.menuView.addAction(self.actionSyntax)
        # self.menuView.addAction(self.actionTabHightlight)
        self.menuView.addSeparator()
        # self.menuView.addAction(self.actionView3D)
        self.menuView.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPython.menuAction())
        self.menubar.addAction(self.menuL_systems.menuAction())
        self.menubar.addAction(self.menuWorkflow.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        
    def edit_status_bar(self, message, time=10000):   
        status = self.statusBar()
        status.showMessage(message, time) 
        
    def open(self, fname = None):
        try:
            fname = qt.QFileDialog.getOpenFileName(self, 'Open file', self.current_path, "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
            f = open(fname, 'r')
            data = f.read()
            # TODO
            fnamesplit = os.path.split(fname)
            fnamesplitext = os.path.splitext(fname)
            self.current_path_and_fname = fname
            self.current_path = fnamesplit[0]
            self.current_file_name = fnamesplit[1]
            self.current_extension = fnamesplitext[1][1:]
            f.close()
            try:
                self.centralWidget.set_text(data.decode("utf8"))#.decode("utf8")
            except:
                self.centralWidget.set_text(data)
            self.edit_status_bar(("File '%s' opened.") %self.current_file_name)
            
            self.set_language()
        except:
            self.edit_status_bar("No file opened...")
    
    def save(self):
        if(self.current_file_name==None):
            self.edit_status_bar("Save as...")
            self.saveas()
        else:
            try:
                code = self.centralWidget.get_full_text() # type(code) = unicode

                fname = self.current_path_and_fname
                # Encode in utf8
                # /!\ 
                # encode("iso-8859-1","ignore") don't know what to do with "\n" and so ignore it
                # encode("utf8","ignore") works well but the read function need decode("utf8")
                code_enc = code.encode("utf8","ignore") #utf8 or iso-8859-1, ignore or replace
                
                # Write text in the file
                f = open(fname, "w")
                f.writelines(code_enc)
                f.close()
                
                self.edit_status_bar(("File '%s' saved.") % self.current_file_name) 
            except:
                self.edit_status_bar("File not saved...") 
    
    def saveas(self):
        try:
            fname = qt.QFileDialog.getSaveFileName(self, 'Save file', self.current_path, "Python File(*.py)")
            code = self.centralWidget.get_full_text()
            code_enc = code.encode("utf8","ignore") 
            
            f = open(fname, "w")
            f.writelines(code_enc)
            f.close()
            
            self.edit_status_bar(("File '%s' saved.") % self.current_file_name)  
        except:
            self.edit_status_bar("File not saved...")  

    def close(self):
        try:
            self.centralWidget.clear_all()
            self.edit_status_bar(("File '%s' closed.") % self.current_file_name)
            self.current_file_name = None
            self.current_extension = None
        except:
            self.edit_status_bar("No file closed...")
        
    def run(self):
        code = self.centralWidget.get_full_text()
        interp = self.get_interpreter()
        interp.runsource(code)
        self.edit_status_bar("Code runned.")

    def get_interpreter(self):
        return self.interpreter


def main():
    app = qt.QApplication(sys.argv)
    app.setStyle('windows')
    MainW = MainWindow()
    MainW.resize(1000, 750)
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()