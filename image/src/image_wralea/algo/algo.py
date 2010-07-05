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

from math import sqrt
from numpy import array,apply_along_axisfrom scipy.ndimage import rotate,gaussian_filter
from colorsys import hsv_to_rgb,rgb_to_hsv,rgb_to_hls

def crop (img, x, y, dx, dy) :
	data = img[x:(x + dx),y:(y + dy),...]
	
	return data,

def paste (img, im2, x, y, reshape) :
	data = img + 0
	dx,dy = im2.shape[:2]
	data[x:(x + dx),y:(y + dy),...] = im2
	
	return data,

def wra_rotate (img, angle, reshape) :
	data = rotate(img,angle,(0,1),reshape)
	
	return data,

def gaussian (img, sigma) :
	data = gaussian_filter(img,sigma)
	
	return data,

def saturate (img) :
	"""Saturate colors in the image
	"""
	def func (pix) :
		h,s,v = rgb_to_hsv(*tuple(v / 255. for v in pix[:3]) )
		return tuple(int(v * 255) for v in hsv_to_rgb(h,1.,1.) )
	
	data = apply_along_axis(func,2,img)
	
	return data,

def high_level (img, color) :
	"""Create a mask where all colors below color are transparent
	"""
	th = sum(color[:3]) / 3.
	
	def func (pix) :
		if (sum(pix[:3]) / 3.) > th :
			return 255
		else :
			return 0
	
	data = apply_along_axis(func,2,img)
	
	return data,

def color_select (img, color, tol) :
	"""Create a mask to conserve only colors 
	around the given color.
	
	:ref:`http://en.wikipedia.org/wiki/Color_difference`
	"""
	href,lref,sref = rgb_to_hls(*tuple(v / 255. for v in color[:3]) )
	tol /= 100.
	
	def func (pix) :
		h,l,s = rgb_to_hls(*tuple(v / 255. for v in pix[:3]) )
		d = sqrt( ( (l - lref) / 1.)**2 + \
		          ( (s - sref) / (1 + 0.045 * sref) )**2 + \
		          ( (h - href) / (1 + 0.015 * sref) )**2)
		
		if d < tol :
			return 255
		else :
			return 0
	
	data = apply_along_axis(func,2,img)
	
	return data,









