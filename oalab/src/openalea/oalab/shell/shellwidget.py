# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

from streamredirection import GraphicalStreamRedirection

try:
    from qtconsole.rich_ipython_widget import RichJupyterWidget
except ImportError:
    from qtconsole.rich_ipython_widget import RichJupyterWidget

class ShellWidget(RichJupyterWidget, GraphicalStreamRedirection):
    """
    ShellWidget is an IPython shell.
    """

    def __new__(self, interpreter=None, message="", log='', parent=None):
        obj = RichJupyterWidget()
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
        self.runcode = self.interpreter.runcode
        self.loadcode = self.interpreter.loadcode

        # Write welcome message
        self.write(message)

        # Set kernel manager
        try:
            from qtconsole.inprocess import QtInProcessKernelManager
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
            km.kernel.gui = 'qt'

            kernel_client = km.client()
            kernel_client.start_channels()

            self.kernel_manager = km
            self.kernel_client = kernel_client

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
    from Qt import QtWidgets

    import sys

    app = QtWidgets.QApplication(sys.argv)

    from openalea.core.service.ipython import interpreter
    interpreter = interpreter()

    interpreter.user_ns['interp'] = interpreter
    shellwdgt = ShellWidget(interpreter)
    interpreter.user_ns['shell'] = shellwdgt

    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()

    app.exec_()

if(__name__ == "__main__"):
    main()

#
# shellwidget.py ends here
