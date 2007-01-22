# -*- python -*-
#
#       OpenAlea.Core.UI: OpenAlea Interfaces 
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
This module define User Interfaces of Node and DataFlow
"""

__license__= "Cecill-C"
__revision__=" $Id: observer.py 229 2007-01-22 10:17:17Z tyvokka-toufou $ "

###############################################################################

class Node (object) :
	"""
	Base class for all Nodes.
	A Node is a callable object with typed inputs and outputs.
	"""
	def __init__ (self) :
		raise RuntimeError()
	
	##########################################################
	#
	#		Readable Concept
	#
	##########################################################
	def nb_inputs (self) :
		"""
		return number of input ports
		"""
		raise RuntimeError()
	
	def nb_outputs (self) :
		"""
		return number of output ports
		"""
		raise RuntimeError()
	
	def inputs (self) :
		"""
		iterable on input_buffer values
		"""
		raise RuntimeError()
	
	def outputs (self) :
		"""
		iterable on output_buffer values
		"""
		raise RuntimeError()
	
	def input (self, port_nb=None, port_name=None) :
		"""
		return value associated with a given port in input buffer
		"""
		raise RuntimeError()
	
	def output (self, port_nb=None, port_name=None) :
		"""
		return value associated with a given port in output buffer
		"""
		raise RuntimeError()
	
	##########################################################
	#
	#		Writable Concept
	#
	##########################################################
	def set_input (self, value, port_nb=None, port_name=None) :
		"""
		set value into input port given either by an id or a name
		"""
		raise RuntimeError()
	
	def set_output (self, value, port_nb=None, port_name=None) :
		"""
		set value into output port given either by an id or a name
		"""
		raise RuntimeError()
	
	##########################################################
	#
	#		Mutable Concept
	#
	##########################################################
	def add_input (self, name, interface=None) :
		"""
		add a new port at the end of the input buffer
		"""
		raise RuntimeError()
	
	def add_output (self, name, interface=None) :
		"""
		add a new port at the end of the output buffer
		"""
		raise RuntimeError()
	
	##########################################################
	#
	#		Evaluation Concept
	#
	##########################################################
	def __call__ (self, input_values) :
		""" Call function. Must be overriden """
		
		raise RuntimeError('Node function not implemented.')
	
	# Functions used by the node evaluator
	def eval (self) :
		"""
		Evaluate the node by calling __call__
		with values stored into input_buffer
		write result into output_buffer
		"""
		raise RuntimeError()

class DataFlow (object) :
	"""
	A DataFlow is a container of nodes and link between nodes
	"""
	def __init__ (self) :
		raise RuntimeError()
	
	###########################################################
	#
	#		Node List Concept
	#
	###########################################################
	def nodes (self) :
		"""
		iterable on all nodes id
		"""
		raise RuntimeError()
	
	def node (self, nid) :
		"""
		return node associated with the given id
		"""
		raise RuntimeError()
	
	###########################################################
	#
	#		Link List Concept
	#
	###########################################################
	def links (self) :
		"""
		iterable on all link id
		"""
		raise RuntimeError()
	
	###########################################################
	#
	#		Mutable Concept
	#
	###########################################################
	def add_node (self, node, nid=None) :
		"""
		add a new node to the dataflow with a given id
		if nid is None, choose a free id
		return node id
		"""
		raise RuntimeError()
	
	def remove_node (self, nid) :
		"""
		remove a node specified by its id from the dataflow
		"""
		raise RuntimeError()
	
	def connect (self, source_id, source_port_nb, target_id, target_port_nb) :
		"""
		connect source_port_nb outport of node source_id to
		target_port_nb inport of node target_id
		"""
		raise RuntimeError()
	
	def disconnect (self, eid) :
		"""
		remove a connection between two nodes
		"""
		raise RuntimeError()
	
	##########################################################
	#
	#		Evaluation Concept
	#
	##########################################################
	def evaluate_nodes (self, nid_list=None) :
		"""
		Evaluate nodes specified by their id,
		or the whole dataflow if nid_list is None
		"""
		raise RuntimeError()
	
	def run (self) :
		"""
		Evaluate the whole dataflow
		"""
		raise RuntimeError()



