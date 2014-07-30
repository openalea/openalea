__all__ = ["get_interpreter",]
           
from openalea.oalab.session.session import Session
from openalea.vpltk.shell.shell import get_interpreter_class

__interpreter = []


def get_interpreter():
    if len(__interpreter):
        return __interpreter[0]

    else:
        if Session.instanciated:
            __interpreter.append(Session().interpreter)
        else:
            try:
                from IPython.core.getipython import get_ipython
                interpreter = get_ipython()
                if interpreter:
                    __interpreter.append(get_ipython())
            except:
                pass
            if not len(__interpreter):
                interpreter = get_interpreter_class()()
                if interpreter:
                    __interpreter.append(interpreter)

    if len(__interpreter):
        return get_interpreter()
