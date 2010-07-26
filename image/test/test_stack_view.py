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
Test stack view
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from openalea.image import grayscale,read_inrimage,SpatialImage
from openalea.image.gui import StackView
from openalea.pglviewer import display

img = read_inrimage("SAM.inr.gz")
pal = grayscale(img.max(),True)
pix = SpatialImage(pal[img],img.resolution,vdim = 3)

sv = StackView(pix,slices = range(0,33,4) )
sv.redraw()

display(sv)

