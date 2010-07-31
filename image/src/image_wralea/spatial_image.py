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
"""Declaration of spatial image node functors
"""

__license__ = "Cecill-C"
__revision__ = " $Id: interface.py 2245 2010-02-08 17:11:34Z cokelaer $"

def info (img) :
	return getattr(img,"info",{}),

def resolution (img) :
	try :
		return img.resolution,
	except AttributeError :
		return (1,) * len(img.shape)


