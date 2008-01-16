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

import Image
from Image import Image as Im

def blend (image1, image2, alpha) :
    return Image.blend(image1,image2,alpha)

blend.__doc__=Image.blend.__doc__

def composite (image1, image2, mask) :
    return Image.composite(image1,image2,mask)

composite.__doc__=Image.composite.__doc__

def merge (mode, bands) :
    return Image.merge(mode,bands)

merge.__doc__=Image.merge.__doc__

def paste (image_target, image_source, x, y) :
    """
    paste image_source into image_target at position x,y
    """
    return image_target.paste(image_source,(x,y))

paste.__doc__=Im.paste.__doc__

def fill (image, color, xmin, xmax, ymin, ymax) :
    """
    fill a rectangle region with the given color
    """
    return image.paste(color,(xmin,ymin,xmax,ymax))

def put_alpha (image, band) :
    return image.putalpha(band)

put_alpha.__doc__=Im.putalpha.__doc__

def split (image) :
    return image.split()

split.__doc__=Im.split.__doc__

