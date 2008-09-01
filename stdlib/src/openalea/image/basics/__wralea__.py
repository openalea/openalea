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

__name__ = "openalea.image.basics"
__alias__ = ["image.basics"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'PIL wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []



from openalea.core import Factory
from openalea.core.interface import *
from ...interface import interIImageMode,IPix


load2rgb = Factory( name= "load2rgb", 
              description= "load an image file and convert it to RGBA", 
              category = "Image", 
              nodemodule = "basics",
              nodeclass = "load2rgb",
              inputs=(dict(name="Filename", interface=IFileStr,),),
              outputs=(dict(name="Image", interface=IPix,),),
              )

__all__.append("load2rgb")

load2l = Factory( name= "load2l", 
                  description= "load an image file and convert it to L", 
                  category = "Image", 
                  nodemodule = "basics",
                  nodeclass = "load2l",
                  inputs=(dict(name="Filename", interface=IFileStr,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

__all__.append("load2l")


saveimg = Factory( name= "save image", 
                   description= "save an image file", 
                   category = "Image", 
                   nodemodule = "basics",
                   nodeclass = "save_image",
                   inputs=(dict(name="Image", interface=IPix,),
                           dict(name="Filename", interface=IFileStr,),
                           ),
                   outputs=(dict(name="Image", interface=IPix,),),
                   )


__all__.append("saveimg")

viewimg = Factory( name= "view image", 
                   description= "display an image", 
                   category = "Image", 
                   nodemodule = "basics",
                   nodeclass = "pix_visu",
                   widgetmodule = "images_wralea",
                   widgetclass = "PixVisu",
                   inputs=(dict(name="Image", interface=IPix,),),
                   outputs=(dict(name="Image", interface=IPix,),),
                   )

__all__.append("viewimg")


convmode = Factory( name= "convert mode", 
                    description= "change the color mode of the image", 
                    category = "Image", 
                    nodemodule = "basics",
                    nodeclass = "convert",
                    inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Mode", interface=IImageMode,value="RGB"),
                            ),
                    outputs=(dict(name="Image", interface=IPix,),),
                    )


__all__.append("convmode")
