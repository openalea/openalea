from streamredirection import GraphicalStreamRedirection
import sys
VERSION = 1

try:
    from qtconsole.rich_jupyter_widget import RichJupyterWidget as RichIPythonWidget
    VERSION = 2
except ImportError:
    try:
        from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
    except ImportError:
        from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget



class ShellWidget(RichIPythonWidget, GraphicalStreamRedirection):

    """
    ShellWidget is an IPython shell.
    """

    def __new__(self, interpreter=None, message="", log='', parent=None):
        obj = RichIPythonWidget()
        obj.__class__ = ShellWidget
        return obj

    def __init__(self, interpreter=None, message="", log='', parent=None):
        """
        :param interpreter : InteractiveInterpreter in which
        the code will be executed

        :param message: welcome message string

        :param  parent: specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """
        if interpreter is None:
            from openalea.core.service.ipython import interpreter
            interpreter = interpreter()
        # Set interpreter
        self.interpreter = interpreter
        self.interpreter.widget = self

        # Multiple Stream Redirection
        GraphicalStreamRedirection.__init__(self)

        # Compatibility with visualea
        self.runsource = self.interpreter.run_cell
        self.runcode = self.interpreter.run_code
        self.loadcode = self.interpreter.run_code

        # Write welcome message
        #self.write(message)

        # Set kernel manager
        try:
            from qtconsole.inprocess import QtInProcessKernelManager
        except ImportError:
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
            if VERSION == 2:
                km.kernel = self.interpreter
                km.kernel.gui = 'qt4'
            else:
                km.ipykernel = self.interpreter
                km.ipykernel.gui = 'qt4'

            kernel_client = km.client()
            kernel_client.start_channels()

            self.kernel_manager = km
            self.kernel_client = kernel_client
        # For Debug Only
        # self.interpreter.locals['shell'] = self

    def read(self, *args, **kwargs):
        self.kernel_client.stdin_channel.input(*args, **kwargs)

    def readline(self, size=None):
        from openalea.oalab.utils import raw_input_dialog
        txt = raw_input_dialog()
        self.write(txt)
        return txt

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
        sys.stdout.write(data)

    def push(self, var):
        """
        Push variables in the namespace.
        :param var: dict of objects
        """
        self.interpreter.push(var)

    def initialize(self):
        if not hasattr(self.interpreter, "shell"):
            self.interpreter.shell = self.interpreter
        if hasattr(self.interpreter.shell, "events"):
            self.interpreter.shell.events.register("post_execute", self.add_to_history)
        else:
            print("You need ipython >= 2.0 to use history.")

    def add_to_history(self, *args, **kwargs):
        """
        Send the last sent of history to the components that display history
        """
        from openalea.oalab.service.history import display_history
        records = self.interpreter.shell.history_manager.get_range()

        input_ = ''
        # loop all elements in iterator to get last one.
        # TODO: search method returning directly last input
        for session, line, input_ in records:
            pass
        display_history(input_)


def main():
    from openalea.vpltk.qt import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)

    from openalea.core.service.ipython import interpreter
    interpreter = interpreter()

    interpreter.user_ns['interp'] = interpreter
    # Set Shell Widget
    shellwdgt = ShellWidget(interpreter)
    interpreter.user_ns['shell'] = shellwdgt

    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()

    app.exec_()

def main2():
    from openalea.vpltk.qt import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)


    from qtconsole.inprocess import QtInProcessKernelManager

    kernel_manager = QtInProcessKernelManager()
    kernel_manager.start_kernel(show_banner=False)
    kernel = kernel_manager.kernel
    kernel.gui = 'qt4'

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    ipython_widget = RichIPythonWidget()
    ipython_widget.kernel_manager = kernel_manager
    ipython_widget.kernel_client = kernel_client
    ipython_widget.show()

    app.exec_()

if(__name__ == "__main__"):
    main()
