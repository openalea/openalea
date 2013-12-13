# -*- coding: utf-8 -*-

"""Module documentation"""

__editable__ = True
__description__ = 'Module desc'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__version__ = '1.0'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


from openalea.core.factory_decorator import factory, inputs, outputs

def f():
    pass

@factory
def f1():
    pass

@factory
@inputs()
def f2():
    pass

@factory
@outputs()
def f3():
    pass

@factory
@outputs()
def f4():
    pass

"""
@factory
def f2(a):
    pass

@factory
def f3(a, b=1):
    pass

@factory
def f4(a, *args):
    pass

@factory
def f5(a, *args, **kwargs):
    pass
@factory
def f6(*args):
    pass

@factory
def f7(**kwargs):
    pass

@factory
def f8():
    return 1

@factory
def f9():
    return (1,1)

"""
"""
@factory
class A(object):
    def f(self,a):
        return a
    @inputs('a:A', b=[])
    def g(self, b=[]):
        self.b = b

"""

"""
###############################################################################
# STUB

# Stages

# 1. import module and found factories

def f(a=1, b=2.3):
    return a+b
f.__factory__ = True

def g(a=1, b=2.3):
    return a+b
g.__outputs__ = ['res:IFloat']

def h(a=1, b=2.3):
    return a+b
h.__inputs__ = ['a','b']

# Add a class factory??

# 2. Write factory decorator
# 2.1 on Python functions, on classes, on __builtin__
# @ factory, @inputs, @outputs

# 3. Build an OpenAlea package from the NodeFactories

# 4. Instantiate : use the __factory__, __inputs__, __outputs__ and signature to instantiate a node
 
"""
