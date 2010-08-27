from openalea.core import Node, IInt
from openalea.core.external import add_docstring
from numpy.random import randn, standard_normal

def wra_randn(n):
    return (randn(n),)

wra_randn.__doc__ = randn.__doc__

def wra_standard_normal(size):
    return (standard_normal(size),)

wra_standard_normal.__doc__ = standard_normal.__doc__



def wra_standard_normal(size):
    return (standard_normal(size),)

wra_standard_normal.__doc__ = standard_normal.__doc__



