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

__all__ = ["get_interpreter", "interpreter"]

class IInterpreterPlugin(object):

    """
    entry_point: openalea.interpreter
    """
    name = 'InterpreterName'

    def __call__(self):
        """
        :return: interpreter class following IInterpreter interface
        """

class IInterpreter(object):

    """
    Class able to interprete python code

    entry_point: openalea.interpreter
    """

    def __init__(self, *args, **kwargs):
        """
        current interpreter namespace
        """
        self.user_ns = dict()

    def run_cell(self, raw_cell, **kwargs):
        """Run a complete IPython cell.

        :param raw_cell: The code (including IPython code such as %magic functions) to run.
        :type raw_cell: :obj:`str`
        """

    def run_code(self, code_obj):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to display a
        traceback.

        :param code_obj: code object, A compiled code object, to be executed
        :return False : successful execution, True : an error occurred.
        """

    def reset(self, namespace=None, **kwargs):
        """Clear all internal namespaces, and attempt to release references to
        user objects.
        If namespace is specified, use it to populate interpreter namespace.
        """

    def update(self, namespace, **kwargs):
        """
        :param namespace: update namespace with interpreter namespace
        """

    def push(self, variables, **kwargs):
        """
        :param variables: dict The variables to inject into interpreter namespace
        """

    def get(self, varnames, **kwargs):
        """
        :param variables: list of variable name to get from interpreter namespace
        """

    def delete(self, varnames, **kwargs):
        """
        :param variables: list of variable name to delete in the user's namespace
        """

_interpreter = []

from openalea.core.interpreter import _interpreter_class, adapt_interpreter

import logging

def interpreter():
    """
    :return: a unique instance of advanced interpreter that respect interface IInterpreter
    """

    logger = logging.getLogger("interpreter")

    if _interpreter:
        logger.warning("1")
        return _interpreter[0]
    else:
        try:
            logger.warning("2")
            from IPython.core.getipython import get_ipython
            ip = get_ipython()
            logger.warning("3")
            if ip is None:
                logger.warning("4")
                ip = _interpreter_class()()
            logger.warning("5")
            adapt_interpreter(ip)
            _interpreter.append(ip)
            return _interpreter[0]
        except(ImportError, NameError):
            logger.warning("exception")
            Interpreter = _interpreter_class()
            _interpreter.append(Interpreter())
            return _interpreter[0]

#
# ipython.py ends here
