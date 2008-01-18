# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
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


from openalea.core import Factory
from openalea.core.interface import *
from images_wralea import IImageMode,IPix

def define_factory (package) :
    nf = Factory( name= "bands", 
                  description= "extract band names of an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "bands",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="bands", interface=ISequence,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "colors L", 
                  description= "list of colors in a one band image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "colors",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="colors", interface=ISequence,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "data", 
                  description= "extract data from an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "data",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="data", interface=ISequence,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "extrema L", 
                  description= "extract min and max value of a single band image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "extrema",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="min", interface=IInt,),
                          dict(name="max",interface=IInt)),
                  )

    package.add_factory( nf )

    nf = Factory( name= "get pixel", 
                  description= "extract pixel color of an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "get_pixel",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="x",interface=IInt),
                          dict(name="y",interface=IInt)),
                  outputs=(dict(name="color", interface=None,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "histogram", 
                  description= "extract color histogram of an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "histogram",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="mask",interface=IPix)),
                  outputs=(dict(name="histo", interface=ISequence,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "format", 
                  description= "extract image format", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "format",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="format", interface=IStr,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "mode", 
                  description= "extract mode of an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "mode",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="mode", interface=IImageMode,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "size", 
                  description= "extract size of an image", 
                  category = "Image", 
                  nodemodule = "data_access",
                  nodeclass = "size",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="width", interface=IInt,),dict(name="height",interface=IInt)),
                  )

    package.add_factory( nf )


