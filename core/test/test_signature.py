__license__ = "Cecill-C"
__revision__ = " $Id$ "

import openalea.core.signature as sgn
from openalea.core.interface import *


def test_function():
    """Test function"""

    # no parameter

    def func_no_param():
        pass

    s = sgn.Signature(func_no_param)
    assert s.get_name() == 'func_no_param'
    assert s.get_parameters() == []

    # parameter

    def func_param(x, y):
        return z

    s = sgn.Signature(func_param)
    assert s.get_name() == 'func_param'
    assert s.get_parameters() == \
        [{'interface': None, 'name': 'x', 'value': None},
         {'interface': None, 'name': 'y', 'value': None}]

    # partial default

    def func_param_def1(w, x, y=0, z=0):
        pass

    s = sgn.Signature(func_param_def1)
    assert s.get_name() == 'func_param_def1'
    assert s.get_parameters() == \
        [{'interface': None, 'name': 'w', 'value': None},
                   {'interface': None, 'name': 'x', 'value': None},
                   {'interface': IInt, 'name': 'y', 'value': 0},
                   {'interface': IInt, 'name': 'z', 'value': 0}]


    # all default

    def func_param_def2(w=[], x=None, y=0, z=0., a={}):
        pass

    s = sgn.Signature(func_param_def2)
    assert s.get_name() == 'func_param_def2'
    assert s.get_parameters() == \
        [{'interface': ISequence, 'name': 'w', 'value': []},
        {'interface': None, 'name': 'x', 'value': None},
        {'interface': IInt, 'name': 'y', 'value': 0},
        {'interface': IFloat, 'name': 'z', 'value': 0.},
        {'interface': IDict, 'name': 'a', 'value': {}}]


def test_instanceMethod():

    class classTest:

        def __init__(self):
            pass

        def func_no_param(self):
            pass

        def func_param(self, x, y):
            return z

        def func_param_def1(self, w, x, y=0, z=0):
            pass

        def func_param_def2(self, w=[], x=None, y=0, z=0., a={}):
            pass

    ct = classTest()

    s = sgn.Signature(ct.func_no_param)
    assert s.get_name() == 'func_no_param'
    assert s.get_parameters() == []

    s = sgn.Signature(ct.func_param)
    assert s.get_name() == 'func_param'
    assert s.get_parameters() == \
        [{'interface': None, 'name': 'x', 'value': None},
        {'interface': None, 'name': 'y', 'value': None}]

    s = sgn.Signature(ct.func_param_def1)
    assert s.get_name() == 'func_param_def1'
    assert s.get_parameters() == \
        [{'interface': None, 'name': 'w', 'value': None},
        {'interface': None, 'name': 'x', 'value': None},
        {'interface': IInt, 'name': 'y', 'value': 0},
        {'interface': IInt, 'name': 'z', 'value': 0}]

    s = sgn.Signature(ct.func_param_def2)
    assert s.get_name() == 'func_param_def2'
    assert s.get_parameters() == \
        [{'interface': ISequence, 'name': 'w', 'value': []},
        {'interface': None, 'name': 'x', 'value': None},
        {'interface': IInt, 'name': 'y', 'value': 0},
        {'interface': IFloat, 'name': 'z', 'value': 0.},
        {'interface': IDict, 'name': 'a', 'value': {}}]


def test_functor():

    class functor1(object):

        def __call__(self, x, y=0):
            return


    s = sgn.Signature(functor1)
    assert s.get_name() == 'functor1'
    assert s.get_parameters() == \
        [{'interface': None, 'name': 'x', 'value': None},
        {'interface': IInt, 'name': 'y', 'value': 0}]

    class functor2:

        def __call__(self):
            return

    s = sgn.Signature(functor2)
    assert s.get_name() == 'functor2'
    assert s.get_parameters() == []

    class nofunctor(object):
        pass

    s = sgn.Signature(nofunctor)
    assert s.get_name() == 'nofunctor'
    assert s.get_parameters() == []
    assert s.isValid == False
