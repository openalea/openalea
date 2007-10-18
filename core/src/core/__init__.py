from external import *


def global_module(module):
    """ Declare a module accessible everywhere """
    import __builtin__
    __builtin__.__dict__[module.__name__] = module

