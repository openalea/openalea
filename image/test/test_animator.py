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
from openalea.image.all import rainbow, FrameAnimator

qapp = QtGui.QApplication.instance()

if qapp:
	pal = rainbow(99)

	frames = []

	for i in xrange(100) :
		pix = QtGui.QPixmap(300,200)
		pix.fill(QtGui.QColor(*tuple(pal[i]) ) )
		frames.append(pix)

	w = FrameAnimator()
	w.set_frames(frames)

	w.show()


