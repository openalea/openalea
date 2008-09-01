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

__name__ = "openalea.image.svg"
__alias__ = ["image.svg"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium - J. Chopard'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'PIL wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = ["loadsc", "writesc", "getelm", "img",
           "point", "group", "layer", "scene",
           "elements", "positions",]


from openalea.core import *
from openalea.core.interface import *
from openalea.image.interface import IPix

class ISvgElm(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 

loadsc = Factory( name= "loadSC", 
                  description= "load an svg file and convert it to svg scene", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "loadsc",
                  inputs=(dict(name="Filename", interface=IFileStr,),),
                  outputs=(dict(name="scene", interface=ISvgElm,),),
                  )


writesc = Factory( name= "writeSC", 
                   description= "write an svg scene into a file", 
                   category = "Image,svg", 
                   nodemodule = "svg_inout",
                   nodeclass = "loadsc",
                   inputs=(dict(name="scene", interface=ISvgElm),
                           dict(name="Filename", interface=IFileStr,),),
                   outputs=(),
                   )


getelm = Factory( name= "get elm", 
                  description= "retrieve an element from a group", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "get_elm",
                  inputs=(dict(name="scene", interface=ISvgElm),
                          dict(name="id", interface=IStr,),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )


img = Factory( name= "image", 
               description= "create an svg image", 
               category = "Image,svg", 
               nodemodule = "svg_inout",
               nodeclass = "svg_image",
               inputs=(dict(name="id", interface=IStr),
                       dict(name="image", interface=IPix),
                          dict(name="filename", interface=IStr,),),
               outputs=(dict(name="elm", interface=ISvgElm),),
               )

    
point = Factory( name= "point", 
                 description= "create an svg point", 
                 category = "Image,svg", 
                 nodemodule = "svg_inout",
                 nodeclass = "svg_point",
                 inputs=(dict(name="id", interface=IStr),
                         dict(name="x", interface=IFloat),
                          dict(name="y", interface=IFloat),
                         dict(name="radius", interface=IFloat),
                         dict(name="color", interface=IRGBColor,),),
                 outputs=(dict(name="elm", interface=ISvgElm),),
                 )


group = Factory( name= "group", 
                 description= "create an svg group", 
                 category = "Image,svg", 
                 nodemodule = "svg_inout",
                 nodeclass = "svg_group",
                 inputs=(dict(name="id", interface=IStr),
                         dict(name="elms", interface=ISequence),),
                 outputs=(dict(name="elm", interface=ISvgElm),),
                 )


layer = Factory( name= "layer", 
                  description= "create an svg layer", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_layer",
                  inputs=(dict(name="id", interface=IStr),
                          dict(name="elms", interface=ISequence),
                          dict(name="name", interface=IStr),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )


scene = Factory( name= "scene", 
                 description= "create an svg scene", 
                 category = "Image,svg", 
                 nodemodule = "svg_inout",
                 nodeclass = "svg_scene",
                 inputs=(dict(name="width", interface=IFloat),
                         dict(name="height", interface=IFloat),
                         dict(name="layers", interface=ISequence),),
                 outputs=(dict(name="scene", interface=ISvgElm),),
                 )


elements = Factory( name= "elements", 
                    description= "list of elements of a group", 
                    category = "Image,svg", 
                    nodemodule = "svg_inout",
                    nodeclass = "svg_elements",
                    inputs=(dict(name="group", interface=ISvgElm),),
                    outputs=(dict(name="elms", interface=ISequence),),
                    )


positions = Factory( name= "positions", 
                     description= "list of cooridnates from pts", 
                     category = "Image,svg", 
                     nodemodule = "svg_inout",
                     nodeclass = "svg_positions",
                     inputs=(dict(name="pts", interface=ISequence),),
                     outputs=(dict(name="coords", interface=ISequence),),
                     )


