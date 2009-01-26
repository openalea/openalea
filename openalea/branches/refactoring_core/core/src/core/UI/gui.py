# -*- python -*-
#
#       OpenAlea.GUI: OpenAlea Interfaces 
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
This module define the User Interface of a graphical representation of Node (GUINode)
"""

__license__= "Cecill-C"
__revision__=" $Id: observer.py 229 2007-01-22 10:17:17Z tyvokka-toufou $ "

###############################################################################

class GUINode (object) :
	"""
	extension of node concept that provide widgets
	in fact, provide all graphical informations relevant to draw
	a node widget in the GUI.
	"""
	def __init__ (self) :
		raise RuntimeError()
	
	def node (self) :
		"""
		return computation node associated with this GUI
		"""
		raise RuntimeError()
	
	def title (self) :
		"""
		return a relevant name for ther node
		"""
		raise RuntimeError()
	
	def string_representation (self) :
		"""
		return a small string to describe the node
		used for tooltip
		"""
		raise RuntimeError()
	
	def edit_representation (self) :
		"""
		return the widget associated to the node
		and used to modify node properties
		"""
		raise RuntimeError()
	
	def thumbnail_representation (self) :
		"""
		return the small widget associated to the node
		used to represent the node in the dataflow
		"""
		raise RuntimeError()
	
	def icon_representation (self) :
		"""
		return a small visual representation (an icon)
		used to summarize the node
		"""
		raise RuntimeError()
	
	def color (self, interface) :
		"""
		return a color for a special interface type
		"""
		raise RuntimeError()
