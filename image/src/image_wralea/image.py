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


from openalea.image.spatial_image import SpatialImage
try:
    from scipy import lena as sci_lena
except ImportError:
    try:
        from scipy.misc import lena as sci_lena
    except ImportError:
        print "lena unavailable"

def lena():
    return SpatialImage(sci_lena())

def image (img) :
	return img,

def size2 (img) :
	h,w = img.shape[:2]
	return w,h

def size3 (img) :
	h,w,z = img.shape[:3]
	return w,h,z

def geom_size (img) :
	try :
		res = img.resolution
	except AttributeError :
		res = (1.,) * len(img.shape)

	return (v * res[i] for i,v in enumerate(img.shape) )
