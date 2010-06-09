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
This module provide a simple viewer to display 3D stacks
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

__all__ = ["display","SlideViewer"]

from ..serial.inrimage import read_inrimage
from PyQt4.QtCore import Qt,QObject,SIGNAL
from PyQt4.QtGui import (QApplication,QLabel,QMainWindow,
                        QSlider,QToolBar)
from palette import palette_factory
from pixmap_view import PixmapStackView,ScalableLabel

from slide_viewer_ui import Ui_MainWindow

class SlideViewer (QMainWindow) :
	"""Display each image in a stack using a slider
	"""
	def __init__ (self) :
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self._im_view = PixmapStackView()
		self._label = ScalableLabel()
		self.setCentralWidget(self._label)
		
		#slider
		self._bot_toolbar = QToolBar("slider")
		
		self._img_slider = QSlider(Qt.Horizontal)
		self._img_slider.setEnabled(False)
		QObject.connect(self._img_slider,
		                SIGNAL("valueChanged(int)"),
		                self.slice_changed)
		
		self._bot_toolbar.addWidget(self._img_slider)
		self.addToolBar(Qt.BottomToolBarArea,self._bot_toolbar)
		
		
		#statusbar
		self._lab_coord = QLabel("coords:")
		self._lab_xcoord = QLabel("% 4d" % 0)
		self._lab_ycoord = QLabel("% 4d" % 0)
		self._lab_zcoord = QLabel("% 4d" % 0)
		self._lab_intens = QLabel("intens: None")
		
		self.ui.statusbar.addPermanentWidget(self._lab_coord)
		self.ui.statusbar.addPermanentWidget(self._lab_xcoord)
		self.ui.statusbar.addPermanentWidget(self._lab_ycoord)
		self.ui.statusbar.addPermanentWidget(self._lab_zcoord)
		self.ui.statusbar.addPermanentWidget(self._lab_intens)
		
		#mouse handling
		self._label.setMouseTracking(True)
		self._last_mouse_x = 0
		self._last_mouse_y = 0
		
		#connections
		QObject.connect(self.ui.action_close,
		                SIGNAL("triggered(bool)"),
		                self.close)
		
		QObject.connect(self.ui.action_snapshot,
		                SIGNAL("triggered(bool)"),
		                self.snapshot)
		
		QObject.connect(self.ui.action_rotate_left,
		                SIGNAL("triggered(bool)"),
		                self.rotate_left)
		
		QObject.connect(self.ui.action_rotate_right,
		                SIGNAL("triggered(bool)"),
		                self.rotate_right)
		
		QObject.connect(self._label,
		                SIGNAL("mouse_press"),
		                self.mouse_pressed)
		
		QObject.connect(self._label,
		                SIGNAL("mouse_move"),
		                self.mouse_pressed)
	
	def set_image (self, img) :
		self._im_view.set_image(img)
		
		self._img_slider.setRange(0,self._im_view.nb_slices() - 1)
		self._img_slider.setEnabled(True)
		self.slice_changed(self._img_slider.value() )
	
	def set_palette (self, palette) :
		self._im_view.set_palette(palette)
	
	def fill_infos (self) :
		x,y = self._label.pixmap_coordinates(self._last_mouse_x,
		                                     self._last_mouse_y)
		
		img = self._im_view.image()
		if img is not None :
			i,j,k = self._im_view.data_coordinates(x,y)
			self._lab_xcoord.setText("% 4d" % i)
			self._lab_ycoord.setText("% 4d" % j)
			self._lab_zcoord.setText("% 4d" % k)
			
			imax,jmax,kmax = img.shape
			if 0 <= i < imax and 0 <= j < jmax and 0 <= k < kmax :
				self._lab_intens.setText("intens: % 3d" % img[i,j,k])
			else :
				self._lab_intens.setText("intens: None")
	
	def slice_changed (self, ind) :
		self._im_view.set_current_slice(ind)
		pix = self._im_view.pixmap()
		if pix is not None :
			self._label.setPixmap(pix)
		self.fill_infos()
	
	def snapshot (self) :
		"""write the current image
		"""
		pix = self._im_view.pixmap()
		if pix is not None :
			pix.save("slice%.4d.png" % self._img_slider.value() )
	
	def wheelEvent (self, event) :
		inc = event.delta() / 8 / 15
		self._img_slider.setValue(self._img_slider.value() + inc)
	
	def rotate_left (self) :
		self._im_view.rotate(-1)
		pix = self._im_view.pixmap()
		if pix is not None :
			self._label.setPixmap(pix)
	
	def rotate_right (self) :
		self._im_view.rotate(1)
		pix = self._im_view.pixmap()
		if pix is not None :
			self._label.setPixmap(pix)
	
	def mouse_pressed (self, event) :
		self._last_mouse_x = event.x()
		self._last_mouse_y = event.y()
		self.fill_infos()

def display (filenames, palette = "grayscale", color_index_max = None) :
	#test for list of images to display
	if isinstance(filenames,str) :
		filenames = [filenames]
	
	qapp = QApplication.instance()
	if qapp is None :
		qapp = QApplication([])
	
	w_list = []
	for fname in filenames :
		img = read_inrimage(fname)
		
		w = SlideViewer()
		
		if color_index_max is None :
			cmax = img.max()
		else :
			cmax = color_index_max
		
		palette = palette_factory(palette,cmax)
		
		w.set_palette(palette)
		w.set_image(img)
		
		w.show()
		w.setWindowTitle(fname)
		w_list.append(w)

	qapp.exec_()


