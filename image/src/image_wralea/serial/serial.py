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

from os.path import exists
from numpy import issubdtype
from openalea.image import load,save,imread
from pylab import imsave

def wra_load (filename, mmap_mode) :
	return load(filename,mmap_mode),

wra_load.__doc__ = load.__doc__

def wra_save (filename, img) :
	save(filename,img)
	return img,

wra_save.__doc__ = save.__doc__

def wra_imread (filename) :
	return imread(filename)

wra_imread.__doc__ = imread.__doc__

def wra_imsave (filename, img) :
	"""Save an image into a file
	
	.. warning:: depending on the type of data in the image the method chosen
	             to save the image will be different. If the image is an RGB(A)
	             2D array, the image will be saved using pilutils.imsave. If
	             the image is a SpatialImage or a 3D array or an array of data
	             then the write_inrimage function will be used
	
	:Parameters:
	 - `filename` (str)
	 - `img` (array)
	"""
	if isinstance(img,SpatialImage) :
		write_inrimage(filename,img)
	elif len(img.shape) == 3 \
	     and img.shape[2] in (3,4) \
	     and issubdtype(img.dtype,int) :
		imsave(filename,img)
	else :
		raise UserWarning("unable to find the type of this image")
	
	return img,

wra_imsave.__doc__ = imsave.__doc__

