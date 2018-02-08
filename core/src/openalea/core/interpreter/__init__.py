
import sys


def get_interpreter_class():
    """
    :return: the interpreter class to instantiate the shell
    """
    Interpreter = None
    try:
        from openalea.core.interpreter.ipython import Interpreter
    except ImportError:
        from openalea.core.interpreter.python import Interpreter
    else:
        from openalea.core.interpreter import adapt_interpreter
        adapt_interpreter(Interpreter)
    return Interpreter



def get_interpreter():
    from openalea.core.util import warn_deprecated
    warn_deprecated(__name__ + ".get_interpreter", __name__ + 'interpreter', (2014, 10, 8))

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
            interpreter_klass = get_interpreter_class()
            if interpreter_klass:
                interpreter_ = interpreter_klass()
        if interpreter_:
            return interpreter_


def _interpreter_class():
    Interpreter = None
    try:
        from openalea.core.interpreter.ipython import Interpreter
    except ImportError:
        from code import InteractiveInterpreter as Interpreter

    return Interpreter


def adapt_interpreter(ip):

    def loadcode(self, source=None, namespace=None):
        """
        Load 'source' and use 'namespace' if it is in parameter.
        Else use locals.

        :param source: text (string) to load
        :param namespace: dict to use to execute the source
        """
        if namespace is not None:
            exec source in namespace
        else:
            exec source in self.locals, self.locals

    def runsource(self, source=None, filename="<input>", symbol="single"):
        try:
            return self.run_code(source)
        except:
            code = compile(source, filename, symbol)
            if code is not None:
                return self.run_code(code)

    def runcode(self, source=None):
        return self.run_code(source)

    if not hasattr(ip, 'locals'):
        ip.locals = ip.user_ns
    if not hasattr(ip, 'user_ns'):
        ip.user_ns = ip.locals

    ip.runcode = runcode
    ip.runsource = runsource
    ip.loadcode = loadcode
    if not hasattr(ip, 'shell'):
        ip.shell = ip

    return ip
