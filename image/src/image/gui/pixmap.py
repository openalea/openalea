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
This module defines functions to transform images into QPixmaps
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from PyQt4.QtGui import QPixmap,QImage
from numpy import array,uint32

def to_pix (img) :
	"""Transform an image array into a QPixmap
	
	:Parameters:
	 -`img` (2x2x3 or 4 array of int) - 2D matrix of RGB(A) image pixels
	                   i will correspond to x and j to y
	
	:Returns Type: QPixmap
	"""
	img = array(img,uint32)
	dat = (img[...,0] << 16) + (img[...,1] << 8) + img[...,2]
	
	if img.shape[2] == 4 :
		dat += img[...,3] << 24
	else :
		dat += 4278190080
	
	qimg = QImage(dat.flatten('F'),
	              img.shape[0],
	              img.shape[1],
	              QImage.Format_ARGB32)
	
	return QPixmap.fromImage(qimg)
