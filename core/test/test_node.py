# Test node module



from openalea.core.node import *


def test_node():

    # Test Node creation
    inputs = ( dict(name='x', interface=None, value=None),)
    outputs = ( dict(name='y', interface=None),)
    def func():
        raise RuntimeError()
    
    n = Node( inputs, outputs, func)

    try:
        n()
        assert False
    except RuntimeError:
        assert True


    n.add_input( 'a', None , 0)
    assert n.get_nb_input() == 2
    assert n.get_nb_output() == 1


    # Test IO and acess by key or index
    n.set_input(0, 1)
    assert n.get_input('x') == 1

    n.set_input('a', 'BB')
    assert n.get_input(1) == 'BB'

    
    n.set_output(0, "A")
    assert n.get_output('y') == "A"



def test_factory():

    # Test Factory Creation

    # See Test Wralea
    pass
