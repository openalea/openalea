# -*- python -*-
# -*- coding: latin-1 -*-
#
#       PortGraph : graph package
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

class IPortGraph (object):
	"""
	Directed graph with connections between in_ports
	of vertices and out_port of vertices
	"""
	####################################################
	#
	#		edge port view
	#
	####################################################
	def source_port (self, eid) :
		raise NotImplementedError
	
	def target_port (self, eid) :
		raise NotImplementedError
	####################################################
	#
	#		vertex port view
	#
	####################################################
	def out_ports (self, vid=None) :
		raise NotImplementedError
	
	def in_ports (self, vid=None) :
		raise NotImplementedError
	
	def ports (self, vid=None) :
		raise NotImplementedError
	####################################################
	#
	#		port view
	#
	####################################################
	def is_in_port (self, pid) :
		raise NotImplementedError
	
	def is_out_port (self, pid) :
		raise NotImplementedError
	
	def vertex (self, pid) :
		raise NotImplementedError
	
	def port_neighbors (self, pid) :
		raise NotImplementedError
	
	def port_edges (self, pid) :
		raise NotImplementedError
	####################################################
	#
	#		limited number of connections
	#
	####################################################
	def capacity (self, pid) :
		raise NotImplementedError
	
	def set_capacity (self, pid, capacity) :
		raise NotImplementedError
	####################################################
	#
	#		local port concept
	#
	####################################################
	def port (self, pid) :
		raise NotImplementedError
	
	def out_port (self, vid, local_pid) :
		raise NotImplementedError
	
	def in_port (self, vid, local_pid) :
		raise NotImplementedError
	#####################################################
	#
	#		mutable concept
	#
	#####################################################
	def add_in_port (self, vid, local_pid, pid=None) :
		raise NotImplementedError
	
	def add_out_port (self, vid, local_pid, pid=None) :
		raise NotImplementedError
	
	def remove_port (self, pid) :
		raise NotImplementedError
	
	def connect (self, source_pid, target_pid, eid=None) :
		raise NotImplementedError
	
	def disconnect (self, eid) :
		raise NotImplementedError
