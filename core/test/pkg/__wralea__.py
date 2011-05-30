


from openalea.core.external import *
from openalea.core.pkgdict import protected


__editable__ = True
__name__ = "pkg_test"
__version__ = '0.0.1'
__license__= "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = '...'
__url__ = 'http://openalea.gforge.inria.fr'

__icon__ = 'icon.png'

__alias__ = ['pkg_alias',]


__all__ = ['file1', 'file2', 'alias1', 'alias2', 'plus', 'float_']


file1 = DataFactory(name="file1.txt", editors={'gvim' : 'gvim %s', 'emacs' :'emacs %s'})
file2 = DataFactory(name="file2.txt", alias=['f', 'g'])

Alias(file1, "aliasf1")


float_ = Factory( name="float",
              nodemodule="nodes",
              nodeclass="Float",
              inputs=(dict(name="Float", interface=IFloat, value=0.0),),
              outputs=(dict(name="Float", interface=IFloat),),
              )

plus = Factory( name="+",
        inputs=(dict(name="a", interface=IInt, value=0),
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="add",
        )



range_ = Factory(name="range",
                 description="Returns an arithmetic progression of integers",
                 category="Python",
                 nodemodule="nodes",
                 nodeclass="pyrange",
                 )

__all__.append('range_')

list_ = Factory( name=protected("list"),
                 description="Python list",
                 category="datatype",
                 nodemodule="nodes",
                 nodeclass="List",

                 inputs=(dict(name="List", interface=ISequence),),
                 outputs=(dict(name="List", interface=ISequence),),
                 )

__all__.append('list_')


map_ = Factory( name="map",
               description="Apply a function on a sequence",
               category="Functional",
               inputs=(dict(name='func', interface=IFunction),
                       dict(name='seq', interface=ISequence)),
               nodemodule="nodes",
               nodeclass="pymap",
               )

__all__.append('map_')
