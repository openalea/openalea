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
from openalea.image.all import rainbow,grayscale, to_pix, to_img
from numpy import array,zeros,uint

qapp = QtGui.QApplication.instance()

if qapp:
    data = zeros( (100,100),uint)
    data[50:,:50] += 1
    data[:50,50:] += 2
    data[50:,50:] += 3

    pal = array([(255,0,0,255),(0,255,0,255),(0,0,255,255),(0,255,255,255)])

    img = pal[data]

    ii = to_img(img)
    ii.save("toto.png")

    pix = to_pix(img)

    w = QtGui.QLabel()
    w.setPixmap(pix)

    w.show()


