# -*- python -*-
# -*- coding: latin-1 -*-
#
#       PropertyGraph : graph package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
#

__doc__="""
This module provide a set of concepts to add properties to graph elements
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

class IPropertyGraph (object):
	"""
	Directed graph with properties associated with edges and vertices
	"""
	def vertex_property (self, property_name) :
		raise NotImplementedError
	
	def edge_property (self, property_name) :
		raise NotImplementedError
	###########################################################
	#
	#		mutable property concept
	#
	###########################################################
	def add_vertex_property (self, property_name) :
		raise NotImplementedError
	
	def remove_vertex_property (self, property_name) :
		raise NotImplementedError
	
	def add_edge_property (self, property_name) :
		raise NotImplementedError
	
	def remove_edge_property (self, property_name) :
		raise NotImplementedError
