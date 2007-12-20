# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
################################################################################


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
        

# Sort functions

# Sort by priority
def cmp_priority(x, y):
    (xvid, xactor) = x
    (yvid, yactor) = y
    px = xactor.internal_data.get('priority', 0)
    py = yactor.internal_data.get('priority', 0)
	
    # reverse order
    return cmp(py, px)


def cmp_posx(x, y):
    (pid, vid, xactor) = x
    (pid, vid, yactor) = y
    px = xactor.internal_data.get('posx', 0)
    py = yactor.internal_data.get('posx', 0)
	
    # reverse order
    return cmp(px, py)


# Evaluation Algoithm


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

    
    def get_parent_nodes(self, pid):
        """ Return the list of parent node connected to pid
        The list contains tuples (port_pid, node_pid, actor)
        This list is sorted by the x value of the node
        """
        
        df = self._dataflow

        # For each connected node
        npids = [(npid, df.vertex(npid), df.actor(df.vertex(npid))) \
                     for npid in df.connected_ports(pid)]
        npids.sort(cmp=cmp_posx)

        return npids



        

class BrutEvaluation (AbstractEvaluation) :
	""" Basic evaluation algorithm """
	
	def __init__ (self, dataflow) :

		AbstractEvaluation.__init__(self, dataflow)
		# a property to specify if the node has already been evaluated
		self._evaluated = set()

	
	def eval_vertex (self, vid, *args) :
		""" Evaluate the vertex vid """
		
		df = self._dataflow
		actor = df.actor(vid)

		self._evaluated.add(vid)


		# For each inputs
		for pid in df.in_ports(vid) :
			inputs = []

			cpt = 0 
			# For each connected node
                        for npid, nvid, nactor in self.get_parent_nodes(pid):
				if nvid not in self._evaluated:
					self.eval_vertex(nvid)

				inputs.append(nactor.get_output(df.local_id(npid)))
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



class PriorityEvaluation(BrutEvaluation) :
	""" Support priority between nodes and selective"""
	
	def eval (self, vtx_id=None, *args) :

		df = self._dataflow
		# Unvalidate all the nodes
		self._evaluated.clear()

		if(vtx_id is not None):
			return self.eval_vertex(vtx_id, *args)

		# Select the leafs (list of (vid, actor))
		leafs = [ (vid, df.actor(vid))
			  for vid in df.vertices() if df.nb_out_edges(vid)==0 ]

		leafs.sort(cmp_priority)
		
		# Excecute
		for vid, actor in leafs:
			self.eval_vertex(vid, *args)



class GeneratorEvaluation (AbstractEvaluation) :
	""" Evaluation algorithm with generator / priority and selection"""
	
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
                        for npid, nvid, nactor in self.get_parent_nodes(pid):
				# Do no reevaluate the same node
				if (nvid not in self._evaluated):
					self.eval_vertex(nvid)

				inputs.append(nactor.get_output(df.local_id(npid)))
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




from openalea.core.dataflow import SubDataflow
from openalea.core.interface import IFunction

class LambdaEvaluation (PriorityEvaluation) :
	""" Evaluation algorithm with support of lambda / priority and selection"""
	
	def __init__ (self, dataflow) :
		PriorityEvaluation.__init__(self, dataflow)
                
                self.lambda_value = {} # lambda resolution dictionary


	def eval_vertex (self, vid, context, *args) :
		""" Evaluate the vertex vid 
                @param context is a list a value to assign to lambdas
                """
		
		df = self._dataflow
		actor = df.actor(vid)

		self._evaluated.add(vid)

                use_lambda = False

		# For each inputs
		for pid in df.in_ports(vid):

                        input_index = df.local_id(pid)
			inputs = []

                        # Get input interface
                        interface = actor.input_desc[input_index].get('interface', None)

                        # Determine if the context must be transmitted
                        # If interface is IFunction it means that the node is a consumer
                        # We do not propagate the context
                        if(interface is IFunction):
                            transmit_cxt = None
                        else:
                            transmit_cxt = context
                        
			cpt = 0 # parent counter

			# For each connected node
                        for npid, nvid, nactor in self.get_parent_nodes(pid):

				# Do no reevaluate the same node
				if (nvid not in self._evaluated):
					self.eval_vertex(nvid, transmit_cxt)

                                outval = nactor.get_output(df.local_id(npid))

                                # Lambda 

                                # We must consider 2 cases
                                #  1) Lambda detection (receive a SubDataflow and interface != IFunction)
                                #         
                                #  2) Resolution mode (context is not None) : we 
                                #      replace the lambda with value

                                if(isinstance(outval, SubDataflow)
                                   and interface is not IFunction):

                                    if(not context and not self.lambda_value): 
                                        # we are not in resolution mode
                                        use_lambda = True
                                    else:
                                        # We set the context value for later use
                                        if(not self.lambda_value.has_key(outval)):
                                            try:
                                                self.lambda_value[outval] = context.pop()
                                            except Exception:
                                                raise Exception("The number of lambda variables is insuffisant")
                                        
                                        # We replace the value with a context value
                                        outval = self.lambda_value[outval]


				inputs.append(outval)
				cpt += 1

			# set input as a list or a simple value
			if(cpt == 1) : inputs = inputs[0]
			if(cpt > 0) : actor.set_input(input_index, inputs)
			
		# Eval the node
                if(not use_lambda):
                    ret = self.eval_vertex_code(vid)
                else:
                    # set the node output with subdataflow
                    for i in xrange(actor.get_nb_output()):
                        actor.outputs[i] = SubDataflow(df, self, vid, i)



        def eval (self, vtx_id=None, context=None) :
            """ 
            Eval the dataflow from vtx_id with a particular context
            @param vtx_id : vertex id to start the evaluation
            @param context : list a value to assign to lambda variables
            """
            
            self.lambda_value.clear() 
            PriorityEvaluation.eval(self, vtx_id, context)
            self.lambda_value.clear() # do not keep context in memory

DefaultEvaluation = LambdaEvaluation


# from collections import deque


# class LambdaEvaluation (PriorityEvaluation) :
# 	""" Evaluation algorithm with support of lambda / priority and selection"""
	
# 	def __init__ (self, dataflow) :

# 		PriorityEvaluation.__init__(self, dataflow)


#         def scan_graph(self, vid, context):
#             """ Return the list of vextex id in the correct process order
#             starting from vid
#             @param vid : starting vertex id
#             @param context  : variable context
#             """
            
#             df = self._dataflow

#             scanned = set() # Scanned node
#             process_list = deque()
#             scan_list = deque([(vid, context)])

#             while(scan_list):
                
#                 (vid, context) = scan_list.popleft()
                
#                 process_list.appendleft( (vid, context) )
#                 scanned.add(vid)

#                 actor = df.actor(vid)
                
#                 # For each inputs
#                 for pid in df.in_ports(vid):

#                     # Determine if the context must be transmitted
#                     # If interface is IFunction it means that the node is a consumer
#                     # We do not propagate the context
#                     input_index = df.local_id(pid)
#                     interface = actor.input_desc[input_index].get('interface', None)
#                     transmit_cxt = None if(interface is IFunction) else context

#                     # For each connected node
#                     for npid in df.connected_ports(pid):
#                         nvid = df.vertex(npid)
                   
#                         # Do no reevaluate the same node
#                         if (nvid not in scanned):
#                             scan_list.append((nvid, transmit_cxt))

#             return process_list



# 	def eval_vertex (self, vid, context, *args) :
# 		""" Evaluate the graph starting at the vertex vid 
#                 @param vid : starting vertex id
#                 @param context  : list of values to assign to variables
#                 """
                
#                 lambda_value = {}
		
#                 # Get the node order
#                 process_list = self.scan_graph(vid, context)
                
#                 # Eval each node 
#                 for vid, context in process_list:
#                     self.eval_one_vertex(vid, context, lambda_value)
        

#         def eval_one_vertex (self, vid, context, lambda_value) :
# 		""" Evaluate only one vertex 
#                 @param vid : id of vertex to evalaute
#                 @param context  : list of values to assign to variables
#                 @param lambda_value : dictionary of previous assigned values
#                 """

#                 df = self._dataflow
                
#                 actor = df.actor(vid)
#                 use_lambda = False
                    
#                 # Get inputs
#                 for pid in df.in_ports(vid):

#                     inputs = []
#                     cpt = 0 # parent counter
                        
#                     # Get input interface
#                     input_index = df.local_id(pid)
#                     interface = actor.input_desc[input_index].get('interface', None)

#                     # For each connected node
#                     for npid, nvid, nactor in self.get_parent_nodes(pid):
                            
#                         outval = nactor.get_output(df.local_id(npid))

#                         # Lambda 

#                         # We must consider 2 cases
#                         #  1) Lambda detection (receive a SubDataflow and interface != IFunction)
#                         #         
#                         #  2) Resolution mode (context is not None) : we 
#                         #      replace the lambda with value

#                         if(isinstance(outval, SubDataflow)
#                            and interface is not IFunction):

#                             if(not context and not lambda_value): 
#                                 # we are not in resolution mode
#                                 use_lambda = True
#                             else:
#                                 # We set the context value for later use
#                                 if(not lambda_value.has_key(outval)):
#                                     try:
#                                         lambda_value[outval] = context.pop()
#                                     except Exception,e :
#                                         print e, context, lambda_value
#                                         raise Exception("The number of lambda variables is insuffisant")
                                        
#                                 # We replace the value with a context value
#                                 outval = lambda_value[outval]


#                         inputs.append(outval)
#                         cpt += 1

#                     # set input as a list or a simple value
#                     if(cpt == 1) : inputs = inputs[0]
#                     if(cpt > 0) : actor.set_input(input_index, inputs)

                        
#                 # Eval the node
#                 if(not use_lambda):
#                     ret = self.eval_vertex_code(vid)
#                 else:
#                     # tranmit a SubDataflow to following node
#                     for i in xrange(actor.get_nb_output()):
#                         actor.outputs[i] = SubDataflow(df, self, vid, i)



#         def eval (self, vtx_id=None, context=None) :
#             """ 
#             Eval the dataflow from vtx_id with a particular context
#             @param vtx_id : vertex id to start the evaluation
#             @param context : list a value to assign to lambda variables
#             """
            
#             PriorityEvaluation.eval(self, vtx_id, context)



# from openalea.core.threadmanager import ThreadManager

# class ParallelEvaluation(LambdaEvaluation):
#     """ Parallel execution of a dataflow """

#     def eval_vertex (self, vid, context, *args) :
#         """ Evaluate the graph starting at the vertex vid 
#         @param vid : starting vertex id
#         @param context  : list of values to assign to variables
#         """
        
#         tm = ThreadManager()

#         lambda_value = {}
		
#         # Get the node order
#         process_list = self.scan_graph(vid, context)
                
#         # Eval each node 
#         for vid, context in process_list:
#             tm.queue.put( (self.eval_one_vertex, (vid, context, lambda_value)))


# DefaultEvaluation = ParallelEvaluation
