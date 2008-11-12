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


__name__ = "openalea.data structure.array"
#__alias__ = ['catalog.data', 'openalea.data']

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

array_= Factory( name="array",
              description="Python array",
              category="Type",
              nodemodule="arrays",
              nodeclass="PyArray",
              )

__all__.append('array_')




