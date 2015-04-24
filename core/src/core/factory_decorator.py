"""
Decorators to attach signature information to functions
"""

import sys


def factory(f):
    '''
    Flag the given function `f` as an openalea factory.
    '''
    f.__factory__ = True
    mod = sys.modules[f.__module__]
    if not hasattr(mod, '__factories__'):
        mod.__factories__ = [f]
    else:
        mod.__factories__.append(f)
    return f


class inputs(object):

    '''
    Add inputs information to a function

    Example:
       >>> from openalea.core.factory_decorator import inputs
       >>> @inputs('a:int=1,b:list=[]')
       ... def fct(*args):
       ...     pass
    '''

    def __init__(self, *args):
        self.args = args

    def __call__(self, f):
        f.__inputs__ = self.args
        return f


class outputs(inputs):

    '''
    Add outputs information to a function

    Example:
       >>> from openalea.core.factory_decorator import outputs
       >>> @outputs('first:int,remainder:list')
       ... def fct(*args):
       ...     return int(args[0]), args[1:]
    '''

    def __call__(self, f):
        f.__outputs__ = self.args
        return f
