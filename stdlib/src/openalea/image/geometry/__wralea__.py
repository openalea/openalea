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


__doc__ = """ openalea.image """
__revision__ = " $Id: __wralea__.py 1344 2008-08-01 13:05:28Z dufourko $ "


from openalea.core import *

__name__ = "openalea.image.geometry"
__alias__ = ["image.geometry"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'PIL wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = ["mirror", "crop", "resize", "rotate"]

from openalea.core import Factory
from openalea.core.interface import *
from ...interface import IPix
from openalea.core.traitsui import View, Group, Item


crop = Factory( name= "crop image", 
              description= "crop an image", 
              category = "Image", 
              nodemodule = "geom_transfo",
                  nodeclass = "crop",
              inputs=(dict(name="Image", interface=IPix,),
                      dict(name="Xmin", interface=IInt(min=0),),
                      dict(name="Xmax", interface=IInt(min=0),),
                      dict(name="Ymin", interface=IInt(min=0),),
                      dict(name="Ymax", interface=IInt(min=0),),
                      ),
              outputs=(dict(name="Image", interface=IPix,),),
                  )


resize = Factory( name="resize image",
                  description="resize an image",
                  category="Image",
                  nodemodule="geom_transfo",
                  nodeclass="resize",
                  view=View(
        Group(
            "Tabu",
            Group(
                "Size",
                Item("Width"),
                Item("Height"),
                layout='t',
                ),
            Group(
                "Test",
                Item("Mode"),
                ),
            layout='t',
            ),
        Group(
            "Size",
            Item("Width"),
            Item("Height"),
            layout='-',
            ),
        Group(
            "Test",
            Item("Mode"),
            ),
        layout="t",
        ),
                  )


rotate = Factory( name="rotate image",
                  description="rotate an image",
                  category="Image",
                  nodemodule="geom_transfo",
                  nodeclass="rotate",
                  )


mirror = Factory( name= "mirror", 
                  description= "flip an image", 
                  category = "Image", 
                  nodemodule = "geom_transfo",
                  nodeclass = "mirror",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Horizontal", interface=IBool, value=True),
                          ),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

