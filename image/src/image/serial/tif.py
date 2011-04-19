# -*- python -*-
#
#       image.serial: read lsm
#
#       Copyright 2011 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module reads 3D tiff format
"""

__license__ = "Cecill-C"
__revision__ = " $Id: $ "

import numpy as np
from ..spatial_image import SpatialImage

__all__ = []

try:
    from libtiff import TIFFfile
    __all__.append("read_tif")
except ImportError:
    pass

def read_tif(filename,channel=0):
    """Read a tif image

    :Parameters:
     - `filename` (str) - name of the file to read
    """

    # LSM reader
    tif = TIFFfile(filename)
    arr = tif.get_tiff_array()
    _data = arr[:].T

    nx, ny, nz = _data.shape

    info_str = tif.get_info()
    bbox = [ l.split('BoundingBox')[-1] for l in info_str.split('\n') if 'BoundingBox' in l][0]
    xm, xM, ym, yM, zm, zM = map(float,bbox.split())
    _vx = (xM-xm)/nx
    _vy = (yM-ym)/ny
    _vz = (zM-zm)/nz

    #LSM datas   
    im = SpatialImage(_data)
    im.resolution = _vx,_vy,_vz

    return im
