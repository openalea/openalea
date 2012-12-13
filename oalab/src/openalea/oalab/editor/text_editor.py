from openalea.oalab.gui import qt

# TODO : Editor type
#   1. from a flag
#   2. Retrieve the type of editor from settings
#   3. from pkg_resources:entry_point 

EDITOR = "LPY"
EDITOR = "SPYDER"
EDITOR = "SPYDER2"
EDITOR = "VISUALEA"
EDITOR = "SCINTILLA"

PythonCodeEditor = None

if EDITOR == "SCINTILLA":
    from openalea.visualea.scintilla_editor import ScintillaCodeEditor
    PythonCodeEditor = ScintillaCodeEditor


elif EDITOR == "VISUALEA":
    from openalea.visualea.code_editor import PythonCodeEditor    
    

elif EDITOR == "SPYDER":
    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    PythonCodeEditor = CodeEditor

    
# elif EDITOR == "SPYDER2":
    # from spyderlib.widgets.editor import EditorPluginExample      
    # PythonCodeEditor = EditorPluginExample
    
    
elif EDITOR == "LPY":
    from openalea.lpy.gui.lpycodeeditor import LpyCodeEditor      
    class PythonCodeEditor(LpyCodeEditor):
        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__(parent)  
