# Test node module



from openalea.core.node import *


def test_funcnode():

    # Test Node creation
    inputs = ( dict(name='x', interface=None, value=None),)
    outputs = ( dict(name='y', interface=None),)
    def func():
        raise RuntimeError()
    
    n = FuncNode( inputs, outputs, func)

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



class MyNode(Node):

    def __call__(self, inputs):
        return sum(inputs)

def MyFunc(a, b):
    return a + b

def test_node():

    # Test Node creation
    inputs = ( dict(name='x', interface=None, value=None),)
    outputs = ( dict(name='y', interface=None),)
    def func():
        raise RuntimeError()
    
    n = Node( inputs, outputs)

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
    assert n.get_input('x') == 1

    n.eval()
    assert n.get_output('y') == 1


def test_factory():

    f1 = Factory( name = "MyFactory",

                 nodemodule = "test_node",
                 nodeclass = "MyNode",
                 
                 )
                
    n = f1.instantiate()
    assert n.get_nb_input() == 0
    
    f2 = Factory( name = "MyFactory2",

                  nodemodule = "test_node",
                  nodeclass = "MyFunc",
                 )

    n = f2.instantiate()
    assert n.get_nb_input() == 2
    

    f1IO = Factory( name = "MyFactory",

                    nodemodule = "test_node",
                    nodeclass = "MyNode",
                    
                    inputs = (dict(name="x", interface=None),
                              dict(name="y", interface=None),
                              dict(name="z", interface=None)),
                    outputs = (dict(name="a", interface=None),),
                 
                 )

    n = f1IO.instantiate()
    assert n.get_nb_input() == 3
                

    f2IO = Factory( name = "MyFactory2",

                    nodemodule = "test_node",
                    nodeclass = "MyFunc",
                    
                    inputs = (dict(name="x", interface=None), dict(name="y", interface=None)),
                    outputs = (dict(name="z", interface=None),),
                 )

    n = f2IO.instantiate()
    assert n.get_nb_input() == 2



