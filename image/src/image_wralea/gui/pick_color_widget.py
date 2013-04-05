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
load_local(QtCore,'QObject,SIGNAL')
load_local(QtGui,"""QWidget,QLabel,QPixmap,
                         QHBoxLayout,QVBoxLayout,
                         QColor,QCursor,QApplication""")
from openalea.core import Node
from openalea.visualea.node_widget import NodeWidget
from openalea.image.gui.all import to_pix,ScalableLabel
from openalea.image.gui     import icons_rc

def pick_color (img, col) :
	return img,col

class InteractiveScalableLabel(ScalableLabel) :
	"""Add mouse interaction to a scalable label
	"""
	def __init__ (self, parent = None) :
		ScalableLabel.__init__(self,parent)
		self.setMouseTracking(True)

		self._last_mouse_pos = None

	def mouseDoubleClickEvent (self, event) :
		self._last_mouse_pos = None
		self.emit(SIGNAL("mouse_double_click"),event)

	def mousePressEvent (self, event) :
		self._last_mouse_pos = event.pos()

	def mouseReleaseEvent (self, event) :
		if self._last_mouse_pos is not None :
			if self._last_mouse_pos == event.pos() :
				self.emit(SIGNAL("mouse_click"),event)

			self._last_mouse_pos = None

	def mouseMoveEvent (self, event) :
		if self._last_mouse_pos is None :
			self.emit(SIGNAL("mouse_move"),event)


class PickColorWidget(NodeWidget,QWidget) :
	"""
	Node widget to pick a color in an image
	"""

	def __init__(self, node, parent) :
		"""
		"""
		QWidget.__init__(self, parent)
		NodeWidget.__init__(self, node)

		self._img_lab = InteractiveScalableLabel()
		self._img_lab.setCursor(QCursor(QPixmap(":cursor/pick.png"),9,10) )

		self._col_picked_lab = QLabel("col")
		self._col_picked_lab.setPixmap(QPixmap(32,32) )
		self._col_picked_lab.pixmap().fill(QColor(0,0,0) )

		self._col_current_lab = QLabel("col")
		self._col_current_lab.setPixmap(QPixmap(32,32) )
		self._col_current_lab.pixmap().fill(QColor(0,0,0) )

		self._h_layout = QHBoxLayout()
		self._v_layout = QVBoxLayout()

		self._v_layout.addWidget(self._col_picked_lab)
		self._v_layout.addWidget(self._col_current_lab)
		self._v_layout.addStretch(5)

		self._h_layout.addLayout(self._v_layout)
		self._h_layout.addWidget(self._img_lab,5)

		self.setLayout(self._h_layout)

		self.notify(node,("caption_modified",node.get_caption() ) )
		self.notify(node,("input_modified",0) )
		self.notify(node,("input_modified",1) )

		QObject.connect(self._img_lab,SIGNAL("mouse_click"),self.mouse_click)
		QObject.connect(self._img_lab,SIGNAL("mouse_move"),self.mouse_move)

	def notify(self, sender, event):
		"""Notification sent by node
		"""
		if event[0] == 'caption_modified' :
			self.window().setWindowTitle(event[1])

		elif event[0] == 'input_modified' :
			if event[1] == 0 :
				img = self.node.get_input(0)
				if img is None :
					self._img_lab.setText("no pix")
				else :
					self._img_lab.setPixmap(to_pix(img) )
			if event[1] == 1 :
				col = self.node.get_input(1)
				self._col_picked_lab.pixmap().fill(QColor(*col[:3]) )

		self.update()

	def mouse_click (self, event) :
		img = self.node.get_input(0)
		if img is not None :
			j,i = self._img_lab.pixmap_coordinates(event.x(),event.y() )
			col = tuple(img[i,j])
			print "color",col
			self.node.set_input(1,col)
			self._col_picked_lab.pixmap().fill(QColor(*col[:3]) )
			self._col_picked_lab.update()

	def mouse_move (self, event) :
		img = self.node.get_input(0)
		if img is not None :
			j,i = self._img_lab.pixmap_coordinates(event.x(),event.y() )
			col = img[i,j]
			self._col_current_lab.pixmap().fill(QColor(*col[:3]) )
			self._col_current_lab.update()



