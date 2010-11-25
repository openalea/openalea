# -*- python -*-
# -*- coding: latin-1 -*-
#
#       Sorting and searching : numpy package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################


__doc__ = """ openalea.numpy """
__revision__ = " $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *


__name__ = "openalea.numpy.sorting_searching"
__version__ = '0.99'
__license__ = 'CECILL-C'
__authors__ = 'Eric Moscardi, eric.moscardi@sophia.inria.fr'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping (Sorting and searching functions).'
__url__ = 'http://openalea.gforge.inria.fr'
#__icon__ = 'icon.png'

__all__ = []

searchsorted = Factory(name= "searchsorted",
               description= "Find indices where elements should be inserted to maintain order",
               category = "numpy",
               inputs = (  dict(name='a', interface=None),
                           dict(name='v', interface=ISequence),
                           dict(name='side', interface=IEnumStr(['left', 'right']),value='left'),),
               outputs = ( dict(name='indices', interface=None),),
               nodemodule = "numpy",
               nodeclass = "searchsorted",
            )

__all__.append("searchsorted")

where = Factory(name= "where",
               description= "Return elements, either from x or y, depending on condition.",
               category = "numpy",
               inputs = (  dict(name='condition', interface=None),
                           dict(name='x', interface=None),
                           dict(name='y', interface=None),),
               outputs = ( dict(name='out', interface=None),),
               nodemodule = "sorting_searching",
               nodeclass = "wra_where",
            )

__all__.append("where")
