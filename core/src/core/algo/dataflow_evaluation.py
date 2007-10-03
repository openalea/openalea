# -*- python -*-
# -*- coding: latin-1 -*-
#
#       Evaluator : openalea core package
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide an algorithm to evaluate a dataflow
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

import sys
import traceback as tb

class EvaluationException(Exception):
    
    def __init__(self,vid,node,exception,exc_info):
        Exception.__init__(self)
        self.vid = vid
        self.node = node
        self.exception = exception
        self.exc_info = exc_info
        

class AbstractEvaluation (object) :
    """ Abstract evaluation algorithm """
    
    def __init__ (self, dataflow) :
        self._dataflow = dataflow
        
    
    def eval(self, *args):
        raise NotImplementedError()
    
    
    def eval_vertex_code(self, vid):
        """ Evaluate the vertex vid. Can raise an exception if evaluation failed """
        node = self._dataflow.actor(vid)
        try:
            ret = node.eval()
            # When an exception is raised, a flag is set.
            # So we remove it when evaluation is ok.
            if hasattr(node,'raise_exception'):
                del node.raise_exception
                node.notify_listeners( ('data_modified',))
            return ret
        except EvaluationException, e:
            e.vid = vid
            e.node = node
            # When an exception is raised, a flag is set.
            node.raise_exception = True
            raise e
        except Exception, e:
            # When an exception is raised, a flag is set.
            node.raise_exception = True
            raise EvaluationException(vid,node,e,tb.format_tb(sys.exc_info()[2]))

        

class BrutEvaluation (AbstractEvaluation) :
	""" Basic evaluation algorithm """
	
	def __init__ (self, dataflow) :

		AbstractEvaluation.__init__(self, dataflow)
		# a property to specify if the node has already been evaluated
		self._evaluated = set()

	
	def eval_vertex (self, vid) :
		""" Evaluate the vertex vid """
		
		df = self._dataflow
		actor = df.actor(vid)

		self._evaluated.add(vid)


		# For each inputs
		for pid in df.in_ports(vid) :
			inputs = []

			cpt = 0 
			# For each connected node
			for npid in df.connected_ports(pid):
				nvid = df.vertex(npid)
				if nvid not in self._evaluated:
					self.eval_vertex(nvid)

				inputs.append(df.actor(nvid).get_output(df.local_id(npid)))
				cpt += 1

			# set input as a list or a simple value
			if(cpt == 1) : inputs = inputs[0]
			if(cpt > 0) : actor.set_input(df.local_id(pid), inputs)
			
		# Eval the node
		self.eval_vertex_code(vid)

	
	def eval (self, *args) :
		""" Evaluate the whole dataflow starting from leaves"""
		df = self._dataflow
		
		# Unvalidate all the nodes
		self._evaluated.clear()

		# Eval from the leaf
		for vid in (vid for vid in df.vertices() if df.nb_out_edges(vid)==0) :
			self.eval_vertex(vid)



# Sort by priority
def cmp_priority(x, y):
	(xvid, xactor) = x
	(yvid, yactor) = y
	try: px = xactor.internal_data['priority']
	except: px = 0
	try: py = yactor.internal_data['priority']
	except: py = 0
	
	# reverse order
	return cmp(py, px)



class PriorityEvaluation(BrutEvaluation) :
	""" Support priority between nodes and selective"""
	
	def eval (self, vtx_id=None) :

		df = self._dataflow
		# Unvalidate all the nodes
		self._evaluated.clear()

		if(vtx_id is not None):
			return self.eval_vertex(vtx_id)

		# Select the leafs (list of (vid, actor))
		leafs = [ (vid, df.actor(vid))
			  for vid in df.vertices() if df.nb_out_edges(vid)==0 ]

		leafs.sort(cmp_priority)
		
		# Excecute
		for vid, actor in leafs:
			self.eval_vertex(vid)



class GeneratorEvaluation (AbstractEvaluation) :
	""" evaluation algorithm with generator / priority and selection"""
	
	def __init__ (self, dataflow) :

		AbstractEvaluation.__init__(self, dataflow)
		# a property to specify if the node has already been evaluated
		self._evaluated = set()
		self._in_evaluation = set()
		self.reeval = False # Flag to force reevaluation (for generator)


	def clear(self):
		""" Clear evaluation variable """
		self._evaluated.clear()
		self.reeval = False
		
	
	def eval_vertex (self, vid) :
		""" Evaluate the vertex vid """
		
		df = self._dataflow
		actor = df.actor(vid)

		self._evaluated.add(vid)

		# For each inputs
		for pid in df.in_ports(vid) :
			inputs = []

			cpt = 0 
			# For each connected node
			for npid in df.connected_ports(pid):
				nvid = df.vertex(npid)

				# Do no reevaluate the same node
				if (nvid not in self._evaluated):
					self.eval_vertex(nvid)

				inputs.append(df.actor(nvid).get_output(df.local_id(npid)))
				cpt += 1

			# set input as a list or a simple value
			if(cpt == 1) : inputs = inputs[0]
			if(cpt > 0) : actor.set_input(df.local_id(pid), inputs)
			
		# Eval the node
		ret = self.eval_vertex_code(vid)
		
		# Reevaluation flaf
		if(ret) : self.reeval = ret


	def eval (self, vtx_id=None) :

		df = self._dataflow

		if(vtx_id is not None):
			leafs = [ (vtx_id, df.actor(vtx_id)) ]

		else:
			# Select the leafs (list of (vid, actor))
			leafs = [ (vid, df.actor(vid))
				  for vid in df.vertices() if df.nb_out_edges(vid)==0 ]

		leafs.sort(cmp_priority)
		
		# Excecute

		for vid, actor in leafs:
			self.reeval = True
			while(self.reeval):
				self.clear()
				self.eval_vertex(vid)

		return False




