# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or  or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#			Jerome Chopard <jerome.chopard@sophia.inria.fr>
#			Fernandez Romain <romain.fernandez@sophia.inria.fr>
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

from openalea.core import Factory
from openalea.core.interface import *
from images_wralea import IPix

def define_factory (package) :
    nf = Factory( name= "blend", 
                  description= "create an interpolation between two images", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "blend",
                  inputs=(dict(name="Image", interface=IPix,),dict(name="Image", interface=IPix,),dict(name="alpha", interface=IFloat(min=0., max=1.0),value=0.5),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "composite", 
                  description= "create an interpolation between two images", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "composite",
                  inputs=(dict(name="Image", interface=IPix,),dict(name="Image", interface=IPix,),dict(name="masklpha", interface=IPix,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "merge", 
                  description= "merge bands into a single image", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "merge",
                  inputs=(dict(name="mode", interface=IStr,),dict(name="bands", interface=ISequence,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "paste", 
                  description= "paste an image into another", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "paste",
                  inputs=(dict(name="Image", interface=IPix,),dict(name="Image", interface=IPix,),dict(name="x", interface=IInt,),dict(name="y",interface=IInt)),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "fill", 
                  description= "fill a rectangle with a color", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "fill",
                  inputs=(dict(name="Image", interface=IPix,),dict(name="color", interface=None,),dict(name="xmin", interface=IInt,),dict(name="xmax",interface=IInt),dict(name="ymin",interface=IInt),dict(name="ymax",interface=IInt)),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "put_alpha", 
                  description= "add an alpha mask to an image", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "put_alpha",
                  inputs=(dict(name="Image", interface=IPix,),dict(name="alpha", interface=IPix,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "split", 
                  description= "split bands of an image", 
                  category = "Image", 
                  nodemodule = "image_transfo",
                  nodeclass = "split",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="R", interface=IPix,),
                          dict(name="G", interface=IPix,),
                          dict(name="B", interface=IPix,),
                          dict(name="AA", interface=IPix,),),
                  )

    package.add_factory( nf )


