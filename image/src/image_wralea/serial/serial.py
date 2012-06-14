# -*- python -*-
#
#       image: image manipulation
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module import functions to manipulate images
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from os.path import exists
from numpy import issubdtype
from openalea.image.spatial_image import SpatialImage
from openalea.image.serial.inrimage import write_inrimage
from openalea.image.serial.basics import load,save,imread, imsave
from pylab import imsave

def wra_load (filename, mmap_mode) :
    return load(filename,mmap_mode),

wra_load.__doc__ = load.__doc__

def wra_save (filename, img) :
    save(filename,img)
    return img,

wra_save.__doc__ = save.__doc__

def wra_imread (filename) :
    return imread(filename)

wra_imread.__doc__ = imread.__doc__

def wra_imsave (filename, img) :
    return imsave(filename, img)

wra_imsave.__doc__ = imsave.__doc__

