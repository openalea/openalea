from openalea.oalab.gui import qt
from openalea.oalab.editor.plugins import TextEditorOALab

# TODO : Editor type
#   1. from a flag
#   2. Retrieve the type of editor from settings
#   3. from pkg_resources:entry_point 

EDITOR = "VISUALEA"
EDITOR = "SCINTILLA"
EDITOR = "LPY"
EDITOR = "SPYDER"

PythonCodeEditor = None

if EDITOR == "SPYDER":
    # from spyderlib.widgets.editor import EditorStack
    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    class PythonCodeEditor(CodeEditor, TextEditorOALab):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__()
            self.language = 'py'
            # self.LANGUAGES = {('lpy'): (LPySH,'#', PythonCFM)}
            
        def setup(self):
            # Setup the editor
            super(PythonCodeEditor, self).setup_editor() #C:\Spyder\spyder-2.1.11\spyderlib\widgets\sourcecode\codeeditor.py l.669

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
            menuPython.setTitle(qt.QApplication.translate("MainWindow", "Python scripts", None, qt.QApplication.UnicodeUTF8))
            menuPython.setObjectName("menuPython")
            menuPython.addAction(actions)
            return menuPython.menuAction()
            
        def get_text(self, start='sof', end='eof'):
            # Return text which is contained in the editor between 'start' and 'end'
            return super(PythonCodeEditor, self).get_text(start, end)
            
        def set_text(self, text):
            # Set the text 'text' in the editor
            return super(PythonCodeEditor, self).set_text(text)

        def set_language(self, language='py'):
            # Set the language of the editor
            # 'language' can be 'py', 'lpy' or 'wf'
            # (script python, script l-system, workflow)
            self.language = language
            super(PythonCodeEditor, self).set_language(language)
        
        def get_language(self):
            # Return the language of the editor
            # 'language' can be 'py', 'lpy' or 'wf'
            # (script python, script l-system, workflow)
            return self.language
    '''
    ----QPlainTextEdit----
    doc.qt.digia.com: QPlainText uses very much the same technology and concepts as QTextEdit,
    but is optimized for plain text handling.
    - multi-language
    - syntax coloring
    - code analysis (pyflakes + pulint)
    - code completion
    - calltips
    - go-to-definition (rope)
    - function/class browser
    '''
    
    
elif EDITOR == "SCINTILLA":
    from openalea.visualea.scintilla_editor import ScintillaCodeEditor
    class PythonCodeEditor(ScintillaCodeEditor):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__()
            
        def get_full_text(self):
            return self.text()
    '''
    ----QSciScintilla----
    The QsciScintilla class implements a higher level, 
    more Qt-like, API to the Scintilla editor widget (e.g. Notepad++).
    - multi-language
    - syntax coloring
    - find and replace
    - clear
    '''

    
elif EDITOR == "VISUALEA":
    from openalea.visualea.code_editor import PythonCodeEditor as PythonCodeEditor0
    class PythonCodeEditor(PythonCodeEditor0):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__()
            
        def get_full_text(self):
            return self.text()
    '''
    ----QWidget----
    QWidget is a base class... Not optimal?
    - syntax coloring
    - "apply" and "save" buttons
    '''
    
    
elif EDITOR == "LPY":
    from openalea.lpy.gui.lpycodeeditor import LpyCodeEditor      
    class PythonCodeEditor(LpyCodeEditor):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__(parent)
        
        def get_full_text(self):
            return self.toPlainText()
    '''
    ----QTextEdit----
    - syntax coloring
    - (un)comment
    - (un)tab
    - go-to-line
    - (un)zoom
    - find and replace
    '''        
