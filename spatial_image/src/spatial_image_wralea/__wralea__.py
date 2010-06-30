# -*- python -*-
#
#       spatial_image: spatial nd images
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
nodes definition for spatial_image package
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *

__name__ = "spatial_image"
__alias__ = []
__version__ = '0.0.2'
__license__ = "Cecill-C"
__authors__ = 'Jerome Chopard'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'SpatialImage Node library.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = "icon.png"

__all__ = []

#########################################
#
#	serial
#
#########################################
read = Factory( name= "read inr", 
				description= "",
				category = "",
				nodemodule = "spatial",
				nodeclass = "read_inrimage",
				inputs=(dict(name="filename", interface=IFileStr,),),
				outputs=(dict(name="img", interface=None,),),
			)

__all__.append('read')

write = Factory( name= "write inr", 
				description= "",
				category = "",
				nodemodule = "spatial",
				nodeclass = "write_inrimage",
				inputs=(dict(name="img", interface=None,),
				        dict(name="filename", interface=IFileStr,),),
				outputs=(dict(name="img", interface=None,),),
			)

__all__.append('write')

#########################################
#
#	attributes
#
#########################################
info = Factory( name= "info", 
				description= "",
				category = "",
				nodemodule = "image",
				nodeclass = "info",
				inputs=(dict(name="img", interface=None,),),
				outputs=(),
			)

__all__.append('info')



#########################################
#
#	seminaire
#
#########################################

loadimage = Factory(name= "loadimage", 
                   description= "load image to numpy array", 
              	   category = "image",
 		   iinputs=(dict(name='filename', interface= IFileStr),),
		   outputs=(dict(name="matrix", interface=None),),
              	   nodemodule = "segmentation",
              	   nodeclass = "loadimage",
               	  )

__all__.append("loadimage")


invert = Factory(name= "invert", 
                   description= "grayscale inversion", 
              	   category = "image",
 		   inputs=(dict(name='matrix', interface=None),),
		   outputs=(dict(name="matrix", interface=None),),
              	   nodemodule = "segmentation",
              	   nodeclass = "invert",
               	  )

__all__.append("invert")



set_seeds = Factory(name= "set_seeds", 
                   description= "add seeds", 
              	   category = "image",
 		   inputs=(dict(name='matrix', interface=None),
                           dict(name='n', interface= IInt),
                           dict(name='seeds', interface= ISequence),),
		   outputs=(dict(name="markers", interface=None),),
              	   nodemodule = "segmentation",
              	   nodeclass = "set_seeds",
               	  )

__all__.append("set_seeds")


get_seeds = Factory(name= "get_seeds", 
                   description= "extraction of seeds with their center", 
              	   category = "image",
 		   inputs=(dict(name='matrix', interface=None),),
		   outputs=(dict(name="markers", interface=None),
                            dict(name="n", interface=IInt),),
              	   nodemodule = "segmentation",
              	   nodeclass = "get_seeds",
               	  )

__all__.append("get_seeds")


watershed = Factory(name= "watershed_ift", 
                   description= "segmentation of an image", 
              	   category = "image",
 		   inputs=(dict(name='input', interface=None),
                           dict(name='markers', interface=None),
                           dict(name='structure', interface=None),),
		   outputs=(dict(name="matrix", interface=None),),
              	   nodemodule = "spatial",
              	   nodeclass = "watershed_ift",
               	  )

__all__.append("watershed")


threshold = Factory(name= "threshold", 
                   description= "thresholding of an image", 
              	   category = "image",
 		   inputs=(dict(name='matrix', interface=None),
                           dict(name='threshold', interface=IInt),),
		   outputs=(dict(name="matrix", interface=None),),
              	   nodemodule = "segmentation",
              	   nodeclass = "threshold",
               	  )

__all__.append("threshold")


show = Factory(name= "show", 
                   description= "show image", 
              	   category = "image",
 		   inputs=(dict(name='matrix', interface=None),),
		   outputs=(dict(name="matrix", interface=None),),
              	   nodemodule = "segmentation",
              	   nodeclass = "show",
               	  )

__all__.append("show")


opening = Factory(name= "opening",
           	description= "",
           	category = "image",
		inputs = ( dict(name='matrix', interface=None),
     		           dict(name='structure', interface=None),
			   dict(name='iterations', interface=IInt,value=1),
			   dict(name='origine', interface=IInt,value=0),),
     	        outputs = (dict(name='matrix', interface=None),),
           	nodemodule = "spatial",
           	nodeclass = "binary_opening",
            )

__all__.append("opening")


closing = Factory(name= "closing",
           	description= "",
           	category = "image",
		inputs = ( dict(name='matrix', interface=None),
     		           dict(name='structure', interface=None),
			   dict(name='iterations', interface=IInt,value=1),
			   dict(name='origine', interface=IInt,value=0),),
     	        outputs = (dict(name='matrix', interface=None),),
           	nodemodule = "spatial",
           	nodeclass = "binary_closing",
            )

__all__.append("closing")

