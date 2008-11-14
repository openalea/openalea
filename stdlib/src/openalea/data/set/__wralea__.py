# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """ OpenAlea dictionary data structure"""
__license__ = "Cecill-C"
__revision__ =" $Id: __wralea__.py 1362 2008-09-01 12:41:47Z dufourko $ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure.set"
#__alias__ = ['catalog.data', 'openalea.data']

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

set_= Factory( name="set",
              description="Python set",
              category="Type",
              nodemodule="sets",
              nodeclass="py_set",
              inputs=(dict(name="sequence", interface=ISequence,),), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('set_')

clear_= Factory( name="clear",
              description="Remove all elements from a set.",
              category="Type",
              nodemodule="sets",
              nodeclass="py_clear",
              inputs=(dict(name="set", interface=ISequence,),), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('clear_')

add_= Factory( name="add",
              description="Add an element to a set.",
              category="Type",
              nodemodule="sets",
              nodeclass="py_add",
              inputs=(dict(name="set", interface=ISequence),dict(name="obj")), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('add_')

diff_= Factory( name="difference",
              description=" Return the difference of two sets as a new sets.",
              category="Type",
              nodemodule="sets",
              nodeclass="py_difference",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('diff_')

intersect_= Factory( name="intersection",
              description=" Return the intersection of two sets as a new sets.",
              category="Type",
              nodemodule="sets",
              nodeclass="py_intersection",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('intersect_')

issubset_= Factory( name="issubset",
              description=" Report whether another set contains this set. ",
              category="Type",
              nodemodule="sets",
              nodeclass="py_issubset",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('issubset_')

issuperset_= Factory( name="issuperset",
              description=" Report whether a set contains another set. ",
              category="Type",
              nodemodule="sets",
              nodeclass="py_issuperset",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('issuperset_')

sym_= Factory( name="symmetric_difference",
              description="Return the symmetric difference of two sets as a new set. ",
              category="Type",
              nodemodule="sets",
              nodeclass="py_symmetric_difference",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('sym_')

union_= Factory( name="union",
              description="Return the union of two sets as a new set.",
              category="Type",
              nodemodule="sets",
              nodeclass="py_union",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('union_')

update_= Factory( name="update",
              description="Update a set with the union of set1 and set2..",
              category="Type",
              nodemodule="sets",
              nodeclass="py_update",
              inputs=(dict(name="set1", interface=ISequence),dict(name="set2", interface=ISequence)), 
              outputs=(dict(name="set", interface = ISequence),),
              )

__all__.append('update_')

