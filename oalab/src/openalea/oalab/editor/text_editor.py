from openalea.oalab.gui import qt

# TODO : Editor type
#   1. from a flag
#   2. Retrieve the type of editor from settings
#   3. from pkg_resources:entry_point 

EDITOR = "SCINTILLA"
EDITOR = "VISUALEA"
EDITOR = "LPY"
EDITOR = "SPYDER"

PythonCodeEditor = None

if EDITOR == "SCINTILLA":
    from openalea.visualea.scintilla_editor import ScintillaCodeEditor
    PythonCodeEditor = ScintillaCodeEditor
# class PythonCodeEditor(ScintillaCodeEditor):
    # """
    # This is the secondnature editor (which come from visualea which come from QsciScintilla)

    # Advantages:
    # - syntax color
    # - line number
    # - finder
    # - multi-languages
    # """
    # def __init__(self):
        # super(PythonCodeEditor, self).__init__()


# CodeWidget        
elif EDITOR == "VISUALEA":
# PythonCodeEditor

    from openalea.visualea.code_editor import PythonCodeEditor
    
elif EDITOR == "LPY":


    # LpyCodeEditor

    from openalea.lpy.gui.lpycodeeditor import LpyCodeEditor      
    class PythonCodeEditor(LpyCodeEditor):
        """
        This is a visualea editor

        Advantages:
        - really good but complex...
        """

        def __init__(self, parent=None):
            super(PythonCodeEditor, self).__init__(parent)        

elif EDITOR == "SPYDER":


    # CodeEditor

    from spyderlib.widgets.sourcecode.codeeditor import CodeEditor      
    PythonCodeEditor = CodeEditor
