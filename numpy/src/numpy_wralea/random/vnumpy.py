from openalea.core import Node, IInt
from openalea.core.external import add_docstring



class randn(Node):

    
    from numpy.random import randn
    @add_docstring(randn)
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='n', interface=IInt, value=1)
        self.add_output(name='array')

    def __call__(self, inputs):
        from numpy.random import randn
        return randn(self.get_input('n'))


