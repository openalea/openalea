# -*- python -*-
#
#       OpenAlea.Image
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Node declaration for image
"""

__license__ = "Cecill-C"
__revision__ = " $Id:  $ "

from openalea.core import Factory, Alias
from openalea.core.interface import *

__name__ = "openalea.image.registration"

__all__ = []

points2transfo = Factory( name= "pts2transfo", 
			     description= "Infer rigid transformation from control point pairs",
			     category = "image",
			     nodemodule = "registration",
			     nodeclass = "pts2transfo",
                             inputs=(dict(name="points1", interface=ISequence),
			             dict(name="points2", interface=ISequence),),
			     outputs=(dict(name="rigid transformation", interface=None),),
			    )

__all__.append('points2transfo')

Alias(points2transfo, 'pts2transfo')

angles2transfo = Factory( name= "angles2transfo", 
			     description= "Compute transformation matrix between 2 images from the angles in each directions",
			     category = "image",
			     nodemodule = "registration",
			     nodeclass = "angles2transfo",
                             inputs=(dict(name="image1", interface=None),
                                     dict(name="image2", interface=None),
                                     dict(name="angle X", interface=IInt, value=0),
			             dict(name="angle Y", interface=IInt, value=0),
			             dict(name="angle Z", interface=IInt, value=0),),
			     outputs=(dict(name="transformation matrix", interface=None),),
			    )

__all__.append('angles2transfo')
