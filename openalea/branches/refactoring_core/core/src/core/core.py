# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core 
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
This module give a standard implementation of Node and DataFlow interfaces
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

###############################################################################
from graph import Graph
import UI

class NodePort (object) :
	"""
	named buffer used to store values in nodes
	"""
	def __init__ (self, name, interface=None) :
		self._name=name
		self._interface=interface
		self._value=None
	
	def name (self) :
		return self._name
	
	def value (self) :
		return self._value
	
	def set_value (self, val) :
		self._value=val

class Node (UI.Node) :
	"""
	Implementation of Node user Interface
	"""
	name="Node"
	description="""a usefull string description like a tooltip"""
	
	def __init__ (self) :
		self._input_buffer=[]
		self._output_buffer=[]
	
	##########################################################
	#
	#		Readable Concept
	#
	##########################################################
	def nb_inputs (self) :
		"""
		return number of input ports
		"""
		return len(self._input_buffer)
	
	def nb_outputs (self) :
		"""
		return number of output ports
		"""
		return len(self._output_buffer)
	
	def inputs (self) :
		"""
		iterable on input_buffer values
		"""
		for port in self._input_buffer :
			yield port.value()
	
	def outputs (self) :
		"""
		iterable on output_buffer values
		"""
		for port in self._output_buffer :
			yield port.value()
	
	def input (self, port_nb=None, port_name=None) :
		"""
		return value associated with a given port in input buffer
		"""
		if port_nb is not None :
			return self._input_buffer[port_nb].value()
		elif port_name is not None :
			for port in self._input_buffer :
				if port.name()==port_name :
					return port.value()
			raise InvalidNameException ("this node has no input port called %s" % port_name)
		else :
			raise UserWarning("you must specify either a port number or a port name")
	
	def output (self, port_nb=None, port_name=None) :
		"""
		return value associated with a given port in output buffer
		"""
		if port_nb is not None :
			return self._output_buffer[port_nb].value()
		elif port_name is not None :
			for port in self._output_buffer :
				if port.name()==port_name :
					return port.value()
			raise InvalidNameException ("this node has no output port called %s" % port_name)
		else :
			raise UserWarning("you must specify either a port number or a port name")
	
	##########################################################
	#
	#		Writable Concept
	#
	##########################################################
	def set_input (self, value, port_nb=None, port_name=None) :
		"""
		set value into input port given either by an id or a name
		"""
		if port_nb is not None :
			self._input_buffer[port_nb].set_value(value)
		elif port_name is not None :
			for port in self._input_buffer :
				if port.name()==port_name :
					port.set_value(value)
			raise InvalidNameException ("this node has no input port called %s" % port_name)
		else :
			raise UserWarning("you must specify either a port number or a port name")
	
	def set_output (self, value, port_nb=None, port_name=None) :
		"""
		set value into output port given either by an id or a name
		"""
		if port_nb is not None :
			self._output_buffer[port_nb].set_value(value)
		elif port_name is not None :
			for port in self._output_buffer :
				if port.name()==port_name :
					port.set_value(value)
			raise InvalidNameException ("this node has no output port called %s" % port_name)
		else :
			raise UserWarning("you must specify either a port number or a port name")
	
	##########################################################
	#
	#		Mutable Concept
	#
	##########################################################
	def add_input (self, name, interface=None) :
		"""
		add a new port at the end of the input buffer
		"""
		self._input_buffer.append(NodePort(name,interface))
	
	def add_output (self, name, interface=None) :
		"""
		add a new port at the end of the output buffer
		"""
		self._output_buffer.append(NodePort(name,interface))
	
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
		input_values=tuple(self.inputs())
		output_values=self.__call__(input_values)
		for ind,val in enumerate(output_values) :
			self.set_output(value=val,port_nb=ind)

class DataFlow (Graph,UI.DataFlow) :
	"""
	Implementation of DataFlow user Interface
	"""
	def __init__ (self) :
		Graph.__init__(self)
		self._nodes={}
		self._source_port_nb={}
		self._target_port_nb={}
	
	###########################################################
	#
	#		Node List Concept
	#
	###########################################################
	def nodes (self) :
		"""
		iterable on all nodes id
		"""
		return self.vertices()
	
	def node (self, nid) :
		"""
		return node associated with the given id
		"""
		return self._nodes[nid]
	
	###########################################################
	#
	#		Link List Concept
	#
	###########################################################
	def links (self) :
		"""
		iterable on all link id
		"""
		return self.edges()
	
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
		nid=self.add_vertex(nid)
		self._nodes[nid]=node
		return nid
	
	def remove_node (self, nid) :
		"""
		remove a node specified by its id from the dataflow
		"""
		self.remove_vertex(nid)
		del self._nodes[nid]
	
	def connect (self, source_id, source_port_nb, target_id, target_port_nb) :
		"""
		connect source_port_nb outport of node source_id to
		target_port_nb inport of node target_id
		"""
		eid=self.add_edge(edge=(source_id,target_id))
		self._source_port_nb[eid]=source_port_nb
		self._target_port_nb[eid]=target_port_nb
		return eid
	
	def disconnect (self, eid) :
		"""
		remove a connection between two nodes
		"""
		self.remove_edge(eid)
		del self._source_port_nb[eid]
		del self._target_port_nb[eid]
	
	##########################################################
	#
	#		Evaluation Concept
	#
	##########################################################
	def _leaves (self) :
		"""
		internal function to find all node without any output connection
		"""
		for vid in self.vertices() :
			if self.nb_out_neighbors(vid)==0 :
				yield vid
	
	def _evaluate_node (self, nid, already_evaluated) :
		"""
		internal function that evaluate a given node
		call eval on nodes connected to its entries if necessary
		"""
		node=self._nodes[nid]
		#compute all entries if necessary
		for eid in self.in_edges(nid) :
			vid=self.source(eid)
			if not already_evaluated[vid] :
				self._evaluate_node(vid,already_evaluated)
			value=self._nodes[vid].output(port_nb=self._source_port_nb[eid])
			node.set_input(value,port_nb=self._target_port_nb[eid])
		#evaluate the node
		node.eval()
		#modify dict of evaluated nodes
		already_evaluated[nid]=True
	
	def evaluate_nodes (self, nid_list=None) :
		"""
		Evaluate nodes specified by their id,
		or the whole dataflow if nid_list is None
		"""
		if nid_list is None :
			nid_list=list(self._leaves())
		
		#keep trace of already evaluated nodes
		evaluated={}
		for nid in self.vertices() : evaluated[nid]=False
		
		#try to evaluate the specified nodes
		for nid in nid_list :
			self._evaluate_node(nid,evaluated)
	
	def run (self) :
		"""
		Evaluate the whole dataflow
		"""
		return self.evaluate_nodes()


