"""
See online documentation at 
http://openalea.gforge.inria.fr/doc/sphinx/core/html/contents.html 


"""
__license__ = "Cecill-C"
__revision__ = "$Id: __init__.py 2044 2009-12-21 08:59:16Z chopard $"

from openalea.core.external import *
from script_library import ScriptLibrary

def global_module(module):
    """ Declare a module accessible everywhere"""
    import __builtin__
    __builtin__.__dict__[module.__name__] = module

