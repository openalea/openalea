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

__revision__ = " $Id: __wralea__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from openalea.visualea.node_widget import NodeWidget
from animator import FrameAnimator

def animator_functor (frames) :
	return frames,

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
		self.notify(node,("input_modified",0) )
	
	def notify(self, sender, event):
		"""Notification sent by node
		"""
		if event[0] == 'caption_modified' :
			self.window().setWindowTitle(event[1])
		
		elif event[0] == 'input_modified' :
			self.set_frames(self.node.get_input(0) )

