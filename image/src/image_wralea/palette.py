# -*- python -*-
#
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
#
#       File author(s): Chopard
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Declaration of image palette related node functors
"""

__license__ = "Cecill-C"
__revision__ = " $Id: interface.py 2245 2010-02-08 17:11:34Z cokelaer $"

from openalea.image.gui.palette import bw, grayscale
from openalea.image.spatial_image import SpatialImage

def apply_palette (data, palette) :
    if data.dtype == bool :
        data = data * 1

    img = palette[data]

    if isinstance(data,SpatialImage) :
        img = SpatialImage(img,img.resolution,palette.shape[1],img.info)

    return img,

def wra_grayscale (nb) :
    return grayscale(nb),

wra_grayscale.__doc__ = grayscale.__doc__

def wra_bw () :
    return bw(),

wra_bw.__doc__ = bw.__doc__


