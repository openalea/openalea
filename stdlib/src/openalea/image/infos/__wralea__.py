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


from openalea.core import Factory
from openalea.core.interface import *
from openalea.image.interface import IImageMode,IPix

__name__ = "openalea.image.infos"
__alias__ = ["image.infos"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'PIL wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = ["bands", "colors", "data", "extrema", "pixel", "histo", "format", "mode", "size"]



bands = Factory( name= "bands", 
                 description= "extract band names of an image", 
                 category = "Image", 
                 nodemodule = "data_access",
                 nodeclass = "bands",
                 inputs=(dict(name="Image", interface=IPix,),),
                 outputs=(dict(name="bands", interface=ISequence,),),
                 )


colors = Factory( name= "colors L", 
                  description= "list of colors in a one band image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "colors",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="colors", interface=ISequence,),),
                  )


data = Factory( name= "data", 
                description= "extract data from an image", 
                category = "Image", 
                nodemodule = "data_access",
                nodeclass = "data",
                inputs=(dict(name="Image", interface=IPix,),),
                outputs=(dict(name="data", interface=ISequence,),),
                )


extrema = Factory( name= "extrema L", 
                   description= "extract min and max value of a single band image", 
                   category = "Image", 
                   nodemodule = "data_access",
                   nodeclass = "extrema",
                   inputs=(dict(name="Image", interface=IPix,),),
                   outputs=(dict(name="min", interface=IInt,),
                            dict(name="max",interface=IInt)),
                   )


pixel = Factory( name= "get pixel", 
                 description= "extract pixel color of an image", 
                 category = "Image", 
                 nodemodule = "data_access",
                 nodeclass = "get_pixel",
                 inputs=(dict(name="Image", interface=IPix,),
                         dict(name="x",interface=IInt),
                         dict(name="y",interface=IInt)),
                 outputs=(dict(name="color", interface=None,),),
                 )


histo = Factory( name= "histogram", 
                 description= "extract color histogram of an image", 
                 category = "Image", 
                 nodemodule = "data_access",
                 nodeclass = "histogram",
                 inputs=(dict(name="Image", interface=IPix,),
                         dict(name="mask",interface=IPix)),
                 outputs=(dict(name="histo", interface=ISequence,),),
                 )


format = Factory( name= "format", 
                  description= "extract image format", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "format",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="format", interface=IStr,),),
                  )


mode = Factory( name= "mode", 
                description= "extract mode of an image", 
                category = "Image", 
                nodemodule = "data_access",
                nodeclass = "mode",
                inputs=(dict(name="Image", interface=IPix,),),
                outputs=(dict(name="mode", interface=IImageMode,),),
                )


size = Factory( name= "size", 
                description= "extract size of an image", 
                category = "Image", 
                nodemodule = "data_access",
                nodeclass = "size",
                inputs=(dict(name="Image", interface=IPix,),),
                outputs=(dict(name="width", interface=IInt,),dict(name="height",interface=IInt)),
                )


