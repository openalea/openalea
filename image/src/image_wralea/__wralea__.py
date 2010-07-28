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
from image_interface import IImage
from image_interface_widget import IImageWidget
from openalea.color import IColor,IColorWidget

__name__ = "openalea.image"

__version__ = '0.8.0'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Image manipulation'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'

__all__ = []

image = Factory(name = "img",
                description = "display image",
                category = "image",
                nodemodule = "image",
                nodeclass = "image",
                inputs = (dict(name = "img", interface = IImage),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("image")

size = Factory(name = "size",
                description = "size of image",
                category = "image",
                nodemodule = "image",
                nodeclass = "size",
                inputs = (dict(name = "img", interface = IImage),),
                outputs = (dict(name = "width", interface = IInt),
                           dict(name = "height", interface = IInt),),
                )

__all__.append("size")

apply_mask = Factory(name = "apply_mask",
                description = "apply a mask on a image",
                category = "image",
                nodemodule = "image",
                nodeclass = "wra_apply_mask",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "mask", interface = None),
                          dict(name = "background_color",
                               interface = IColor,
                               value = None),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("apply_mask")

apply_palette = Factory(name = "apply_palette",
                description = "apply a palette to data to create an image",
                category = "image",
                nodemodule = "image",
                nodeclass = "apply_palette",
                inputs = (dict(name = "data", interface = None),
                          dict(name = "pal", interface = None),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("apply_palette")

bw = Factory(name = "bw",
                description = "black and white palette",
                category = "image",
                nodemodule = "image",
                nodeclass = "wra_bw",
                inputs = (),
                outputs = (dict(name = "pal", interface = None),),
                )

__all__.append("bw")

grayscale = Factory(name = "grayscale",
                description = "grayscale palette",
                category = "image",
                nodemodule = "image",
                nodeclass = "wra_grayscale",
                inputs = (dict(name = "nb", interface = IInt, value = 1),),
                outputs = (dict(name = "pal", interface = None),),
                )

__all__.append("grayscale")

invert = Factory(name = "invert",
                description = "invert colors and alpha",
                category = "image",
                nodemodule = "image",
                nodeclass = "invert",
                inputs = (dict(name = "data", interface = None),),
                outputs = (dict(name = "data", interface = None),),
                )

__all__.append("invert")

flatten = Factory(name = "flatten",
                description = "flatten a set of images with same shape",
                category = "image",
                nodemodule = "image",
                nodeclass = "flatten",
                inputs = (dict(name = "data", interface = ISequence),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("flatten")


