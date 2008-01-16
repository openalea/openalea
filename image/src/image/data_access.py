# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#						Jerome Chopard <jerome.chopard@sophia.inria.fr>
#						Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide basics function to handle 2D images
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

from Image import Image

def bands (image) :
    return image.getbands()

bands.__doc__=Image.getbands.__doc__

def bounding_box (image) :
    return image.getbbox()

def colors (image) :
    return image.colors()

def data (image) :
    return image.data()

def extrema (image) :
    return image.extrema()

def pixel (image, x, y) :
    return image.getpixel( (x,y) )

def histogram (image, mask=None) :
    if mask is None :
        return image.histogram()
    else :
        return image.histogram(mask)

def put_pixel (image, x, y, color) :
    image.putpixel( (x,y),color )

def format (image) :
    return image.format

def mode (image) :
    return image.mode

def size (image) :
    return image.size

