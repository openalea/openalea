import sys

__factories__ = []

def factory(f):
    '''
    Fonction decorator: if the list __factories__ exists in the module which 
    defines f, then add f to __factories__, else, create the list __factories__ 
    which contains f.
    '''
    mod = sys.modules[f.__module__]
    if not hasattr(f, '__factories__'):
        mod.__factories__ = [f]
    else:
        mod.__factories__.append(f)
    return f