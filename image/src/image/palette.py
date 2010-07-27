# -*- python -*-
#
#       image: image manipulation
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module provide a set of palettes to associate colors to data
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

from colorsys import hsv_to_rgb,rgb_to_hsv
from numpy import array,uint32

palette_names = ["grayscale","rainbow","bwrainbow"]

__all__ = palette_names + ["palette_names","palette_factory"]

def grayscale (cmax, alpha = False) :
	"""Grayscale values ranging from 0 to 255
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of (R,G,B,(A) )
	"""
	if alpha :
		pal = [(int(i * 255. / cmax),
		        int(i * 255. / cmax),
		        int(i * 255. / cmax),
		        int(i * 255. / cmax) ) for i in xrange(cmax + 1)]
	else :
		pal = [(int(i * 255. / cmax),
		        int(i * 255. / cmax),
		        int(i * 255. / cmax) ) for i in xrange(cmax + 1)]
	
	return array(pal,uint32)

def rainbow (cmax) :
	"""Rainbow values ranging from red to blue and violet
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of (R,G,B)
	"""
	cmax = float(cmax)
	pal = [tuple(int(v * 255) for v in hsv_to_rgb(i / cmax,1.,1.) ) \
	       for i in xrange(int(cmax + 1) )]
	
	return array(pal,uint32)

def bwrainbow (cmax, alpha = False) :
	"""Black, White plus Rainbow values ranging from red to blue and violet
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of int
	"""
	cmax = float(cmax)
	if alpha :
		pal = [(255,255,255,0),(0,0,0,0)] \
			+ [tuple(int(v * 255) for v in hsv_to_rgb(i / cmax,1.,1.) ) + (255,) \
			   for i in xrange(int(cmax - 1) )]
	else :
		pal = [(255,255,255),(0,0,0)] \
			+ [tuple(int(v * 255) for v in hsv_to_rgb(i / cmax,1.,1.) ) \
			   for i in xrange(int(cmax - 1) )]
	
	return array(pal,uint32)

def palette_factory (palname, cmax) :
	assert palname in palette_names
	return globals()[palname](cmax)

