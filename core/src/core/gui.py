# -*- python -*-
#
#       OpenAlea.Core: OpenAlea GUI 
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <theveny@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module give a standard implementation of GUINode interface
"""

__license__= "Cecill-C"
__revision__=" $Id: observer.py 229 2007-01-22 10:17:17Z tyvokka-toufou $ "

###############################################################################
import UI

class GUINode (UI.GUINode) :
	"""
	Standard implementation of GUINode interface
	"""
	def __init__ (self, node) :
		self._node=node
	
	def node (self) :
		"""
		return computation node associated with this GUI
		"""
		return node
	
	def title (self) :
		"""
		return a relevant name for ther node
		"""
		return self._node.name
	
	def string_representation (self) :
		"""
		return a small string to describe the node
		used for tooltip
		"""
		return self._node.description
	
	def edit_representation (self) :
		"""
		return the widget associated to the node
		and used to modify node properties
		"""
		return None
	
	def thumbnail_representation (self) :
		"""
		return the small widget associated to the node
		used to represent the node in the dataflow
		"""
		return None
	
	def icon_representation (self) :
		"""
		return a small visual representation (an icon)
		used to summarize the node
		"""
		return None
	
	def color (self, interface) :
		"""
		return a color for a special interface type
		"""
		return None
