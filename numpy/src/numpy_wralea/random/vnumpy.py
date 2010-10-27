from openalea.core import Node, IInt
from openalea.core.external import add_docstring
from numpy.random import rand, randn, random, standard_normal, uniform

def wra_rand(d):
    return (rand(d),)
wra_rand.__doc__ = rand.__doc__

def wra_randn(n):
    return (randn(n),)
wra_randn.__doc__ = randn.__doc__

def wra_random(size):
    return (random(size),)
wra_random.__doc__ = random.__doc__

def wra_standard_normal(size):
    return (standard_normal(size),)
wra_standard_normal.__doc__ = standard_normal.__doc__

def wra_standard_normal(size):
    return (standard_normal(size),)
wra_standard_normal.__doc__ = standard_normal.__doc__

def wra_uniform(low, high, size):
    return (uniform(low, high, size),)
wra_uniform.__doc__ = uniform.__doc__

