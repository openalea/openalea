# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Library 
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
This module provide some usefull nodes
GUINodes implementations must be subclassed in a GUI application to provide some
widget for each node
"""

__license__= "Cecill-C"
__revision__=" $Id: core.py 268 2007-01-22 09:43:10Z chopard $ "

###############################################################################
from core import Node
from gui import GUINode

##############################################################
#
#		empty node
#
##############################################################
class EmptyNode (Node) :
	"""
	node that do nothing and report values from input buffer to ouput buffer
	"""
	name="Empty"
	description="""Repport values directly from input to output"""
	
	def __init__ (self) :
		Node.__init__(self)
		self.add_input("in")
		self.add_output("out")
	
	def __call__ (self, input_values) :
		return input_values

class GUIEmptyNode (GUINode) :
	
	def __init__ (self) :
		GUINode.__init__(self,EmptyNode())

##############################################################
#
#		dataflow node
#
##############################################################
class DataFlowNode (Node) :
	"""
	node whose value is evaluated
	using a data_flow
	"""
	name="dataflow"
	description="""Node that use an inside dataflow to evaluate itself"""
	
	def __init__ (self) :
		Node.__init__(self)
		d=DataFlow()
		self._in_node=d.add_node(EmptyNode())
		self._out_node=d.add_node(EmptyNode())
		self._dataflow=d
	
	def dataflow (self) :
		return self._dataflow
	
	def __call__ (self, input_values) :
		"""
		evaluate the whole inside data_flow to find node value
		"""
		in_node.in_port.set_values(input_values)
		self._dataflow.run()
		return out_node.out_port
	
	def in_port (self) :
		"""
		return id of an in port to connect in_port
		of the DataFlowNode to an internal node
		"""
		return self._in_node
	
	def out_port (self) :
		"""
		return id of an out port to connect out_port
		of the DataFlowNode to an internal node
		"""
		return self._out_node

class GUIDataFlowNode (GUINode) :
	def __init__ (self) :
		GUINode.__init__(self,DataFlowNode())
	
	def dataflow (self) :
		return self.node().dataflow()

##############################################################
#
#		func node
#
##############################################################
class FuncNode (Node) :
	"""
	this node execute a given function
	"""
	name="func"
	description="""This node execute a user defined function"""
	
	def __init__ (self, func) :
		Node.__init__(self)
		self._func=func
	
	def __call__ (self,input_values) :
		return (self._func(input_values),)

class GUIFuncNode (GUINode) :
	def __init__ (self,func) :
		UINode.__init__(self,FuncNode(func))
	
	def __call__ (self,input_values) :
		return self.node()(input_values)

##############################################################
#
#		data node
#
##############################################################
class DataNode (Node) :
	"""
	node able to store a data of any kind
	"""
	name="data"
	description="""This node store a value"""
	
	def __init__ (self, default_value) :
		Node.__init__(self)
		self.add_output("out")
		self._data=default_value
	
	def __call__ (self, input_values) :
		return (self._data,)
	
	def data (self) :
		return self._data

class GUIDataNode (GUINode) :
	
	def __init__ (self, default_value) :
		UINode.__init__(self,DataNode(default_value))
	
	def data (self) :
		return self.node()._data


