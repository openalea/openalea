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

from numpy import array,uint8

__all__ = ["flatten"]
def flatten (img_list) :
	"""Concatenate all images into a single image
	
	Use alpha to blend images one on top of each other
	
	.. warning:: all images must have the same shape and an alpha channel
	
	.. warning:: the resulting image has no alpha channel
	
	:Parameters:
	 - `img_list` (list of NxMx4 array of uint8)
	
	:Returns Type: NxMx3 array of uint8
	"""
	R = img_list[0][...,0]
	G = img_list[0][...,1]
	B = img_list[0][...,2]
	
	for lay in img_list[1:] :
		alpha = lay[...,3] / 255.
		ialpha = 1. - alpha
		R = R * ialpha + lay[...,0] * alpha
		G = G * ialpha + lay[...,1] * alpha
		B = B * ialpha + lay[...,2] * alpha
	
	return array([R,G,B],uint8).transpose(1,2,0)

