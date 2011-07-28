# -*- python -*-
#
#       image.serial: read lsm
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################
"""
This module reads lsm format
"""

__license__ = "Cecill-C"
__revision__ = " $Id: $ "

import numpy as np
from openalea.image.spatial_image import SpatialImage

__all__ = []

try:
    from pylsm import lsmreader
    __all__.append("read_lsm")
except ImportError:
    pass

def read_lsm(filename,channel=0):
    """Read an lsm image

    :Parameters:
     - `filename` (str) - name of the file to read
     - `channel` (int) - optional
    """

    # LSM reader
    imageFile = lsmreader.Lsmimage(filename)
    imageFile.open()

    _info = {}
    #LSM header
    _VX = imageFile.header['CZ LSM info']['Voxel Size X']
    _VY = imageFile.header['CZ LSM info']['Voxel Size Y']
    _VZ = imageFile.header['CZ LSM info']['Voxel Size Z']
    _vx = _VX * 10**6
    _vy = _VY * 10**6
    _vz = _VZ * 10**6

    _PIXSIZE = imageFile.header['Image'][0]['Bit / Sample']

    _info["TYPE"] = 'unsigned fixed'
    _info["PIXSIZE"] = str(_PIXSIZE)
    _info["SCALE"] = 2
    _info["CPU"] = 'decm'
    _info["#GEOMETRY"] = 'CARTESIAN'

    #LSM datas
    _data = imageFile.image['data'][channel]
    im = SpatialImage(_data)
    im.resolution = _vx,_vy,_vz
    im.info = _info
    return im
