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
__revision__ = " $Id: __wralea__.py$ "


from openalea.core import *
from openalea.core import Factory
from openalea.core.interface import *

__name__ = "openalea.image.movie"

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'PIL wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []


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


