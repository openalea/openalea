
try:
    from .ipython import Interpreter
except ImportError:
    from code import InteractiveInterpreter as Interpreter

def get_interpreter_class():
    """
    :return: the interpreter class to instantiate the shell
    """
    return Interpreter
