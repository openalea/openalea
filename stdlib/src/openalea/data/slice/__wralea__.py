# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
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
__revision__ =" $Id:  $ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure.slice"
__alias__ = []

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

slice_ = Factory( name="slice",
              description="Python slice",
              category="datatype",
              nodemodule="slices",
              nodeclass="Slice",
              inputs=(dict(name="start", interface=IInt, value=0),
                      dict(name="stop", interface=IInt, value=None),
                      dict(name="step", interface=IInt, value=None),),
              outputs=(dict(name="slice", interface = ISlice),),
              )

__all__.append('slice_')

