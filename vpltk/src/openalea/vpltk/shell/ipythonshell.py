from streamredirection import GraphicalStreamRedirection
from openalea.vpltk.check.ipython import has_new_ipython
if has_new_ipython():
    from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
else:
    from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget


class ShellWidget(RichIPythonWidget, GraphicalStreamRedirection):
    """
    ShellWidget is an IPython shell.
    """
    
    def __new__(self, interpreter, message="", log='', parent=None):
        obj = RichIPythonWidget()
        obj.__class__ = ShellWidget
        return obj
    
    def __init__(self, interpreter, message="", log='', parent=None):
        """
        :param interpreter : InteractiveInterpreter in which
        the code will be executed

        :param message: welcome message string
        
        :param  parent: specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """
        # Set interpreter
        self.interpreter = interpreter
        self.interpreter.widget = self

        # Multiple Stream Redirection
        GraphicalStreamRedirection.__init__(self)

        # Compatibility with visualea
        self.runsource = self.interpreter.runsource
        self.runcode = self.interpreter.runcode
        self.loadcode = self.interpreter.loadcode
        
        # Write welcome message
        self.write(message)   

        # Set kernel manager
        try:
            from IPython.qt.inprocess import QtInProcessKernelManager
        except ImportError:
            import warnings
            message = "You are using a deprecated version of IPython (please update)."
            warnings.warn(message)
            
            # DEPRECATED !
            from IPython.frontend.qt.inprocess_kernelmanager import QtInProcessKernelManager
            km = QtInProcessKernelManager(kernel=self.interpreter)
            km.start_channels()
            self.interpreter.frontends.append(km)
            self.kernel_manager = km
        else:
            km = QtInProcessKernelManager()
            km.kernel = self.interpreter
            km.kernel.gui = 'qt4'

            kernel_client = km.client()
            kernel_client.start_channels()

            self.kernel_manager = km
            self.kernel_client = kernel_client
        # # For Debug Only
        # self.interpreter.locals['shell'] = self
        
    def read(self, *args, **kwargs):
        self.kernel_client.stdin_channel.input(*args, **kwargs)
        
    def get_interpreter(self):
        """ 
        :return: the interpreter object 
        """
        return self
    
    def write(self, txt):    
        """
        Write a text in the stdout of the shell and flush it.
        :param txt: String to write.
        """
        self.interpreter.shell.write(txt)
        self.interpreter.stdout.flush()

    def push(self, var):
        """
        Push variables in the namespace.
        :param var: dict of objects
        """
        if var is not None:
            for v in var:
                self.interpreter.locals += v


def main():
    from openalea.vpltk.qt import qt as qt_
    from ipythoninterpreter import Interpreter
    import sys
    
    app = qt_.QtGui.QApplication(sys.argv)

    # Set interpreter
    interpreter = Interpreter()
    
    interpreter.locals['interp'] = interpreter
    # Set Shell Widget
    shellwdgt = ShellWidget(interpreter)
    interpreter.locals['shell'] = shellwdgt
    
    mainWindow = qt_.QtGui.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()
    
    app.exec_()
    
    
if( __name__ == "__main__"):
    main()    
