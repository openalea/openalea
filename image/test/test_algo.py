# -*- python -*-
#
#       image: image manipulation GUI
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
Test frame manipulator
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from numpy import array, random, zeros
from openalea.vpltk.qt import QtGui
from openalea.image.all import (rainbow,grayscale,bw,
				apply_mask,saturate,high_level,color_select, to_pix)

qapp = QtGui.QApplication.instance()

if qapp:

	#create image
	data = array(range(30000) ).reshape( (100,300) )

	pal = rainbow(30000)

	img = pal[data]

	img[:,:150,:] = img[:,:150,:] / 10

	#saturate
	sat = saturate(img)

	#high_level
	mask = high_level(img,100)
	pal = bw()
	hg = pal[mask * 1]
	hgimg = apply_mask(img,mask)

	#color_select
	mask = color_select(img,(0,255,0),10)
	sel = pal[mask * 1]
	selimg = apply_mask(img,mask)

	w_list = []
	y = 0
	for im,name in [(img,"img"),
			(sat,"sat"),
			(hgimg,"hgimg"),(hg,"hg"),
			(selimg,"selimg"),(sel,"sel")] :
		w = QtGui.QLabel()
		w.setWindowTitle(name)
		w.setPixmap(to_pix(im) )
		w.show()
		w.move(0,y)
		y += w.frameRect().height()
		w_list.append(w)


