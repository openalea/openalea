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
__revision__ = " $Id: __wralea__.py 2585 2010-07-02 15:28:03Z chopard $ "

from openalea.core import *
from openalea.color import IColor,IColorWidget
from openalea.image_wralea import IImage,IImageWidget

__name__ = "openalea.image.algo"

__all__ = []

crop = Factory(name = "crop",
                description = "crop an image",
                category = "image",
                nodemodule = "algo",
                nodeclass = "crop",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "x", interface = IInt, value = 0),
                          dict(name = "y", interface = IInt, value = 0),
                          dict(name = "dx", interface = IInt, value = 0),
                          dict(name = "dy", interface = IInt, value = 0),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("crop")

paste = Factory(name = "paste",
                description = "paste an image into another",
                category = "image",
                nodemodule = "algo",
                nodeclass = "paste",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "im2", interface = IImage),
                          dict(name = "x", interface = IInt, value = 0),
                          dict(name = "y", interface = IInt, value = 0),
                          dict(name = "reshape", interface = IBool, value = False),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("paste")

rotate = Factory(name = "rotate",
                description = "rotate an image",
                category = "image",
                nodemodule = "algo",
                nodeclass = "wra_rotate",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "angle", interface = IInt, value = 0),
                          dict(name = "reshape", interface = IBool, value = True),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("rotate")

gaussian = Factory(name = "gaussian",
                description = "gaussian filter",
                category = "image",
                nodemodule = "algo",
                nodeclass = "gaussian",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "sigma", interface = IFloat, value = 0.),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("gaussian")

saturate = Factory(name = "saturate",
                description = "saturate colors of the image",
                category = "image",
                nodemodule = "algo",
                nodeclass = "saturate",
                inputs = (dict(name = "img", interface = IImage),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("saturate")

high_level = Factory(name = "high_level",
                description = "high_level filter",
                category = "image",
                nodemodule = "algo",
                nodeclass = "high_level",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "color", interface = IColor, value = (0,0,0) ),),
                outputs = (dict(name = "alpha", interface = None),),
                )

__all__.append("high_level")

color_select = Factory(name = "color_select",
                description = "",
                category = "image",
                nodemodule = "algo",
                nodeclass = "color_select",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "color", interface = IColor, value = (0,0,0) ),
                          dict(name = "tol", interface = IInt, value = 0),),
                outputs = (dict(name = "alpha", interface = None),),
                )

__all__.append("color_select")

