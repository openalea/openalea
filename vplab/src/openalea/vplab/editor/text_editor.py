from openalea.vpltk.qt import qt
from openalea.vplab.editor.plugins import TextEditorVPLab
import os

# TODO : Editor type
#   1. from a flag
#   2. Retrieve the type of editor from settings
#   3. from pkg_resources:entry_point 

EDITOR = "SPYDER"
EDITOR = "SCINTILLA"

LPYEDITOR = "SPYDER"
LPYEDITOR = "LPY"
LPYEDITOR = "SCINTILLA"

PythonCodeEditor = None
LPyCodeEditor = None

'''
if LPYEDITOR == "SPYDER":
    # from spyderlib.widgets.editor import EditorStack
    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    class LPyCodeEditor(CodeEditor, TextEditorVPLab):
        def __init__(self, parent=None):
            super(LPyCodeEditor, self).__init__()
            self.language = 'lpy'
            # self.LANGUAGES = {('lpy'): (LPySH,'#', PythonCFM)}
            
        def setup(self):
            # Setup the editor
            super(LPyCodeEditor, self).setup_editor() #C:\Spyder\spyder-2.1.11\spyderlib\widgets\sourcecode\codeeditor.py l.669
            
        def set_actions(self):    
            actionRun = qt.QtGui.QAction(self)
            actionRun.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
            return actionRun
            
        def set_buttons(self, actionRun, window):
            # Create qt btns and connect actions
            actionRun.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QtGui.QApplication.UnicodeUTF8))
            icon3 = qt.QtGui.QIcon()
            icon3.addPixmap(qt.QtGui.QPixmap("./resources/new/run.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
            actionRun.setIcon(icon3)
            qt.QtCore.QObject.connect(actionRun, qt.QtCore.SIGNAL('triggered(bool)'),window.run)
            return actionRun
            
        def set_menu(self, menubar, actions):
            # Return qt actions
            menuPython = qt.QMenu(menubar)
            menuPython.setTitle(qt.QtGui.QApplication.translate("MainWindow", "LPy scripts", None, qt.QtGui.QApplication.UnicodeUTF8))
            menuPython.setObjectName("menuPython")
            menuPython.addAction(actions)
            return menuPython.menuAction()
            
        def get_text(self, start='sof', end='eof'):
            # Return text which is contained in the editor between 'start' and 'end'
            return super(LPyCodeEditor, self).get_text(start, end)
            
        def set_text(self, text):
            # Set the text 'text' in the editor
            return super(LPyCodeEditor, self).set_text(text)

        def set_language(self, language='lpy'):
            # Set the language of the editor
            # 'language' can be 'py', 'lpy' or 'wf'
            # (script python, script l-system, workflow)
            self.language = language
            super(LPyCodeEditor, self).set_language(language)
        
        def get_language(self):
            # Return the language of the editor
            # 'language' can be 'py', 'lpy' or 'wf'
            # (script python, script l-system, workflow)
            return self.language
            
        def get_widgets_controls(self):
            pass
    """
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
    """
'''   

if LPYEDITOR == "LPY":
    from openalea.lpy.gui.lpycodeeditor import LpyCodeEditor, Margin      
    class LPyCodeEditor(LpyCodeEditor, TextEditorVPLab):
        def __init__(self, parent=None):
            super(LPyCodeEditor, self).__init__(parent)
            self.set_name('LPyEditor')
            self.set_language('lpy')
            from openalea.lpy.gui.lpystudio import LPyWindow
            self.initWithEditor(LPyWindow())
            self.setup()     

        def setup(self):
            self.sidebar = Margin(self,self)
            self.sidebar.hide() 
        
        def get_full_text(self):
            """
            :return: the full text in the editor
            """
            return self.toPlainText()
        
        def get_text(self, start='sof', end='eof'):
            """
            Return a part of the text.
            
            :param start: is the begining of what you want to get
            :param end: is the end of what you want to get
            :return: text which is contained in the editor between 'start' and 'end'
            """
            return self.toPlainText()
        
        def set_text(self, txt): 
            """
            Set text in the editor
            
            :param text: text you want to set 
            """
            cursor = self.textCursor()
            cursor.insertText(txt)
            
        '''    
        def set_actions(self):    
            actionRun = qt.QtGui.QAction(self)
            actionRun.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
            return actionRun
            
        def set_buttons(self, actionRun, window):
            # Create qt btns and connect actions
            actionRun.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QtGui.QApplication.UnicodeUTF8))
            icon3 = qt.QtGui.QIcon()
            icon3.addPixmap(qt.QtGui.QPixmap("./resources/new/run.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
            actionRun.setIcon(icon3)
            qt.QtCore.QObject.connect(actionRun, qt.QtCore.SIGNAL('triggered(bool)'),window.run)
            return actionRun
        '''    

   

elif LPYEDITOR == "SCINTILLA":
    from openalea.visualea.scintilla_editor import ScintillaCodeEditor
    from openalea.plantgl import all as pgl
    from openalea.lpy_wralea.lpy_nodes import run_lpy
    class LPyCodeEditor(ScintillaCodeEditor, TextEditorVPLab):
        def __init__(self, parent=None):
            super(LPyCodeEditor, self).__init__()
            
        def get_full_text(self):
            """
            :return: the full text in the editor
            """
            return self.text()
            
        def get_text(self, start='sof', end='eof'):
            """
            Return a part of the text.
            
            :param start: is the begining of what you want to get
            :param end: is the end of what you want to get
            :return: text which is contained in the editor between 'start' and 'end'
            """
            return super(LPyCodeEditor, self).text()
            
        def set_text(self, text):
            """
            Set text in the editor
            
            :param text: text you want to set 
            """
            return super(LPyCodeEditor, self).setText(text)    
            
        def set_actions(self):
            """
            .. todo:: Move this to applets
            """
            actionRun = qt.QtGui.QAction(self)
            actionRun.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
            return actionRun
            
        def set_buttons(self, actionRun, window):
            """
            .. todo:: Move this to applets
            """
            # Create qt btns and connect actions
            self.window = window
            actionRun.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QtGui.QApplication.UnicodeUTF8))
            icon3 = qt.QtGui.QIcon()
            icon3.addPixmap(qt.QtGui.QPixmap("./resources/new/run.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
            actionRun.setIcon(icon3)
            qt.QtCore.QObject.connect(actionRun, qt.QtCore.SIGNAL('triggered(bool)'),self.run)
            return actionRun    

        def run(self):
            code = self.get_text()
            ns = self.window.current_project.ns
   
            file = open('.mytemplpy.lpy', "w")
            file.write(code)
            file.close()    

            tree, lsys = run_lpy('.mytemplpy.lpy', parameters=ns)
    
            os.remove('.mytemplpy.lpy')

            scene = lsys.sceneInterpretation(tree)
            self.window.history.add(name='lpy',obj=scene)
        
    


if EDITOR == "SPYDER":
    # from spyderlib.widgets.editor import EditorStack as CodeEditor
    # from spyderlib.plugins.editor import Editor as CodeEditor
    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    class PythonCodeEditor(CodeEditor, TextEditorVPLab):
        def __init__(self, parent):
            super(PythonCodeEditor, self).__init__(parent)
            self.language = 'py'
            # print super(PythonCodeEditor, self).get_shortcut_data()
            
            # self.LANGUAGES = {('lpy'): (LPySH,'#', PythonCFM)}
            
        # def codecomp(self):
            # print '0'
            # super(PythonCodeEditor, self).do_code_completion()
            
        def setup(self):
            # Setup the editor
            super(PythonCodeEditor, self).setup_editor(go_to_definition=True) #C:\Spyder\spyder-2.1.11\spyderlib\widgets\sourcecode\codeeditor.py l.669
            
        def set_actions(self):    
            actionRun = qt.QtGui.QAction(self)
            actionRun.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
            return actionRun
            
        def set_buttons(self, actionRun, window):
            # Create qt btns and connect actions
            actionRun.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QtGui.QApplication.UnicodeUTF8))
            icon3 = qt.QtGui.QIcon()
            icon3.addPixmap(qt.QtGui.QPixmap("./resources/run.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
            actionRun.setIcon(icon3)
            qt.QtCore.QObject.connect(actionRun, qt.QtCore.SIGNAL('triggered(bool)'),window.run)
            return actionRun
            
        def set_menu(self, menubar, actions):
            # Return qt actions
            menuPython = qt.QMenu(menubar)
            menuPython.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Python scripts", None, qt.QtGui.QApplication.UnicodeUTF8))
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
    class PythonCodeEditor(ScintillaCodeEditor, TextEditorVPLab):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__()
            
        def get_full_text(self):
            """
            :return: the full text in the editor
            """
            return self.text()
            
        def get_text(self, start='sof', end='eof'):
            """
            Return a part of the text.
            
            :param start: is the begining of what you want to get
            :param end: is the end of what you want to get
            :return: text which is contained in the editor between 'start' and 'end'
            """
            return super(PythonCodeEditor, self).text()
            
        def set_text(self, text):
            """
            Set text in the editor
            
            :param text: text you want to set 
            """
            return super(PythonCodeEditor, self).setText(text)    
            
        def set_actions(self):
            """
            .. todo:: Move this to applets
            """
            actionRun = qt.QtGui.QAction(self)
            actionRun.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
            return actionRun
            
        def set_buttons(self, actionRun, window):
            """
            .. todo:: Move this to applets
            """
            # Create qt btns and connect actions
            self.window = window
            actionRun.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, qt.QtGui.QApplication.UnicodeUTF8))
            icon3 = qt.QtGui.QIcon()
            icon3.addPixmap(qt.QtGui.QPixmap("./resources/new/run.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
            actionRun.setIcon(icon3)
            qt.QtCore.QObject.connect(actionRun, qt.QtCore.SIGNAL('triggered(bool)'),self.run)
            return actionRun    

        def run(self):
            code = self.get_text()
            interp = self.window.get_interpreter()
            interp.runcode(code)
            self.window.edit_status_bar("Code runned.")
