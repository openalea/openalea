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
from openalea.image.all import imread, to_pix
from numpy import zeros,uint32


qapp = QtGui.QApplication.instance()

if qapp:
    try:
        img = imread("4_ocean_currents.png")
    except:
        img = imread("test/4_ocean_currents.png")

    #img = zeros( (100,50,3),uint32)
    #img[10:20,10:30,1] = 255

    pix = to_pix(img)

    w = QtGui.QLabel()
    w.setPixmap(pix)

    w.show()


