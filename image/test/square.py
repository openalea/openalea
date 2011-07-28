#
#       image: image GUI
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test point selection
"""

__license__= "Cecill-C"
__revision__ = " $Id: $ "

import numpy as np
from openalea.image.all import SpatialImage

def square(shape=(100,100), voxels=(1,1), dimensions=(10,10), center=(49,49)):
    """
    Generating a 2-D square
    :Parameters:
    - `shape` (tuple) - image shape (xdim,ydim)
    - `voxels` (tuple) - voxels size (vx,vy)
    - `dimensions` (tuple) - dimensions of square (w,h)
    - `center` (tuple) - coordinates of center (cx,cy)
    :Returns: 2-D square into a inrimage
    """

    xdim, ydim = shape
    zdim = 1.
    vx,vy = voxels
    w,h = dimensions
    cx,cy = center

    data = np.zeros([xdim, ydim, zdim],np.uint8)

    for i in xrange(xdim):
        for j in xrange(ydim):
            if abs(i * vx - cx) < w and abs(j * vy - cy) < h :
                data[i,j] = 255 * i*j

    out = SpatialImage(data,(vx,vy,1))
    return out
