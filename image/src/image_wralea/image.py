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

from numpy import array,uint8
from openalea.image import bw,grayscale,flatten,apply_mask,SpatialImage

def image (img) :
	return img,

def size (img) :
	h,w = img.shape[:2]
	return w,h

def wra_apply_mask (img, mask, background_color) :
	return apply_mask(img,mask,background_color),

wra_apply_mask.__doc__ = apply_mask.__doc__

def apply_palette (data, palette) :
	if data.dtype == bool :
		data = data * 1
	
	img = palette[data]
	
	if isinstance(data,SpatialImage) :
		img = SpatialImage(img,img.resolution,palette.shape[1],img.info)
	
	return img,

def wra_grayscale (nb) :
	return grayscale(nb),

wra_grayscale.__doc__ = grayscale.__doc__

def wra_bw () :
	return bw(),

wra_bw.__doc__ = bw.__doc__

def invert (img) :
	if img.dtype == bool :
		return -img
	else :
		return 255 - img,

def wra_flatten (img_list) :
	return flatten(img_list),

wra_flatten.__doc__ = flatten.__doc__
