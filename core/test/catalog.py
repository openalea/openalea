from openalea.core import *
from operator import add


plus = NodeFactory('plus', nodemodule='operator', nodeclass='add',
                        inputs=(dict(name='a',interface=None,value=0.),dict(name='b',interface=None,value=0.),), 
                        outputs=(dict(name='out'),))
my_float = NodeFactory('float', nodemodule='', nodeclass='float', 
                        inputs=(dict(name='in',interface=None,value=0.),), 
                        outputs=(dict(name='out'),))
my_int = NodeFactory('int', nodemodule='', nodeclass='int', 
                        inputs=(dict(name='in',interface=None,value=0),), 
                        outputs=(dict(name='out'),))
my_string = NodeFactory('string', nodemodule='', nodeclass='str', 
                        inputs=(dict(name='in',interface=None,value=''),), 
                        outputs=(dict(name='out'),))

pkg = Package('core catalog',metainfo={})
pkg.add_factory(plus)
pkg.add_factory(my_float)
pkg.add_factory(my_int)
pkg.add_factory(my_string)

