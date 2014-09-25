__all__ = ["get_interpreter"]
           
from openalea.oalab.session.session import Session
from openalea.core.interpreter import get_interpreter_class


def get_interpreter():
    if Session.instantiated:
        return Session().interpreter

    else:
        interpreter = None
        try:
            from IPython.core.getipython import get_ipython
            interpreter = get_ipython()
        except(ImportError, NameError):
            pass
        if not interpreter:
            interpreter = get_interpreter_class()()
        if interpreter:
            return interpreter
