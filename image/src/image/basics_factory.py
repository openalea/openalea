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

    nf = Factory( name= "load image", 
                  description= "load an image file", 
                  category = "Image", 
                  nodemodule = "basics",
                  nodeclass = "load_image",
                  inputs=(dict(name="Filename", interface=IFileStr,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "save image", 
                  description= "save an image file", 
                  category = "Image", 
                  nodemodule = "basics",
                  nodeclass = "save_image",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Filename", interface=IFileStr,),
                          ),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "view image", 
                  description= "display an image", 
                  category = "Image", 
                  nodemodule = "basics",
                  nodeclass = "pix_view",
                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

    nf = Factory( name= "convert mode", 
                  description= "change the color mode of the image", 
                  category = "Image", 
                  nodemodule = "basics",
                  nodeclass = "convert",
                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Mode", interface=IImageMode,value="RGB"),
                          ),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )

    package.add_factory( nf )

