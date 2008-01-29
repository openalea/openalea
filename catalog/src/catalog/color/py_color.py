# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" Colormap Nodes """
__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
import colormap


def color_map(val,minval = 0,maxval = 1,coul1 = 80,coul2 = 20):
    map = colormap.ColorMap()
    if val is None:
	return lambda x: map(x,minval,maxval,coul1,coul2)
    elif callable(val):
	return lambda x: map(val(x),minval,maxval,coul1,coul2)
    else: return map(val,minval,maxval,coul1,coul2),

