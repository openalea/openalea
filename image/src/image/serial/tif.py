# -*- python -*-
#
#       image.serial: read tif
#
#       Copyright 2011 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal@cirad.fr>
#                       Daniel Barbeau    <daniel.barbeau@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################
"""
This module reads 3D tiff format
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import numpy as np
from openalea.image.spatial_image import SpatialImage

__all__ = []

try:
    from libtiff import TIFFfile
    __all__.append("read_tif")
except ImportError:
    print 'Unable to import libtiff'
    pass

def read_tif(filename,channel=0):
    """Read a tif image

    :Parameters:
     - `filename` (str) - name of the file to read
    """

    # TIF reader
    tif = TIFFfile(filename)
    arr = tif.get_tiff_array()
    _data = arr[:].T

    nx, ny, nz = _data.shape

    # -- prepare metadata dictionnary --
    info_str = tif.get_info()
    info_dict = dict( filter( lambda x: len(x)==2,
                              (inf.split(':') for inf in info_str.split("\n"))
                              ) )
    for k,v in info_dict.iteritems():
        info_dict[k] = v.strip()

    # -- getting the voxelsizes from the tiff image: sometimes
    # there is a BoundingBox attribute, sometimes there are
    # XResolution, YResolution, ZResolution or spacing.
    # the object returned by get_tiff_array has a "get_voxel_sizes()"
    # method but it fails, so here we go. --
    if "BoundingBox" in info_dict:
        bbox = info_dict["BoundingBox"]
        xm, xM, ym, yM, zm, zM = map(float,bbox.split())
        _vx = (xM-xm)/nx
        _vy = (yM-ym)/ny
        _vz = (zM-zm)/nz
    else:
        if "XResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            xres_str = eval(info_dict["XResolution"])
            if isinstance(xres_str, list) and isinstance(xres_str[0], tuple):
                xres_str = xres_str[0]
                _vx = float(xres_str[0])/xres_str[1]
            elif isinstance(xres_str, (int, float)):
                _vx = float(xres_str)
            else:
                _vx = 1.
        else:
            _vx = 1.0 # dumb fallback, maybe we will find something smarter later on
        if "YResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            yres_str = eval(info_dict["YResolution"])
            if isinstance(yres_str, list) and isinstance(yres_str[0], tuple):
                yres_str = yres_str[0]
                _vy = float(yres_str[0])/yres_str[1]
            elif isinstance(yres_str, (int, float)):
                _vy = float(yres_str)
            else:
                _vy = 1.
        else:
            _vy = 1.0 # dumb fallback, maybe we will find something smarter later on

        if "ZResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            zres_str = eval(info_dict["ZResolution"])
            if isinstance(zres_str, list) and isinstance(zres_str[0], tuple):
                zres_str = zres_str[0]
                _vz = float(zres_str[0])/zres_str[1]
            elif isinstance(zres_str, (int, float)):
                _vz = float(zres_str)
            else:
                _vz = 1.
        else:
            if "spacing" in info_dict:
                _vz = eval(info_dict["spacing"])
            else:
                _vz = 1.0 # dumb fallback, maybe we will find something smarter later on

    tif.close()
    # -- dtypes are not really stored in a compatible way (">u2" instead of uint16)
    # but we can convert those --
    dt = np.dtype(arr.dtype.name)
    # -- Return a SpatialImage please! --
    im = SpatialImage(_data, dtype=dt)
    im.resolution = _vx,_vy,_vz

    return im
