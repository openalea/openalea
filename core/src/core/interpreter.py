
from IPython.kernel.inprocess.ipkernel import InProcessKernel
from IPython.core.error import UsageError
import types

class Interpreter(InProcessKernel):
    """
    Interpreter is an IPython kernel adapted for OpenAlea.

    :param gui: GUI to use. Default 'qt4'.
    :param locals: namespace to set to the interpreter. Default 'None'.
    """

    def __init__(self, gui="qt4", locals=None):
        super(Interpreter, self).__init__(gui=gui)
        # cf. get_ipython for ipython singleton problem
        self.locals = self.shell.user_ns

        if locals is not None:
            for l in locals:
                self.locals += l
        self.shell.locals = self.locals
        self.user_ns = self.shell.user_ns
        self.shell.showtraceback = types.MethodType(showtraceback, self.shell)

    def run_cell(self, *args, **kwargs):
        return self.shell.run_cell(*args, **kwargs)

    def runcode(self, source=None):
        """
        TODO
        """
        return self.shell.runcode(source)

    def runsource(self, source=None, filename="<input>", symbol="single"):
        """
        TODO
        """
        try:
            return self.runcode(source)
        except:
            code = compile(source, filename, symbol)
            if code is not None:
                return self.runcode(code)

    def loadcode(self, source=None, namespace=None):
        """
        Load 'source' and use 'namespace' if it is in parameter.
        Else use locals.

        :param source: text (string) to load
        :param namespace: dict to use to execute the source
        """
        # Not multiligne
        if namespace is not None:
            exec(source, namespace)
        else:
            exec(source, self.locals, self.locals)


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


def main():
    from shell import main as main_
    main_()


if(__name__ == "__main__"):
    main()
