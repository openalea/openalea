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
from numpy import array,zeros,uint8,apply_along_axis,rollaxis
from colorsys import hsv_to_rgb,rgb_to_hsv,rgb_to_hls
from ..spatial_image import SpatialImage

__all__ = ["bounding_box","apply_mask",
           "flatten","saturate",
           "high_level","color_select","border","end_margin","stroke"]

def bounding_box (mask) :
	"""Compute the bounding box of a mask
	
	:Parameters:
	 - `mask` (array of bool) - a nd array of booleans
	
	:Returns: a slice (ind_min,ind_max) for each dimension of the mask or None
	          if the mask do not contain any True value.
	          Where ind_min correspond to the first slice that contains a True
	          value and ind_max correspond to the first slice that contains
	          only False after slices that contain at least one True value
	
	:Returns Type: list of (int,int)
	"""
	loc_mask = mask
	bb = [slice(0,m) for m in mask.shape]
	
	for ind in range(len(mask.shape) ) :
		#find bounding box along ind axis
		imax = mask.shape[ind]
		
		#find imin
		bb[ind] = 0
		while (bb[ind] < imax) and (not loc_mask[bb].any() ) :
			bb[ind] += 1
		
		if bb[ind] == imax :
			return None
		
		bbimin = bb[ind]
		
		#find imax
		bb[ind] += 1
		while (bb[ind] < imax) and mask[bb].any() :
			bb[ind] += 1
		
		bbimax = bb[ind]
		
		#restore slice
		bb[ind] = slice(bbimin,bbimax)
	
	return bb

def apply_mask (img, mask, background_color = None) :
	"""Apply a mask on a given image
	
	If background_color is None, the mask is applied as the alpha channel in
	image. Pixels whose value is True will have an alpha value of 255 and others
	will have an alpha value of 0
	
	Else, pixels whose value is True will conserve their original color and
	others will have a color equal to background color
	
	:Parameters:
	 - `img` (NxM(xP)x3(4) array of uint8)
	 - `mask` (NxM(xP) array of bool)
	 - `background_color` (int,int,int,(int) )
	
	:Returns Type: (NxM(xP)x3(4) array of uint8)
	"""
	if background_color is None :
		R = img[...,0]
		G = img[...,1]
		B = img[...,2]
		alpha = mask * 255
		return rollaxis(array([R,G,B,alpha],img.dtype),0,len(img.shape) )
	else :
		raise NotImplementedError
def flatten (img_list, alpha = False) :
	"""Concatenate all images into a single image
	
	Use alpha to blend images one on top of each other
	
	.. warning:: all images must have the same nD shape
	             and an alpha channel (except maybe for the first one)
	
	If alpha is True, the resulting image will use the max of all alpha channels
	as an alpha channel.
	
	.. warning:: if the first image is a SpatialImage, the resulting image will
	             also be a SpatialImage but no test is made to ensure
	             consistency in the resolution of the layers
	
	:Parameters:
	 - `img_list` (list of NxM(xP)x4 array of uint8)
	 - `alpha` (bool) - the resulting image will have an alpha channel or not
	
	:Returns Type: NxM(xP)x3(4) array of uint8
	"""
	bg = img_list[0]
	
	R = bg[...,0]
	G = bg[...,1]
	B = bg[...,2]
	
	if bg.shape[-1] == 4 :
		alpha_list = [bg[...,3] ]
	else :
		alpha_list = []
	
	for lay in img_list[1:] :
		A = lay[...,3]
		alpha_list.append(A)
		
		A = A / 255.
		iA = 1. - A
		
		R = R * iA + lay[...,0] * A
		G = G * iA + lay[...,1] * A
		B = B * iA + lay[...,2] * A
	
	if alpha :
		A = array(alpha_list).max(axis = 0)
		ret = rollaxis(array([R,G,B,A],bg.dtype),0,len(bg.shape) )
	else :
		ret = rollaxis(array([R,G,B],bg.dtype),0,len(bg.shape) )
	
	if isinstance(bg,SpatialImage) :
		return SpatialImage(ret,bg.resolution,4,bg.info)
	else :
		return ret

def saturate (img) :
	"""Saturate colors in the image
	
	:Parameters:
	 - `img` (NxM(xP)x3(4) array of uint8)
	
	:Returns Type: NxM(xP)x3(4) array of uint8
	"""
	if img.shape[2] == 3 :
		def func (pix) :
			h,s,v = rgb_to_hsv(*tuple(v / 255. for v in pix[:3]) )
			return tuple(int(v * 255) for v in hsv_to_rgb(h,1.,1.) )
	else :
		def func (pix) :
			h,s,v = rgb_to_hsv(*tuple(v / 255. for v in pix[:3]) )
			return tuple(int(v * 255) for v in hsv_to_rgb(h,1.,1.) ) + (pix[3],)
	
	return apply_along_axis(func,-1,img)

def intensity (color) :
	"""Returns the intensity of a color
	"""
	return (color[0] + color[1] + color[2]) / 3.

def high_level (img, threshold) :
	"""Create a mask where all pixel whose intensity is smaller than threshold
	are transparent.
	
	:Parameters:
	 - `img` (NxM(xP)x3(4) array of uint8)
	 - `threshold` (int between 0 and 255)
	
	:Returns Type: NxM(xP) array of bool
	"""
	def func (pix) :
		return intensity(pix) > threshold
	
	return apply_along_axis(func,-1,img)

def color_select (img, color, tol) :
	"""Create a mask to conserve only colors 
	around the given color.
	
	:ref:`http://en.wikipedia.org/wiki/Color_difference`
	
	:Parameters:
	 - `img` (NxM(xP)x3(4) array of uint8)
	 - `color (int,int,int) - R,G,B color
	 - `tol` (int between 0 and 100) - distance max between a pixel and color
	                                   to be conserved
	
	:Returns Type: NxM(xP) array of bool
	"""
	href,lref,sref = rgb_to_hls(*tuple(v / 255. for v in color[:3]) )
	tol /= 100.
	
	def func (pix) :
		h,l,s = rgb_to_hls(*tuple(v / 255. for v in pix[:3]) )
		d = sqrt( ( (l - lref) / 1.)**2 + \
		          ( (s - sref) / (1 + 0.045 * sref) )**2 + \
		          ( (h - href) / (1 + 0.015 * sref) )**2)
		
		return d < tol
	
	return apply_along_axis(func,-1,img)

def border(img, (x_min,y_min,z_min)=(0,0,0), (x_max,y_max,z_max)=(0,0,0) ):
    """
    A border is a outside black space that can be added to an array object.

    :Parameters: 
    - `img` ( NxMxP array)
                    
    - `x_min, y_min, z_min` (int, int,int) - The begining of the border

    - `x_max, y_max, z_max` (int, int, int) - The end of the border

    :Returns Type: (N+x_min+x_max) x (M+y_min+y_max) x (P+z_min+z_max) array
    """

    xdim, ydim, zdim = img.shape

    mat = zeros([xdim+x_min+x_max, ydim+y_min+y_max, zdim+z_min+z_max], img.dtype)
    mat[x_min:xdim+x_min, y_min:ydim+y_min, z_min:zdim+z_min] = img

    return mat

def end_margin(img, width, axis=None):
    """
    A end margin is a inside black space that can be added into the end of array object.

    :Parameters: 
    - `img` ( NxMxP array)

    - `width` (int) - size of the margin

    - `axis` (int optional) - axis along which the margin is added.  
    By default, add in all directions (see also stroke).

    :Returns Type: img
    """

    xdim, ydim, zdim = img.shape

    mat = zeros((xdim,ydim,zdim), img.dtype)
    
    if axis is None:
        mat[:-width,:-width,:-width] = img[:-width,:-width,:-width]
    elif axis == 0:
        mat[:-width,:,:] = img[:-width,:,:]
    elif axis == 1:
        mat[:,:-width,:] = img[:,:-width,:]
    elif axis == 2:
        mat[:,:,:-width] = img[:,:,:-width]
    else:
        raise AttributeError('axis')
    
    return mat


def stroke(img, width, outside=False):
    """
    A stroke is an outline that can be added to an array object.

    :Parameters: 
    - `img` ( NxMxP array)

    - `width` (int) - size of the stroke

    - `outside` (bool optional) - used to set the position of the stroke.
    By default, the position of the stroke is inside (outside = False)

    :Return Type : img     
    """

    xdim,ydim,zdim = img.shape

    if outside:
        mat = zeros([xdim+2*width, ydim+2*width, zdim+2*width], img.dtype)
        mat[width:xdim+width, width:ydim+width, width:zdim+width] = img
    else:
        mat = zeros((xdim,ydim,zdim), img.dtype)
        mat[width:-width,width:-width,width:-width] = img[width:-width,width:-width,width:-width]

    return mat

