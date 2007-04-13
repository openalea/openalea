# Core tests


from openalea.core.signature import get_parameters
from openalea.core.interface import *

def test_function():

    # no parameter
    def func_no_param():
        pass

    ret = get_parameters(func_no_param)
    assert ret == []

    # parameter
    def func_param(x, y):
        return z

    ret = get_parameters(func_param)
    assert ret == [{'interface': None, 'name': 'x', 'value': None},
                   {'interface': None, 'name': 'y', 'value': None}]

    # partial default
    def func_param_def1(w, x, y=0, z=0):
        pass

    ret = get_parameters(func_param_def1)
    assert ret == [{'interface': None, 'name': 'w', 'value': None},
                   {'interface': None, 'name': 'x', 'value': None},
                   {'interface': IInt, 'name': 'y', 'value': 0},
                   {'interface': IInt, 'name': 'z', 'value': 0}]


    # all default
    def func_param_def2(w=[], x=None, y=0, z=0., a={}):
        pass

    ret =  get_parameters(func_param_def2)
    assert ret == [{'interface': ISequence, 'name': 'w', 'value': []},
                   {'interface': None, 'name': 'x', 'value': None},
                   {'interface': IInt, 'name': 'y', 'value': 0},
                   {'interface': IFloat, 'name': 'z', 'value': 0.},
                   {'interface': IDict, 'name': 'a', 'value': {}}]


def test_functor():

    class functor1(object):

        def __call__(self, x, y=0):
            return


    ret = get_parameters(functor1())
    assert ret == [{'interface': None, 'name': 'x', 'value': None},
                   {'interface': IInt, 'name': 'y', 'value': 0}]


    class functor2:

        def __call__(self):
            return

    ret = get_parameters(functor2())
    assert ret == []

    class nofunctor1(object):
        pass

    assert get_parameters(nofunctor1()) == ()

    
    class nofunctor2(object):
        pass

    assert get_parameters(nofunctor2()) == ()
