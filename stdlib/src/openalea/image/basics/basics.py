# -*- python -*-
#
#       basics : image package
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#			Jerome Chopard <jerome.chopard@sophia.inria.fr>
#			Fernandez Romain <romain.fernandez@sophia.inria.fr>
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
from openalea.core import Node
from openalea.image.interface import IPix


def load2rgb (filename) :
    """
    Load an image from a file and convert it into 'RGBA' image
    """
    img_pil = Image.open(filename)
    img = img_pil.convert('RGBA')
    return img,

def load2l (filename) :
    """
    Load an image from a file and convert it into 'L' image
    """
    img_pil = Image.open(filename)
    img = img_pil.convert('L')
    return img,


def save_image (image, filename) :
    image.save(filename)

save_image.__doc__=Im.save.__doc__

def convert (image, mode) :
    return image.convert(mode)

convert.__doc__=Im.convert.__doc__

def pix_visu(image) : 
    return image,
