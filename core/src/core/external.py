"""This module defines all the import used in wralea declarations"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core.package import Package, UserPackage
from openalea.core.node import Factory, Node, NodeFactory, Alias
from openalea.core.data import DataFactory, PackageData
from openalea.core.compositenode import CompositeNode, CompositeNodeFactory
from openalea.core.interface import *



def add_docstring(obj):
    """Decorator that replace a function's docstring by another from `obj`

    This function should be used to decorate your wralea functions when docstring
    is equivalent to an already existing function or class.

    :param obj: a function or class that contains a docstring

    :Example:

    ::

        from math import abs

        @add_docstring(abs)
        def int_abs_function(x):
            if type(x) == int:
                return abs(x)
            else:
                raise TypeError("expect int as parameter")


    """
    def wrap(f):
        f.__doc__ = obj.__doc__
        return f
    return wrap

