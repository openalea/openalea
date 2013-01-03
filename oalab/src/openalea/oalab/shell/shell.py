from streamredirection import *

# from ipyinterpreter import IPyInterpreter
from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.frontend.qt.inprocess_kernelmanager import QtInProcessKernelManager


class ShellWidget(RichIPythonWidget,GraphicalStreamRedirection):
    """
    ShellWidget is an IPython shell.
    """
    
    def __new__(self, interpreter, message="", log='', parent=None):
        obj = RichIPythonWidget()
        obj.__class__ = ShellWidget
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
        

    def write(self, s):
        self.interpreter.shell.write(s)
