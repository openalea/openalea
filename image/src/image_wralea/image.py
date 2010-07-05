# -*- python -*-
#
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA  
#
#       File author(s): Chopard
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Declaration of image node functors
"""

__license__ = "Cecill-C"
__revision__ = " $Id: interface.py 2245 2010-02-08 17:11:34Z cokelaer $"

from numpy import array
from openalea.image import grayscale

def image (img) :
	return img,

def size (img) :
	return img.shape[:2]

def paste_alpha (img, alpha) :
	return array([img[...,0],img[...,1],img[...,2],alpha]).transpose( (1,2,0) ),

def apply_palette (data, palette) :
	return palette[data],

def wra_grayscale (nb) :
	return grayscale(nb),
