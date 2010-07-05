# -*- python -*-
#
#       spatial_image.visu : spatial nd images
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module provide a 2D QPixmap view on spatial images
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

__all__ = ["PixmapView","PixmapStackView",
           "ScalableLabel","ScalableGraphicsView"]

from PyQt4.QtCore import Qt,SIGNAL
from PyQt4.QtGui import (QImage,QPixmap,QTransform,QMatrix,
                         QLabel,QGraphicsView)

class ScalableLabel (QLabel) :
	"""Scalable label that respect the ratio of the pixmap it display
	"""
	def __init__ (self, parent = None) :
		QLabel.__init__(self,parent)
		self.setScaledContents(True)
		
		self._ratio = 1.
		self._resolution = (1.,1.)
	
	def _compute_ratio (self) :
		pix = self.pixmap()
		if pix is not None :
			vx,vy = self._resolution
			self._ratio = (pix.height() * vy) / (pix.width() * vx)
	
	def set_resolution (self, x_scale, y_scale) :
		"""Set the resolution of the image
		
		:Parameters:
		 - `x_scale` (float) - size of a pixel in x direction
		 - `y_scale` (float) - size of a pixel in y direction
		"""
		self._resolution = (x_scale,y_scale)
		self._compute_ratio()
	
	def pixmap_coordinates (self, x_screen, y_screen) :
		"""Compute pixmaps coordinates that map the given point on the screen
		
		:Parameters:
		 - `x_screen` (int)
		 - `y_screen` (int)
		"""
		pix = self.pixmap()
		if pix is None :
			return None
		
		x_pix = x_screen * pix.width() / self.width()
		y_pix = y_screen * pix.height() / self.height()
		
		return x_pix,y_pix
	
	def resizeEvent (self, event) :
		if event.oldSize() != event.size() :
			w = event.size().width()
			h = event.size().height()
			if int(w * self._ratio) <= h :
				self.resize(w,w * self._ratio)
			else :
				self.resize(h / self._ratio,h)
	
	def setPixmap (self, pix) :
		QLabel.setPixmap(self,pix)
		self._compute_ratio()
	
	def mousePressEvent (self, event) :
		self.emit(SIGNAL("mouse_press"),event)
	
	def mouseMoveEvent (self, event) :
		self.emit(SIGNAL("mouse_move"),event)


class ScalableGraphicsView (QGraphicsView) :
	"""Graphics View that always zoom to fit it's content
	"""
	
	def __init__ (self, *args, **kwargs) :
		QGraphicsView.__init__(self,*args,**kwargs)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	
	def resizeEvent (self, event) :
		sc = self.scene()
		if sc is not None and event.oldSize() != event.size() :
			s = min(event.size().width() / sc.width(),
			        event.size().height() / sc.height() )
			
			t = QMatrix()
			t.scale(s,s)
			self.setMatrix(t)

