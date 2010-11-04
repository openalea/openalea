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
from openalea.image_wralea import IImage
from openalea.color import IColor

__name__ = "openalea.image.gui"

__all__ = []

from openalea.core import Factory
from openalea.core.interface import *


frames = Factory( name= "frames", 
				description= "",
				category = "",
				nodemodule = "frame",
				nodeclass = "register_frames",
				inputs=(dict(name="viewer", interface=None),
				        dict(name="step", interface=IInt, value=0),
				        dict(name="output dir", interface=IDirStr, value=""),
				        dict(name="name_template",
				             interface=IStr,
				             value="frame%.4d.png"),),
				outputs=(dict(name="name", interface=IFileStr),),
			)

__all__.append('frames')

frame_list = Factory( name= "frame_list", 
				description= "",
				category = "",
				nodemodule = "frame",
				nodeclass = "frame_list",
				inputs=(dict(name="dir", interface=IDirStr, value=""),
				        dict(name="name_template",
				             interface=IStr,
				             value="frame%.4d.png"),),
				outputs=(dict(name="names", interface=ISequence),),
			)

__all__.append('frame_list')

animator_node = Factory( name= "Animator", 
				description= "",
				category = "",
				nodemodule = "animator_widget",
				nodeclass = "AnimatorNode",
				widgetmodule = "animator_widget",
				widgetclass = "AnimatorWidget",
				inputs=(dict(name="frames", interface=ISequence, value=[]),
				        dict(name="lastframe", interface=IFileStr, value=""),
				        dict(name="fps", interface=IInt, value=25),
				        dict(name="loop", interface=IBool, value=True),
				        dict(name="reinit", interface=IBool, value=False),),
				outputs=(dict(name="frames", interface=ISequence,),),
				lazy = True,
			)

__all__.append('animator_node')

pick_color = Factory( name= "PickColor", 
				description= "",
				category = "",
				nodemodule = "pick_color_widget",
				nodeclass = "pick_color",
				widgetmodule = "pick_color_widget",
				widgetclass = "PickColorWidget",
				inputs=(dict(name="img", interface=IImage),
				        dict(name="col", interface=IColor, value=(0,0,0) ),),
				outputs=(dict(name="img", interface=IImage),
				         dict(name="col", interface=IColor,),),
				lazy = True,
			)

__all__.append('pick_color')

select_box = Factory( name= "SelectBox", 
				description= "",
				category = "",
				nodemodule = "select_box_widget",
				nodeclass = "select_box",
				widgetmodule = "select_box_widget",
				widgetclass = "SelectBoxWidget",
				inputs=(dict(name="img", interface=IImage),
				        dict(name="x", interface=IInt, value=0),
				        dict(name="y", interface=IInt, value=0),
				        dict(name="dx", interface=IInt, value=0),
				        dict(name="dy", interface=IInt, value=0),),
				outputs=(dict(name="img", interface=IImage),
				        dict(name="x", interface=IInt),
				        dict(name="y", interface=IInt),
				        dict(name="dx", interface=IInt),
				        dict(name="dy", interface=IInt),),
				lazy = True,
			)

__all__.append('select_box')

#########################################
#
#	display
#
#########################################

display = Factory(  name= "display", 
		    description= "",
		    category = "",
		    nodemodule = "viewer",
		    nodeclass = "display",
		    inputs=(dict(name="images", interface=None),
			    dict(name="palette_name", interface=IStr, value="grayscale"),
			    dict(name="color_index_max", interface=IInt, value=None),),
		    outputs=(dict(name="view", interface=None),),
                                )

__all__.append('display')


point_selection = Factory(name= "Point Selection", 
			  description= "enable to select points in an image",
			  category = "image",
			  nodemodule = "point_selection_node",
			  nodeclass = "point_selection",
			  widgetmodule = "point_selection_widget",
			  widgetclass = "PointSelectionWidget",
                          inputs=(dict(name="image", interface=None),
			          dict(name="points", interface=None),
                                  dict(name="new_points", interface=None, hide=True),),
			  outputs=(dict(name="image", interface=None),
			           dict(name="points", interface=None,),),
                          lazy=True
			  )

__all__.append('point_selection')

