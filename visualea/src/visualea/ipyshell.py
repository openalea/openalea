import os, sys
from streamredirection import *

# from ipyinterpreter import IPyInterpreter
from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.frontend.qt.inprocess_kernelmanager import QtInProcessKernelManager


class IPyShell(RichIPythonWidget,GraphicalStreamRedirection):
    """
    IPyShell is an IPython shell.
    """
    
    def __new__(self, interpreter, message="", log='', parent=None):
        obj = RichIPythonWidget()
        obj.__class__ = IPyShell
        return obj
    
    
    def __init__(self, interpreter, message="", log='', parent=None):
        """Constructor.
        @param interpreter : InteractiveInterpreter in which
        the code will be executed

        @param message : welcome message string
        
        @param  'parent' : specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """
        GraphicalStreamRedirection.__init__(self)
        
        self.interpreter = interpreter
        self.write(message)   
        
        km = QtInProcessKernelManager(kernel=self.interpreter)
        km.start_channels()
        self.interpreter.frontends.append(km)
        
        self.kernel_manager = km

        
        
    def get_interpreter(self):
        """ Return the interpreter object """
        return self.interpreter
        
     
    # def run_code(self, s):
        # self.execute(s)
        
        
    def write(self, s):
        self.interpreter.shell.write("\n" + s)

        
    # def customEvent(self,event):
        # GraphicalStreamRedirection.customEvent(self,event)
        # RichIPythonWidget.customEvent(self,event)
        
        
    # Drag and Drop support
    def dragEnterEvent(self, event):
        event.setAccepted(event.mimeData().hasFormat("text/plain"))


    def dragMoveEvent(self, event):
        if (event.mimeData().hasFormat("text/plain")):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

            
    def dropEvent(self, event):

        if(event.mimeData().hasFormat("text/plain")):
            line = event.mimeData().text()
            self.__insertTextAtEnd(line)
            self.setFocus()
            
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()
