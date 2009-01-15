from openalea.core.alea import run
from openalea.core.pkgmanager import PackageManager
from random import random, randint

""" A unique PackageManager is created for all test of dataflow """
pm = PackageManager()
pm.init(verbose=False)


def test_ifelse():
    """ Test of node ifelse """
    res = run(('openalea.python method', 'ifelse'),\
        inputs={'c': True, 'a': 'a', 'b': 'b'}, pm=pm)
    assert res[0] == 'a'
    res = run(('openalea.python method', 'ifelse'),\
        inputs={'c': False, 'a': 'a', 'b': 'b'}, pm=pm)
    assert res[0] == 'b'


def test_getitem():
    """ Test of node getitem """
    res = run(('openalea.python method', 'getitem'),\
        inputs={'obj': {'a': 1, 'b': 2}, 'key': 'a'}, pm=pm)
    assert res[0] == 1
    res = run(('openalea.python method', 'getitem'),\
        inputs={'obj': range(10), 'key': 2}, pm=pm)
    assert res[0] == 2


def test_setitem():
    """ Test of node setitem """
    res = run(('openalea.python method', 'setitem'),
        inputs={'obj': {'a': 1, 'b': 2}, 'key': 'c', 'value': 3}, pm=pm)
    assert len(res[0]) == 3
    res = run(('openalea.python method', 'setitem'),
        inputs={'obj': range(10), 'key': 2, 'value': 3}, pm=pm)
    assert len(res[0]) == 10
    assert res[0][2] == 3


def test_delitem():
    """ Test of node delitem """
    res = run(('openalea.python method', 'delitem'),
        inputs={'obj': {'a': 1, 'b': 2}, 'key': 'a'}, pm=pm)
    assert len(res[0]) == 1
    res = run(('openalea.python method', 'delitem'),
        inputs={'obj': range(10), 'key': 2}, pm=pm)
    assert len(res[0]) == 9


def test_len():
    """ Test of node len """
    res = run(('openalea.python method', 'len'),
        inputs={'obj': {'a': 1, 'b': 2}}, pm=pm)
    assert res[0] == 2
    res = run(('openalea.python method', 'len'),
        inputs={'obj': range(10)}, pm=pm)
    assert res[0] == 10


def test_keys():
    """ Test of node keys """
    res = run(('openalea.python method', 'keys'),
        inputs={'obj': {'a': 1, 'b': 2}}, pm=pm)
    assert res[0] == ['a', 'b']


def test_values():
    """ Test of node values """
    res = run(('openalea.python method', 'values'),
        inputs={'obj': {'a': 1, 'b': 2}}, pm=pm)
    assert res[0] == [1, 2]


def test_items():
    """ Test of node items """
    res = run(('openalea.python method', 'items'),
        inputs={'obj': {'a': 1, 'b': 2}}, pm=pm)
    assert res[0] == [('a', 1), ('b', 2)]


def test_range():
    """ Test of node range """
    res = run(('openalea.python method', 'range'),
        inputs={'start': 0, 'stop': 10, 'step': 2}, pm=pm)
    assert res[0] == range(0, 10, 2)


def test_enumerate():
    """ Test of node enumerate """
    res = run(('openalea.python method', 'enumerate'),
        inputs={'obj': range(2, 10)}, pm=pm)
    assert res[0] == [(i-2, i) for i in range(2, 10)]


def test_print():
    """ Test of node print """
    val = 'test'
    res = run(('openalea.python method', 'print'),
        inputs={'x': val}, pm=pm)
    assert res[0] == val


def test_method():
    """ Test of node method """

    class Dummy:

        def __init__(self):
            self.tvalue = False

        def test(self, value=True):
            self.tvalue = value
    val = Dummy()
    res = run(('openalea.python method', 'method'),
        inputs={'obj': val, 'member_name': 'test'}, pm=pm)
    assert res[0] == val
    assert val.tvalue == True
    val.tvalue = False
    res = run(('openalea.python method', 'method'),
        inputs={'obj': val, 'member_name': 'test', 'args': (True, )}, pm=pm)
    assert res[0] == val
    assert val.tvalue == True


def test_getattr():
    """ Test of node getattr """

    class Dummy:

        def __init__(self):
            self.tvalue = False
    val = Dummy()
    res = run(('openalea.python method', 'getattr'),
        inputs={'obj': val, 'member_name': 'tvalue'}, pm=pm)
    assert res[0] == val.tvalue


def test_eval():
    """ Test of node eval """
    val = 'True'
    res = run(('openalea.python method', 'eval'),
        inputs={'expression': val}, pm=pm)
    assert res[0] == True


def test_zip():
    """ Test of node zip """
    res = run(('openalea.python method', 'zip'),
        inputs={'s1': range(10), 's2': range(10)}, pm=pm)
    assert res[0] == [(i, i) for i in range(10)]


def test_flatten():
    """ Test of node flatten """
    res = run(('openalea.python method', 'flatten'),
        inputs={'obj': [(3*i, 3*i+1, 3*i+2) for i in range(5)]}, pm=pm)
    assert len(res[0]) == 15
    assert res[0] == range(15)


def test_sum():
    """ Test of node sum """
    res = run(('openalea.python method', 'sum'),
        inputs={'sequence': [i for i in range(5)]}, pm=pm)
    assert res[0] == sum(range(5))


def test_mean():
    """ Test of node mean """
    res = run(('openalea.python method', 'mean'),
        inputs={'sequence': [i for i in range(5)]}, pm=pm)
    assert res[0] == sum(range(5))/5.
