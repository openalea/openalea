# -*- python -*-
#
#       basics : image package
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#		        Jerome Chopard <jerome.chopard@sophia.inria.fr>
#	                Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""This module provide basics function to handle 2D images"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import Image
from Image import Image as Im

def bands (image) :
    return image.getbands(),

bands.__doc__ = Im.getbands.__doc__

def colors (image) :
    return image.getcolors(),

colors.__doc__ = Im.getcolors.__doc__

def data (image) :
    return list(image.getdata()),

data.__doc__ = Im.getdata.__doc__

def extrema (image) :
    return image.getextrema(),

extrema.__doc__ = Im.getextrema.__doc__

def get_pixel (image, x, y) :
    return image.getpixel( (x, y) ),

get_pixel.__doc__ = Im.getpixel.__doc__

def histogram (image, mask=None) :
    if mask is None :
        return image.histogram(),
    else :
        return image.histogram(mask)

histogram.__doc__ = Im.histogram.__doc__

def format (image) :
    """
    return image format
    """
    return image.format,

def mode (image) :
    """
    return image mode (RGB,RGBA,L,P,...)
    """
    return image.mode,

def size (image) :
    """
    return width and height of the image
    """
    return image.size[0], image.size[1]

