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

@factory
def f1():
    pass

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


