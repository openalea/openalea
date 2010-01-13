"""Node tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.node import *


def test_funcnode():
    """ Test Node creation"""
    inputs = (dict(name='x', interface=None, value=None), )
    outputs = (dict(name='y', interface=None), )

    def func(*input_values):
        return (input_values, )

    n = FuncNode(inputs, outputs, func)

    n.add_input(name='a', inteface=None, value=0)
    assert n.get_nb_input() == 2
    assert n.get_nb_output() == 1

    # Test IO and acess by key or index
    n.set_input(0, 1)
    n.eval()
    print n.get_output('y')
    assert n.get_output('y') == (1, 0)

    n.set_input('a', 'BB')
    n.eval()
    assert n.get_output(0) == (1, 'BB')


class MyNode(Node):

    def __call__(self, inputs):
        return sum(inputs)


def MyFunc(a, b):
    return a + b


def test_node():
    """ Test Node creation"""
    inputs = (dict(name='x', interface=None, value=None), )
    outputs = (dict(name='y', interface=None), )

    def func():
        raise RuntimeError()

    n = Node(inputs, outputs)

    try:
        n()
        assert False
    except NotImplementedError:
        assert True

    n = MyNode(inputs, outputs)

    assert n.get_nb_input() == 1
    assert n.get_nb_output() == 1

    # Test IO and acess by key or index
    n.set_input(0, 1)
    n.eval()
    assert n.get_output('y') == 1


def test_factory():
    """test factory"""
    f1 = Factory(name = "MyFactory",
                 nodemodule = "test_node",
                 nodeclass = "MyNode",
                 )

    n = f1.instantiate()
    print n.get_nb_input()
    assert n.get_nb_input() == 0

    f2 = Factory(name = "MyFactory2",
                  nodemodule = "test_node",
                  nodeclass = "MyFunc",
                 )

    n = f2.instantiate()
    assert n.get_nb_input() == 2

    f1IO = Factory(name = "MyFactory",
                    nodemodule = "test_node",
                    nodeclass = "MyNode",
                    inputs = (dict(name="x", interface=None),
                              dict(name="y", interface=None),
                              dict(name="z", interface=None)),
                    outputs = (dict(name="a", interface=None), ), )

    n = f1IO.instantiate()
    assert n.get_nb_input() == 3

    f2IO = Factory(name = "MyFactory2",
                    nodemodule = "test_node",
                    nodeclass = "MyFunc",
                    inputs = (dict(name="x", interface=None), \
                        dict(name="y", interface=None)),
                    outputs = (dict(name="z", interface=None), ), )

    n = f2IO.instantiate()
    assert n.get_nb_input() == 2


def test_factory_name():
    """ test the factory python name """

    names = [
        'aaaa',
        '234AB3',
        'azert er',
        'AZ_12',
        '::qsd,;']

    for n in names:
        f = Factory(name = n)
        python_name = f.get_python_name()
        exec("%s = 0"%(python_name))



# BUG #4877


def test_node_output():

    # Test Node creation
    inputs = (dict(name='x', interface=None, value=None), )
    outputs = (dict(name='y', interface=None), )

    def func1(*inputs):
        return 1

    def func2(*inputs):
        return [1, 2]

    n1 = FuncNode(inputs, outputs, func1)
    n2 = FuncNode(inputs, outputs, func2)

    assert n1.get_nb_input() == 1
    assert n1.get_nb_output() == 1
    assert n2.get_nb_input() == 1
    assert n2.get_nb_output() == 1

    # Test IO and acess by key or index
    n1.eval()
    n2.eval()
    assert n1.get_output('y') == 1
    assert n2.get_output('y') == [1, 2]
