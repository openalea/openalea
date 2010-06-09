# -*- python -*-
#
#       spatial_image: spatial nd images
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
This module a set of simple usefull algorithms to manipulate spatial images
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

__all__ = ["rectify",
           "view_right","view_face"]

def rectify (img) :
	"""Ensure that dimensions of the image are multiple of 4
	
	.. warning:: modify image in place
	
	:Parameters:
	 - `img` (array)
	"""
	shp = img.shape
	for i in xrange(min(3,len(shp) ) ) :
		if shp[i] % 4 != 0 :
			subshp = list(shp)
			subshp[i] = 4 - (shp[i] % 4)
			img = append(img,
			             zeros(subshp,self._data.dtype),
			             i)

def view_right (img) :
	"""Return a view on a 3D spatial image from right side
	
	:Parameters:
	 - `img` (array)
	"""
	ret = img.transpose(2,1,0)
	
	try :
		vx,vy,vz = ret.resolution
		ret.resolution = (vz,vy,vx)
	except AttributeError :
		pass
	
	return ret

def view_face (img) :
	"""Return a view on a 3D spatial image from the face
	
	:Parameters:
	 - `img` (array)
	"""
	ret = img.transpose(0,2,1)
	
	try :
		vx,vy,vz = ret.resolution
		ret.resolution = (vx,vz,vy)
	except AttributeError :
		pass
	
	return ret














