# -*- python -*-
#
#       spatial_image: spatial nd images
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
nodes definition for spatial_image package
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *

__name__ = "spatial_image"
__alias__ = []
__version__ = '0.0.2'
__license__ = "Cecill-C"
__authors__ = 'Jerome Chopard'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'SpatialImage Node library.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = "icon.png"

__all__ = []

#########################################
#
#	serial
#
#########################################
read = Factory( name= "read inr", 
				description= "",
				category = "",
				nodemodule = "serial",
				nodeclass = "read",
				inputs=(dict(name="filename", interface=IFileStr,),),
				outputs=(dict(name="img", interface=None,),),
			)

__all__.append('read')

write = Factory( name= "write inr", 
				description= "",
				category = "",
				nodemodule = "serial",
				nodeclass = "write",
				inputs=(dict(name="img", interface=None,),
				        dict(name="filename", interface=IFileStr,),),
				outputs=(dict(name="img", interface=None,),),
			)

__all__.append('write')

#########################################
#
#	attributes
#
#########################################
info = Factory( name= "info", 
				description= "",
				category = "",
				nodemodule = "image",
				nodeclass = "info",
				inputs=(dict(name="img", interface=None,),),
				outputs=(),
			)

__all__.append('info')


