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
""" openalea.image """

__revision__ = " $Id: __wralea__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from PyQt4.QtCore import QObject,Qt,SIGNAL,QTimer
from PyQt4.QtGui import (QMainWindow,QLabel,QToolBar,
                         QAction,QIcon,QSlider,
                         QPixmap,QSpinBox)

import movie_rc

def clone_action (ref_action, clone) :
	clone.setText(ref_action.text() )
	clone.setIcon(ref_action.icon() )
	clone.setToolTip(ref_action.toolTip() )
	clone.setShortcuts(ref_action.shortcuts() )

class FrameAnimator (QMainWindow) :
	"""Animate a list of frames
	"""
	def __init__ (self, parent = None) :
		QMainWindow.__init__(self,parent)
		
		self._pix = []
		self._current_frame = None
		self._timer = QTimer()
		self._timer.setInterval(40)
		
		self._view = QLabel()
		self.setCentralWidget(self._view)
		
		QObject.connect(self._timer,SIGNAL("timeout()"),self.step)
		
		#UI
		self._menu = self.menuBar().addMenu("anim")
		self._action_bar = self.addToolBar("movie")
		self._slider_bar = QToolBar("slider")
		self.addToolBar(Qt.BottomToolBarArea,self._slider_bar)
		
		#close
		self._action_close = QAction("close",self)
		self._action_close.setShortcut("Escape")
		self._menu.addAction(self._action_close)
		QObject.connect(self._action_close,
		                SIGNAL("triggered(bool)"),
		                self.close_window)
		
		self._menu.addSeparator()
		
		#stop play/pause step
		self._action_reinit = QAction("reinit",self)
		self._action_reinit.setIcon(QIcon(":image/stop.png") )
		self._action_bar.addAction(self._action_reinit)
		QObject.connect(self._action_reinit,
		                SIGNAL("triggered(bool)"),
		                self.reinit)
		self._menu.addAction(self._action_reinit)
		
		self._action_play = QAction("play",self)
		self._action_play.setIcon(QIcon(":image/play.png") )
		self._action_play.setShortcut("Space")
		
		self._action_pause = QAction("pause",self)
		self._action_pause.setIcon(QIcon(":image/pause.png") )
		self._action_pause.setShortcut("Space")
		
		self._toggle_running = QAction("toggle",self)
		QObject.connect(self._toggle_running,
		                SIGNAL("triggered(bool)"),
		                self.toggle_running)
		self._action_bar.addAction(self._toggle_running)
		self._menu.addAction(self._toggle_running)
		
		self._action_step = QAction("step",self)
		self._action_step.setIcon(QIcon(":image/step.png") )
		self._action_step.setShortcut("Ctrl+Space")
		QObject.connect(self._action_step,
		                SIGNAL("triggered(bool)"),
		                self.step)
		self._action_bar.addAction(self._action_step)
		self._menu.addAction(self._action_step)
		
		#loop
		self._action_bar.addSeparator()
		self._menu.addSeparator()
		
		self._action_loop = self._action_bar.addAction("loop")
		self._action_loop.setCheckable(True)
		self._action_loop.setChecked(True)
		self._action_loop.setIcon(QIcon(":image/loop.png") )
		self._menu.addAction(self._action_loop)
		
		self._fps_edit = QSpinBox()
		self._action_bar.addWidget(self._fps_edit)
		self._fps_edit.setRange(1,99)
		self._fps_edit.setSuffix(" fps")
		self._fps_edit.setValue(25)
		
		QObject.connect(self._fps_edit,
		                SIGNAL("valueChanged(int)"),
		                self.fps_changed)
		
		#slider
		self._frame_slider = QSlider(Qt.Horizontal)
		self._slider_bar.addWidget(self._frame_slider)
		QObject.connect(self._frame_slider,
		                SIGNAL("sliderMoved(int)"),
		                self.frame_changed)
		
		#init GUI
		self.pause()
		self.set_frames([])
	
	def close_window (self) :
		self.pause()
		self.window().close()
	
	def set_current_frame (self, ind) :
		"""Set the index of the frame to be displayed
		"""
		self._current_frame = ind
		self._frame_slider.setValue(ind)
	
	def update_pix (self) :
		"""Change currently displayed frame
		"""
		if self._current_frame is not None :
			self._view.setPixmap(self._pix[self._current_frame])
	
	def set_frames (self, frames) :
		"""Set frame names
		
		:Parameters:
		 - `frames` (list of str) - list of frame path
		"""
		self._pix = [QPixmap(name) for name in frames]
		
		if len(self._pix) == 0 :
			self._current_frame = None
			self._frame_slider.setEnabled(False)
			self._action_bar.setEnabled(False)
			self._menu.setEnabled(False)
		else :
			self._frame_slider.setRange(0,len(self._pix) - 1)
			self._frame_slider.setEnabled(True)
			self._action_bar.setEnabled(True)
			self._menu.setEnabled(True)
			
			if self._current_frame is None :
				self._current_frame = 0
			else :
				self._current_frame = min(self._current_frame,len(self._pix) )
		
		self.update_pix()
	
	############################################
	#
	#	animate
	#
	############################################
	def fps_changed (self, fps) :
		self._timer.setInterval(int(1000. / fps) )
	
	def frame_changed (self, ind) :
		self.set_current_frame(ind)
		self.update_pix()
	
	def reinit (self) :
		self.pause()
		self.set_current_frame(0)
		self.update_pix()
	
	def step (self) :
		next_frame = self._current_frame + 1
		if next_frame == len(self._pix) :
			if self._action_loop.isChecked() :
				self.set_current_frame(0)
				self.update_pix()
			else :
				self.pause()
		else :
			self.set_current_frame(next_frame)
			self.update_pix()
	
	def toggle_running (self) :
		if self._timer.isActive() :
			self.pause()
		else :
			self.play()
	
	def play (self) :
		self._action_step.setEnabled(False)
		self._fps_edit.setEnabled(False)
		clone_action(self._action_pause,self._toggle_running)
		self._timer.start()
	
	def pause (self) :
		self._timer.stop()
		self._action_step.setEnabled(True)
		self._fps_edit.setEnabled(True)
		clone_action(self._action_play,self._toggle_running)
	






