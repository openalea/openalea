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

from openalea.vpltk.qt import QtGui
from openalea.image.all import rainbow,grayscale, to_pix
from numpy import array,apply_along_axis

qapp = QtGui.QApplication.instance()

if qapp:
	data = array(range(10000) ).reshape( (100,100) )

	pal = rainbow(10000)

	img = pal[data]

	def func (pix) :
		if pix[0] > 100 :
			return (0,0,0)
		else :
			return (255,255,255)

	img = apply_along_axis(func,-1,img)



	pix = to_pix(img)

	w = QtGui.QLabel()
	w.setPixmap(pix)

	w.show()


