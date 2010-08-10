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
__revision__ =" $Id$ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure.list"
__alias__ = []

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = []



list_ = Factory( name="list",
              description="Python list",
              category="datatype",
              nodemodule="lists",
              nodeclass="List",

              inputs=(dict(name="list", interface=ISequence),),
              outputs=(dict(name="list", interface=ISequence),),
              )

slice_ = Factory( name="slice",
              category="datatype",
              nodemodule="lists",
              nodeclass="Slice",

              inputs=(dict(name="list", interface="ISequence"),
                      dict(name="start", interface="IInt"),
                      dict(name="end", interface="IInt"),
                      dict(name="stride", interface="IInt")),
              outputs=(dict(name="list", interface="ISequence"),),
              )


__all__ += ['list_', 'slice_']



