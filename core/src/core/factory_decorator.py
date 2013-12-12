import sys

def factory(f):
    '''
    Function decorator: if the list __factories__ exists in the module which 
    defines f, then add f to __factories__, else, create the list __factories__ 
    which contains f.
    '''
    f.__factory__ = True
    mod = sys.modules[f.__module__]
    if not hasattr(f, '__factories__'):
        mod.__factories__ = [f]
    else:
        mod.__factories__.append(f)
    return f


class inputs(object):
    '''
    Add inputs.
    '''
    def __init__(self, *args):
        self.args = args
        
    def __call__(self, f):
        f.__inputs__ = self.args
        return f


class outputs(object):
    '''
    Add outputs.
    '''
    def __init__(self, *args):
        self.args = args
        
    def __call__(self, f):
        f.__outputs__ = self.args
        return f



