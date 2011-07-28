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

from openalea.core import Node
from openalea.visualea.node_widget import NodeWidget
from openalea.image.gui.animator import FrameAnimator

class AnimatorNode (Node) :
	def __init__(self, *args, **kwargs) :
		Node.__init__(self, *args, **kwargs)
		self._ini_frames = None
		self._frames = []

	def __call__ (self, inputs) :
		frames,last_frame,fps,loop,reinit = inputs

		if reinit or self._ini_frames is None:
			self.set_input(4,False)
			self._ini_frames = frames
			self._frames = list(frames)

		if last_frame != "" :
			self._frames.append(last_frame)

		return self._frames,

#	def notify(self, sender, event):
#		"""Notification sent by node
#		"""
#		print event

class AnimatorWidget(NodeWidget,FrameAnimator) :
	"""
	Node Widget associated to a frame animator
	"""

	def __init__(self, node, parent) :
		"""
		"""
		FrameAnimator.__init__(self, parent)
		NodeWidget.__init__(self, node)

		self.notify(node,("caption_modified",node.get_caption() ) )

	def showEvent (self, event) :
		if len(self._frames) == 0 :
			self.set_frames(self.node._frames)

		self.notify(self.node,("input_modified",2) )
		self.notify(self.node,("input_modified",3) )

		FrameAnimator.showEvent(self,event)

	def notify(self, sender, event):
		"""Notification sent by node
		"""
		if event[0] == 'caption_modified' :
			self.window().setWindowTitle(event[1])

		elif event[0] == 'input_modified' :
			if event[1] == 0 :
				self.set_frames(self.node.get_input(0) )
			elif event[1] == 1 :
				name = self.node.get_input(1)
				if name != "" :
					self.append_frame(name)
			elif event[1] == 2 :
				self.set_fps(self.node.get_input(2) )
			elif event[1] == 3 :
				self.set_loop(self.node.get_input(3) )
			elif event[1] == 4 :
				print "reinit",self.node.get_input(4)

	def fps_changed (self, fps) :
		print "fps",fps
		FrameAnimator.fps_changed(self,fps)
		self.node.set_input(2,fps)

	def loop_changed (self, loop) :
		FrameAnimator.loop_changed(self,loop)
		self.node.set_input(3,loop)

	def clear_frames (self) :
		FrameAnimator.clear_frames(self)
		self.node.set_input(4,True)



