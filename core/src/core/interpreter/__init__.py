try:
    from .ipython import Interpreter
except ImportError:
    from code import InteractiveInterpreter

    class Interpreter(InteractiveInterpreter):
        def __init__(self):
            super(Interpreter, self).__init__()
            self.user_nas = self.locals


def get_interpreter_class():
    """
    :return: the interpreter class to instantiate the shell
    """
    from openalea.core.util import warn_deprecated
    warn_deprecated(__name__+".get_interpreter_class", 'openalea.core.service.ipython.interpreter', (2014, 10, 8))
    return Interpreter
