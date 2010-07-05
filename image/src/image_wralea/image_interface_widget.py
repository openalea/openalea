# -*- python -*-
#
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA  
#
#       File author(s): Chopard
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Declaration of IImage interface widget
"""

__license__ = "Cecill-C"
__revision__ = " $Id: interface.py 2245 2010-02-08 17:11:34Z cokelaer $"

from openalea.core.observer import lock_notify
from openalea.core.interface import IInterfaceWidget,make_metaclass
from openalea.image.gui import to_pix,ScalableLabel
from image_interface import IImage

class IImageWidget (IInterfaceWidget, ScalableLabel) :
	"""Interface for images expressed as array of triplet of values
	"""
	__interface__ = IImage
	__metaclass__ = make_metaclass()
	
	def __init__(self, node, parent, parameter_str, interface):
		"""Constructor
		
		:Parameters:
		 - `node` (Node) - node that own the widget
		 - `parent` (QWidget) - parent widget
		 - `parameter_str` (str) - the parameter key the widget is associated to
		 - `interface` (Ismth) - instance of interface object
		"""
		ScalableLabel.__init__(self,parent)
		IInterfaceWidget.__init__(self,node,parent,parameter_str,interface)
		self.setMinimumSize(100,50)
		
		self.notify(node,("input_modified",self.param_str) )
	
	@lock_notify
	def notify(self, sender, event):
		"""Notification sent by node
		"""
		if event[0] == "input_modified" :
			img = self.node.get_input(self.param_str)
			if img is None :
				self.setText("no pix")
			else :
				self.setPixmap(to_pix(img) )
			
			self.update()



