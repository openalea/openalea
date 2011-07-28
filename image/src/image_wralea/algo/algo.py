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

from scipy.ndimage import rotate,gaussian_filter
from openalea.image.algo.all import (saturate, high_level, color_select,
				     flatten, apply_mask, reverse_image,
				     scale_shift_intensities)

def crop (img, x, y, dx, dy) :
	data = img[y:(y + dy),x:(x + dx),...]

	return data,

def paste (img, im2, x, y, reshape) :
	data = img + 0
	dy,dx = im2.shape[:2]
	data[y:(y + dy),x:(x + dx),...] = im2

	return data,

def wra_apply_mask (img, mask, background_color) :
	return apply_mask(img,mask,background_color),

wra_apply_mask.__doc__ = apply_mask.__doc__

#def wra_invert (img) :
#	return invert(img)
#
#wra_invert.__doc__ = invert.__doc__

def wra_flatten (img_list) :
	return flatten(img_list),

wra_flatten.__doc__ = flatten.__doc__
def wra_rotate (img, angle, reshape) :
	data = rotate(img,angle,(0,1),reshape)

	return data,

wra_rotate.__doc__ = rotate.__doc__

def gaussian (img, sigma) :
	data = gaussian_filter(img,sigma)

	return data,

gaussian.__doc__ = gaussian_filter.__doc__

def wra_saturate (img) :
	return saturate(img),

wra_saturate.__doc__ = saturate.__doc__

def wra_high_level (img, color) :
	return high_level(img,color),

wra_high_level.__doc__ = high_level.__doc__

def wra_color_select (img, color, tol) :
	return color_select(img,color,tol),

wra_color_select.__doc__ = color_select.__doc__


def wra_reverse_image (img) :
	return reverse_image(img),

wra_reverse_image.__doc__ = reverse_image.__doc__







