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

from PyQt4.QtCore import QObject,SIGNAL
from PyQt4.QtGui import QWidget,QLabel,QPixmap,QHBoxLayout,QVBoxLayout,QColor
from openalea.core import Node
from openalea.visualea.node_widget import NodeWidget
from openalea.image.gui import to_pix,ScalableLabel

def pick_color (img, col) :
	return col,

class PickColorWidget(NodeWidget,QWidget) :
	"""
	Node widget to pick a color in an image
	"""
	
	def __init__(self, node, parent) :
		"""
		"""
		QWidget.__init__(self, parent)
		NodeWidget.__init__(self, node)
		
		self._img_lab = ScalableLabel()
		self._col_lab = QLabel("col")
		self._col_lab.setPixmap(QPixmap(32,32) )
		self._col_lab.pixmap().fill(QColor(0,0,0) )
		
		self._h_layout = QHBoxLayout()
		self._v_layout = QVBoxLayout()
		
		self._v_layout.addWidget(self._col_lab)
		self._v_layout.addStretch(5)
		
		self._h_layout.addLayout(self._v_layout)
		self._h_layout.addWidget(self._img_lab)
		
		self.setLayout(self._h_layout)
		
		self.notify(node,("caption_modified",node.get_caption() ) )
		self.notify(node,("input_modified",0) )
		self.notify(node,("input_modified",1) )
		
		QObject.connect(self._img_lab,SIGNAL("mouse_press"),self.mouse_press)
	
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
				self._col_lab.pixmap().fill(QColor(*col[:3]) )
		
		self.update()
	
	def mouse_press (self, event) :
		img = self.node.get_input(0)
		if img is not None :
			i,j = self._img_lab.pixmap_coordinates(event.x(),event.y() )
			col = img[i,j]
			print "color",col
			self.node.set_input(1,col)
			self._col_lab.pixmap().fill(QColor(*col[:3]) )
	


