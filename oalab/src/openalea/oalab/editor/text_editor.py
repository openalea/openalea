from openalea.oalab.gui import qt

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
    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    class PythonCodeEditor(CodeEditor):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__()
            
        def get_full_text(self):
            return self.get_text('sof', 'eof')

        # def set_language(self, language)    
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
