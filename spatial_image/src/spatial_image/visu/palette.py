# -*- python -*-
#
#       spatial_image.visu : spatial nd images
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

palette_names = ["grayscale","rainbow","bwrainbow"]

__all__ = palette_names + ["palette_names","palette_factory"]

from PyQt4.QtGui import QColor

def grayscale (cmax) :
	"""Grayscale values ranging from 0 to 255
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of int
	"""
	pal = [QColor(i * 255. / cmax,
	              i * 255. / cmax,
	              i * 255. / cmax,
	              255).rgba() for i in xrange(cmax + 1)]
	
	return pal

def rainbow (cmax) :
	"""Rainbow values ranging from red to blue and violet
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of int
	"""
	pal = [QColor.fromHsv(i * 359. / cmax,
	                      255,
	                      255,
	                      255).rgba() for i in xrange(cmax + 1)]
	
	return pal

def bwrainbow (cmax) :
	"""Black, White plus Rainbow values ranging from red to blue and violet
	
	:Parameters:
	 - `cmax` (int) - data maximum value
	
	:Returns Type: list of int
	"""
	pal = [QColor(255,255,255,0).rgba(),
	       QColor(0,0,0,0).rgba()] \
	    + [QColor.fromHsv(int(i * 359. / (cmax - 2.) ),
	                      255,
	                      255,
	                      255).rgba() for i in xrange(cmax - 1)]
	
	return pal

def palette_factory (palname, cmax) :
	assert palname in palette_names
	return globals()[palname](cmax)

