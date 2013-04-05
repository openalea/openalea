# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""
Expose the animator as a visualea node
"""

__revision__ = " $$ "

def load_local(mod,modules):
    modules = modules.split()
    modules = ''.join(modules).split(',')

    for m in modules:
        globals()[m] = mod.__getattribute__(m)

from openalea.vpltk.qt import QtGui, QtCore
load_local(QtCore,'QObject,SIGNAL,QRect,QSize,QPoint')
load_local(QtGui,"""QWidget,QLabel,QPixmap,
                         QHBoxLayout,QVBoxLayout,
                         QColor,QCursor,QPainter,QPen""")
from openalea.core import Node
from openalea.visualea.node_widget import NodeWidget
from openalea.image.gui.all import to_pix, ScalableLabel
from openalea.image.gui import icons_rc


def select_box (img, x, y, dx, dy) :
	return img,x,y,dx,dy

class SelectBoxWidget(NodeWidget,ScalableLabel) :
	"""Mouse selection of a box in a pixmap
	"""
	def __init__ (self, node, parent = None) :
		ScalableLabel.__init__(self,parent)
		NodeWidget.__init__(self, node)

		self.setMouseTracking(True)

		self._mouse_ini_pos = None
		self._select_rect = QRect()

		self.notify(node,("input_modified",0) )

	def notify(self, sender, event):
		"""Notification sent by node
		"""
		if event[0] == 'caption_modified' :
			self.window().setWindowTitle(event[1])

		elif event[0] == 'input_modified' :
			if event[1] == 0 :
				img = self.node.get_input(0)
				if img is None :
					self.setText("no pix")
				else :
					if len(img.shape) in (3,4):
						self.setPixmap(to_pix(img[:,:,0].copy()) )
					else:
						self.setPixmap(to_pix(img) )
#			if event[1] == 1 :
#				col = self.node.get_input(1)
#				self._col_picked_lab.pixmap().fill(QColor(*col[:3]) )

		self.update()

	def selected_rect (self, pos) :
		if self._mouse_ini_pos is None :
			return None

		x1 = self._mouse_ini_pos.x()
		y1 = self._mouse_ini_pos.y()
		x2 = pos.x()
		y2 = pos.y()
		rect = QRect(min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1) )
		return rect

	def mousePressEvent (self, event) :
		self._mouse_ini_pos = event.pos()

	def mouseReleaseEvent (self, event) :
		if self._mouse_ini_pos is not None :
			if self._mouse_ini_pos == event.pos() :
				self._select_rect = QRect()
				self.update()
			else :
				rect = self.selected_rect(event.pos() )
				self._mouse_ini_pos = None

				if rect is not None :
					x,y = self.pixmap_coordinates(rect.x(),rect.y() )
					w,h = self.pixmap_coordinates(rect.width(),rect.height() )
					self.node.set_input(1,x)
					self.node.set_input(2,y)
					self.node.set_input(3,w)
					self.node.set_input(4,h)

	def mouseMoveEvent (self, event) :
		if self._mouse_ini_pos is not None :
			old_rect = QRect(self._select_rect.topLeft(),
			                 self._select_rect.size() + QSize(1,1) )
			self._select_rect = self.selected_rect(event.pos() )
			update_rect = QRect(self._select_rect.topLeft(),
			                 self._select_rect.size() + QSize(1,1) ) | old_rect
			self.update(update_rect)

	def paintEvent (self, event) :
		ScalableLabel.paintEvent(self,event)

		if self._select_rect is not None :
			painter = QPainter(self)
			pen = QPen(QColor(255,255,255) )
			pen.setDashPattern([5,5])
			painter.setPen(pen)
			painter.drawRect(self._select_rect)
			pen.setColor(QColor(0,0,0) )
			pen.setDashOffset(5.)
			painter.setPen(pen)
			painter.drawRect(self._select_rect)
			painter.end()


