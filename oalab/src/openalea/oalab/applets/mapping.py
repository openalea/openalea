from openalea.oalab.gui import qt


def map_language(language):
    """
    Realize the mapping between languages and applets and widget

    :param language: language to map. It can be python, lpy or visualea.
    :return: applet, widget
    """
    if language == "py": language = "python"
    elif language == "wf": language = "visualea"

    if language == "python":
        from .python import pythonApplet
        from openalea.oalab.editor.text_editor import PythonCodeEditor
##        return  pythonApplet, PythonCodeEditor 
        return  PythonCodeEditor 
        
    elif language == "lpy":
        from .lpy import lpyApplet
        from openalea.oalab.editor.text_editor import LPyCodeEditor
##        return  lpyApplet, LPyCodeEditor 
        return  LPyCodeEditor 

    elif language == "visualea":
        print "You try to use Visualea but you can't for the moment."
        print "Visualea is not implemented yet. You can use the Python Editor."
        from .python import pythonApplet
        from openalea.oalab.editor.text_editor import PythonCodeEditor
##        return  pythonApplet, PythonCodeEditor 
        return  PythonCodeEditor 

    else:
        from .python import pythonApplet
        from openalea.oalab.editor.text_editor import PythonCodeEditor
##        return  pythonApplet, PythonCodeEditor 
        return  PythonCodeEditor
        
class SelectEditor(qt.QWidget):
    """
    This is the widget for select the type of editor/applet that you want to use.
    
    :param parent: is the widget parent. In general, it is the mainWindow.
    The parent must have a method 'new_text_editor(type)'
    """
    def __init__(self, parent=None):
        super(SelectEditor, self).__init__()
        self.parent = parent
        self._addButtons()
        
    def _addButtons(self):
        layout = qt.QVBoxLayout()
        layout.setAlignment(qt.Qt.AlignCenter)
        pythonBtn = qt.QPushButton("Python")
        pythonBtn.setMaximumSize(100,100)  
        pythonBtn.setMinimumSize(50,50)         
        lpyBtn = qt.QPushButton("L-System")
        lpyBtn.setMaximumSize(100,100)    
        lpyBtn.setMinimumSize(50,50)
        workflowBtn = qt.QPushButton("Workflow")
        workflowBtn.setMaximumSize(100,100) 
        workflowBtn.setMinimumSize(50,50)
        
        qt.QObject.connect(pythonBtn, qt.SIGNAL("clicked()"),self._clicpy)
        qt.QObject.connect(lpyBtn, qt.SIGNAL("clicked()"),self._cliclpy)
        qt.QObject.connect(workflowBtn, qt.SIGNAL("clicked()"),self._clicwf)
        
        layout.addWidget(pythonBtn)
        layout.addWidget(lpyBtn)
        layout.addWidget(workflowBtn)
        
        self.setLayout(layout)

    def _clicpy(self):
        self._clic(type="python")
        
    def _cliclpy(self):
        self._clic(type="lpy")

    def _clicwf(self):
        self._clic(type="visualea")
    
    def _clic(self, type):
        self.parent.new_text_editor(type=type)