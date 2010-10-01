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

__license__= "Cecill-C"
__revision__=" $Id: $ "

from openalea.image import SpatialImage, SlideViewer, palette_factory

def display (images, palette_name, color_index_max) :
    if isinstance(images,SpatialImage) :
	images = [images]
	
    w_list = []
    for i,img in enumerate(images) :
	w = SlideViewer()
		
	if color_index_max is None :
	    cmax = img.max()
	else :
	    cmax = color_index_max
		
	palette = palette_factory(palette_name,cmax)
		
	w.set_palette(palette,palette_name)
	w.set_image(img)
		
	w.setWindowTitle("image%d" % i)
	w.show()
	w_list.append(w)
	
    return w_list


