#
#       image: image GUI
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test point selection
"""

__license__= "Cecill-C"
__revision__ = " $Id: $ "

from openalea.vpltk.qt import QtGui
from openalea.image.all import point_selection, SpatialImage
from square import square
from scipy.ndimage import rotate


qapp = QtGui.QApplication.instance()
if qapp:
    im1 = square()
    im2 = rotate(im1, 30)
    im2 = SpatialImage(im2,im1.resolution)

    w1 = point_selection (im1)
    w2 = point_selection (im2)
