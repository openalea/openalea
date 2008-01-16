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
from images_wralea import IPix

def define_factory (package) :

    nf = Factory( name= "crop image", 
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

    package.add_factory( nf )

    nf = Factory( name="resize image",
                  description="resize an image",
                  category="Image",
                  nodemodule="geom_transfo",
                  nodeclass="resize",
                )
                  
    package.add_factory( nf )

    nf = Factory( name="rotate image",
                  description="rotate an image",
                  category="Image",
                  nodemodule="geom_transfo",
                  nodeclass="rotate",
                )
                  
    package.add_factory( nf )



    nf = Factory( name= "mirror", 
                  description= "flip an image", 
                  category = "Image", 
                  nodemodule = "geom_transfo",
                  nodeclass = "mirror",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Horizontal", interface=IBool, value=True),
                          ),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

