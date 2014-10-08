__all__ = ["get_interpreter", "interpreter"]
from openalea.core.util import warn_deprecated


def get_interpreter():
    warn_deprecated(__name__+".get_interpreter", __name__+'interpreter', (2014, 10, 8))
    from openalea.oalab.session.session import Session
    if Session.instantiated:
        return Session().interpreter
    else:
        interpreter_ = None
        try:
            from IPython.core.getipython import get_ipython
            interpreter_ = get_ipython()
        except(ImportError, NameError):
            pass
        if not interpreter_:
            from openalea.core.interpreter import get_interpreter_class
            interpreter_ = get_interpreter_class()()
        if interpreter_:
            return interpreter_


def _interpreter_class():
    try:
        from openalea.core.interpreter.ipython import Interpreter
    except ImportError:
        from code import InteractiveInterpreter

        class Interpreter(InteractiveInterpreter):
            def run_cell(self, code):
                return self.runcode(code)

            @property
            def user_ns(self):
                return self.locals

            @user_ns.setter
            def user_ns(self, ns):
                self.locals = ns

    return Interpreter

_interpreter = []


def interpreter():
    """
    :return: a unique instance of advanced interpreter that respect interface IInterpreter
    """
    if _interpreter:
        return _interpreter[0]
    else:
        try:
            from IPython.core.getipython import get_ipython
            ip = get_ipython()
            if ip is None:
                Interpreter = _interpreter_class()
                _interpreter.append(Interpreter())
                return _interpreter[0]
            else:
                # We can adapt ipython interpreter here to use openalea with ipython
                # ex:
                # ip.locals = ip.user_ns
                _interpreter.append(ip)
                return _interpreter[0]
        except(ImportError, NameError):
            Interpreter = _interpreter_class()
            _interpreter.append(Interpreter())
            return _interpreter[0]


class IInterpreter(object):
    """
    TODO: complete
    """
    def run_cell(self, raw_cell, store_history=False, silent=False, shell_futures=True):
        pass

    def runcode(self, code_obj):
        pass

    def push(self, variables, interactive=True):
        pass