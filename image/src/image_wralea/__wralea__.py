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
# from image_interface import IImage
# from image_interface_widget import IImageWidget
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

###################################################
#
#        image basics
#
###################################################
image = Factory(name = "img",
                description = "display image",
                category = "image",
                nodemodule = "image",
                nodeclass = "image",
                inputs = (dict(name = "img", interface = "IImage"),),
                outputs = (dict(name = "img", interface = "IImage"),),
                )

__all__.append("image")

size2 = Factory(name = "size2",
                description = "size of a 2D image",
                category = "image",
                nodemodule = "image",
                nodeclass = "size2",
                inputs = (dict(name = "img", interface = "IImage"),),
                outputs = (dict(name = "width", interface = IInt),
                           dict(name = "height", interface = IInt),),
                )

__all__.append("size2")

size3 = Factory(name = "size3",
                description = "size of a 3D image",
                category = "image",
                nodemodule = "image",
                nodeclass = "size3",
                inputs = (dict(name = "img", interface = "IImage"),),
                outputs = (dict(name = "width", interface = IInt),
                           dict(name = "height", interface = IInt),
                           dict(name = "depth", interface = IInt),),
                )

__all__.append("size3")


lena = Factory(name = "lena",
                description = "lena image",
                category = "image",
                nodemodule = "image",
                nodeclass = "lena",
                outputs = (dict(name = "img", interface = "IImage"),),
                )

__all__.append("lena")

###################################################
#
#        palette
#
###################################################
apply_palette = Factory(name = "apply_palette",
                description = "apply a palette to data to create an image",
                category = "image",
                nodemodule = "palette",
                nodeclass = "apply_palette",
                inputs = (dict(name = "data", interface = None),
                          dict(name = "pal", interface = None),),
                outputs = (dict(name = "img", interface = "IImage"),),
                )

__all__.append("apply_palette")

bw = Factory(name = "bw",
                description = "black and white palette",
                category = "image",
                nodemodule = "palette",
                nodeclass = "wra_bw",
                inputs = (),
                outputs = (dict(name = "pal", interface = None),),
                )

__all__.append("bw")

grayscale = Factory(name = "grayscale",
                description = "grayscale palette",
                category = "image",
                nodemodule = "palette",
                nodeclass = "wra_grayscale",
                inputs = (dict(name = "nb", interface = IInt, value = 1),),
                outputs = (dict(name = "pal", interface = None),),
                )

__all__.append("grayscale")

#########################################
#
#    spatial image
#
#########################################
spatial_image = Factory( name= "spatial_image",
                         description= "create a SpatialImage from a numpy array",
                category = "image",
                nodemodule = "spatial_image",
                nodeclass = "image",
                                inputs=(dict(name="array", interface="ISequence",),
                                        dict(name="resolution", interface="ITuple",),
                                        dict(name="vectorDim", interface="IInt",),
                                        dict(name="info", interface="IDict",),
                                        ),
                         outputs=(dict(name="image", interface="IImage"),),
                         )

__all__.append('spatial_image')

empty_image = Factory( name= "empty_image_like",
                       description= "create a SpatialImage from a numpy array",
                       category = "image",
                       nodemodule = "spatial_image",
                       nodeclass = "empty_image_like",
                       inputs=(dict(name="image", interface="IImage",),
                       ),
                       outputs=(dict(name="image", interface="IImage"),),
                       )

__all__.append('empty_image')


resolution = Factory( name= "resolution",
                description= "extract resolution from spatial image",
                category = "image",
                nodemodule = "spatial_image",
                nodeclass = "resolution",
                inputs=(dict(name="img", interface="IImage",),),
                outputs=(dict(name="res", interface = ISequence),),
            )

__all__.append('resolution')

info = Factory( name= "info",
                description= "extract info from spatial image",
                category = "image",
                nodemodule = "spatial_image",
                nodeclass = "info",
                inputs=(dict(name="img", interface="IImage",),),
                outputs=(dict(name="info", interface=IDict),),
            )

__all__.append('info')


null_vector_field_like = Factory( name= "null_vector_field_like",
                         description= "create a SpatialImage from a numpy array",
                         category = "image",
                         nodemodule = "spatial_image",
                         nodeclass = "null_vector_field_like",
                         inputs=(dict(name="image", interface="IImage",),
                         ),
                         outputs=(dict(name="image", interface="IImage"),),
                         )

__all__.append('null_vector_field_like')

