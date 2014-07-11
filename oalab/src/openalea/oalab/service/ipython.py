__all__ = ["get_interpreter",]
           
from openalea.oalab.session.session import Session


def get_interpreter():
    session = Session()
    if hasattr(session,"interpreter"):
        return session.interpreter
    else:
        print "Can't find ipython interpreter from OpenAleaLab (Session not loaded)."
        print "Searching ipython..."
        try:
            from IPython.core.getipython import get_ipython
            print "Ipython found!"
            return get_ipython()
        except ImportError:
            print "IPython not installed..."
            return None
        except NameError:
            print "Can't find ipython..."
            return None