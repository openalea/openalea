from openalea.oalab.plugins import TextEditorOALab
from spyderlib.widgets.sourcecode.codeeditor import CodeEditor


class LPyEditor(CodeEditor, TextEditorOALab):
    __plugin_name__ = 'MonBeauEditeurLPy'
    __categorie__ = 'TextEditor'

    
    def __init__(self, parent=None):
        super(LPyEditor, self).__init__()
        
    def setup(self):
        # Setup the editor
        super(LPyEditor, self).setup_editor() #C:\Spyder\spyder-2.1.11\spyderlib\widgets\sourcecode\codeeditor.py l.669
        
    def set_actions(self):    
        actionRun = qt.QAction(self)
        actionRun.setText(qt.QApplication.translate("MainWindow", "Run", None, qt.QApplication.UnicodeUTF8))
        return actionRun
        
    def set_buttons(self, actionRun, window):
        # Create qt btns and connect actions
        actionRun.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QApplication.UnicodeUTF8))
        icon3 = qt.QIcon()
        icon3.addPixmap(qt.QPixmap("./resources/run.png"), qt.QIcon.Normal, qt.QIcon.Off)
        actionRun.setIcon(icon3)
        qt.QObject.connect(actionRun, qt.SIGNAL('triggered(bool)'),window.run)
        return actionRun
        
    def set_menu(self, menubar, actions):
        # Return qt actions
        menuPython = qt.QMenu(menubar)
        menuPython.setTitle(qt.QApplication.translate("MainWindow", "LPy scripts", None, qt.QApplication.UnicodeUTF8))
        menuPython.setObjectName("menuPython")
        menuPython.addAction(actions)
        return menuPython.menuAction()
        
    def get_text(self, start='sof', end='eof'):
        # Return text which is contained in the editor between 'start' and 'end'
        return super(PythonCodeEditor, self).get_text(start, end)
        
    def set_text(self, text):
        # Set the text 'text' in the editor
        return super(PythonCodeEditor, self).set_text(text)