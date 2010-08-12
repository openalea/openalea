# -*- python -*-
#
#       image : geometric transformation filters
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
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
__revision__ = " $Id:  $ "

from openalea.core import *
from openalea.image_wralea import IImage

__name__ = "openalea.image.interpolation"

__all__ = []

list_type = ['bool', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'float96', 'complex64', 'complex128', 'complex192']

shift = Factory(name = "shift",
                description = "Shift an array",
                category = "image",
                nodemodule = "interpolation",
                nodeclass = "wra_shift",
                inputs = (dict(name = "img", interface = None),
                          dict(name = "shift", interface = ITuple),
                          dict(name = "output", interface=IEnumStr(list_type), value=None),
                          dict(name = "order", interface = IInt, value=3),
                          dict(name = "mode", interface=IEnumStr(["constant", "nearest", "reflect", "wrap"]), value="constant"),
                          dict(name = "cval", interface=IFloat, value=0.),
                          dict(name = "prefilter", interface=IBool, value=True),),
                outputs = (dict(name = "img", interface = None),),
                )

__all__.append("shift")

rotate = Factory(name = "rotate",
                description = "Rotate an array",
                category = "image",
                nodemodule = "interpolation",
                nodeclass = "wra_rotate",
                inputs = (dict(name = "img", interface = None),
                          dict(name = "angle", interface = IInt, value = 0),
                          dict(name = "axes", interface = ITuple, value = (1,0)),
                          dict(name = "reshape", interface = IBool, value = True),
                          dict(name = "output", interface=IEnumStr(list_type), value=None),
                          dict(name = "order", interface = IInt, value=3),
                          dict(name = "mode", interface=IEnumStr(["constant", "nearest", "reflect", "wrap"]), value="constant"),
                          dict(name = "cval", interface=IFloat, value=0.),
                          dict(name = "prefilter", interface=IBool, value=True),),
                outputs = (dict(name = "img", interface = None),),
                )
__all__.append("rotate")

zoom = Factory(name = "zoom",
                description = "Zoom an array",
                category = "image",
                nodemodule = "interpolation",
                nodeclass = "wra_zoom",
                inputs = (dict(name = "img", interface = None),
                          dict(name = "zoom", interface = IFloat),
                          dict(name = "output", interface=IEnumStr(list_type), value=None),
                          dict(name = "order", interface = IInt, value=3),
                          dict(name = "mode", interface=IEnumStr(["constant", "nearest", "reflect", "wrap"]), value="constant"),
                          dict(name = "cval", interface=IFloat, value=0.),
                          dict(name = "prefilter", interface=IBool, value=True),),
                outputs = (dict(name = "img", interface = None),),
                )

__all__.append("zoom")

crop = Factory(name = "crop",
                description = "crop an image",
                category = "image",
                nodemodule = "interpolation",
                nodeclass = "crop",
                inputs = (dict(name = "img", interface = None),
                          dict(name = "xmin", interface = IInt, value = 0),
                          dict(name = "ymin", interface = IInt, value = 0),
                          dict(name = "xmax", interface = IInt, value = 0),
                          dict(name = "ymax", interface = IInt, value = 0),),
                outputs = (dict(name = "img", interface = None),),
                )

__all__.append("crop")

resample = Factory(name = "resampling",
                description = "Resample an image via a transformation matrix",
                category = "image",
                nodemodule = "interpolation",
                nodeclass = "resample",
                inputs = (dict(name = "img", interface = IImage),
                          dict(name = "transformation", interface = None),
                          dict(name = "order", interface = IInt, value=1),
                          dict(name = "output_shape", interface = None, hide=True),
                          dict(name = "output_voxels", interface = None, hide=True),
                          dict(name = "mode", interface=IEnumStr(["constant", "nearest", "reflect", "wrap"]), value="constant", hide=True),
                          dict(name = "cval", interface=IFloat, value=0., hide=True),
                          dict(name = "prefilter", interface=IBool, value=True, hide=True),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("resample")
