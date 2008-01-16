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

def blend (image1, image2, alpha) :
    pass

def composite (image1, image2, mask) :
    pass

def merge (mode, bands) :
    pass

def paste (image_target, image_source, x, y) :
    """
    paste image_source into image_target at position x,y
    """
    return image_target.paste(image_source,(x,y))

def fill (image, color, xmin, xmax, ymin, ymax) :
    return image.paste(color,(xmin,ymin,xmax,ymax))

def put_alpha (image, band) :
    return image.putalpha(band)

def split (image) :
    return image.split()
