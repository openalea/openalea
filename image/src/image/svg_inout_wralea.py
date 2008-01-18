# -*- python -*-
# -*- coding: latin-1 -*-
#
#       SVGWralea : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#						Jerome Chopard <jerome.chopard@sophia.inria.fr>
#						Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide basics function to handle 2D images
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

from openalea.core import *
from openalea.core.interface import *
from images_wralea import IPix

class ISvgElm(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 
    # interface methods

def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'J. Chopard',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'PIL wrapping and svg module.',
               'url' : 'http://www.svg.org'
               }
    
    
    package = Package("image.svg", metainfo)

    nf = Factory( name= "loadSC", 
                  description= "load an svg file and convert it to svg scene", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "loadsc",
                  inputs=(dict(name="Filename", interface=IFileStr,),),
                  outputs=(dict(name="scene", interface=ISvgElm,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "writeSC", 
                  description= "write an svg scene into a file", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "loadsc",
                  inputs=(dict(name="scene", interface=ISvgElm),
                          dict(name="Filename", interface=IFileStr,),),
                  outputs=(),
                  )

    package.add_factory( nf )

    nf = Factory( name= "get elm", 
                  description= "retrieve an element from a group", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "get_elm",
                  inputs=(dict(name="scene", interface=ISvgElm),
                          dict(name="id", interface=IStr,),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "image", 
                  description= "create an svg image", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_image",
                  inputs=(dict(name="id", interface=IStr),
                          dict(name="image", interface=IPix),
                          dict(name="filename", interface=IStr,),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "point", 
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

    package.add_factory( nf )

    nf = Factory( name= "group", 
                  description= "create an svg group", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_group",
                  inputs=(dict(name="id", interface=IStr),
                          dict(name="elms", interface=ISequence),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "layer", 
                  description= "create an svg layer", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_layer",
                  inputs=(dict(name="id", interface=IStr),
                          dict(name="elms", interface=ISequence),
                          dict(name="name", interface=IStr),),
                  outputs=(dict(name="elm", interface=ISvgElm),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "scene", 
                  description= "create an svg scene", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_scene",
                  inputs=(dict(name="width", interface=IFloat),
                          dict(name="height", interface=IFloat),
                          dict(name="layers", interface=ISequence),),
                  outputs=(dict(name="scene", interface=ISvgElm),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "elements", 
                  description= "list of elements of a group", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_elements",
                  inputs=(dict(name="group", interface=ISvgElm),),
                  outputs=(dict(name="elms", interface=ISequence),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "positions", 
                  description= "list of cooridnates from pts", 
                  category = "Image,svg", 
                  nodemodule = "svg_inout",
                  nodeclass = "svg_positions",
                  inputs=(dict(name="pts", interface=ISequence),),
                  outputs=(dict(name="coords", interface=ISequence),),
                  )

    package.add_factory( nf )

    pkg_manager.add_package(package)
