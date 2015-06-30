# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import types
from IPython.kernel.inprocess.ipkernel import InProcessKernel
from IPython.kernel.zmq.ipkernel import Kernel as ZMQKernel
from IPython.core.error import UsageError


class IPythonInProcessInterpreter(InProcessKernel):

    """
    Interpreter is an IPython kernel adapted for OpenAlea.

    :param gui: GUI to use. Default 'qt4'.
    :param locals: namespace to set to the interpreter. Default 'None'.
    """
    # NOTE: to manually define class used for shell, for example InProcessInteractiveShell, just set shell_class attr
    # shell_class = InProcessInteractiveShell

    def __init__(self, gui="qt4", locals=None):
        super(IPythonInProcessInterpreter, self).__init__(gui=gui)
        self.user_ns = self.shell.user_ns
        self.shell.showtraceback = types.MethodType(showtraceback, self.shell)

    def run_cell(self, *args, **kwargs):
        return self.shell.run_cell(*args, **kwargs)

    def run_code(self, code_obj):
        return self.shell.runcode(code_obj)

    def reset(self, namespace=None, **kwargs):
        self.shell.user_ns.clear()
        self.shell.init_user_ns()
        if namespace:
            self.shell.user_ns.update(namespace)

    def update(self, namespace, **kwargs):
        namespace.update(self.user_ns)

    def push(self, variables, **kwargs):
        self.user_ns.update(variables)

    def get(self, varnames, **kwargs):
        dic = {}
        for name in varnames:
            dic[name] = self.user_ns[name]
        return dic

    def delete(self, varnames, **kwargs):
        for name in varnames:
            del self.user_ns[name]


def showtraceback(self, exc_tuple=None, filename=None, tb_offset=None,
                  exception_only=False):
    """Display the exception that just occurred.

    If nothing is known about the exception, this is the method which
    should be used throughout the code for presenting user tracebacks,
    rather than directly invoking the InteractiveTB object.

    A specific showsyntaxerror() also exists, but this method can take
    care of calling it if needed, so unless you are explicitly catching a
    SyntaxError exception, don't try to analyze the stack manually and
    simply call this method."""
    try:
        try:
            import traceback
            etype, value, tb = self._get_exc_info(exc_tuple)
            # hack by Julien Coste to display errors
            traceback.print_exception(etype, value, tb)
        except ValueError:
            self.write_err('No traceback available to show.\n')
            return

        if issubclass(etype, SyntaxError):
            # Though this won't be called by syntax errors in the input
            # line, there may be SyntaxError cases with imported code.
            self.showsyntaxerror(filename)
        elif etype is UsageError:
            self.show_usage_error(value)
        else:
            if exception_only:
                stb = ['An exception has occurred, use %tb to see '
                       'the full traceback.\n']
                stb.extend(self.InteractiveTB.get_exception_only(etype,
                                                                 value))
            else:
                try:
                    # Exception classes can customise their traceback - we
                    # use this in IPython.parallel for exceptions occurring
                    # in the engines. This should return a list of strings.
                    stb = value._render_traceback_()
                except Exception:
                    stb = self.InteractiveTB.structured_traceback(etype,
                                                                  value, tb, tb_offset=tb_offset)

                self._showtraceback(etype, value, stb)
                if self.call_pdb:
                    # drop into debugger
                    self.debugger(force=True)
                return

            # Actually show the traceback
            self._showtraceback(etype, value, stb)

    except KeyboardInterrupt:
        self.write_err("\nKeyboardInterrupt\n")


Interpreter = IPythonInProcessInterpreter
