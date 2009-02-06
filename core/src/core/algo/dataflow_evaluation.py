# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
###############################################################################
"""This module provide an algorithm to evaluate a dataflow"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import sys
import traceback as tb


class EvaluationException(Exception):

    def __init__(self, vid, node, exception, exc_info):
        Exception.__init__(self)
        self.vid = vid
        self.node = node
        self.exception = exception
        self.exc_info = exc_info


# Sort functions

# order function sort by priority


def cmp_priority(x, y):
    """todo"""
    (xvid, xactor) = x
    (yvid, yactor) = y
    px = xactor.internal_data.get('priority', 0)
    py = yactor.internal_data.get('priority', 0)

    # reverse order
    return cmp(py, px)


# order function to sort by pos x


def cmp_posx(x, y):
    """todo"""
    (xpid, xvid, xactor) = x
    (ypid, yvid, yactor) = y
    px = xactor.internal_data.get('posx', 0)
    py = yactor.internal_data.get('posx', 0)

    ret = cmp(px, py)
    if (not ret):
        ret = cmp(xpid, ypid)
    # reverse order
    return ret


# Evaluation Algoithm


class AbstractEvaluation(object):
    """ Abstract evaluation algorithm """

    def __init__(self, dataflow):
        self._dataflow = dataflow

    def eval(self, *args):
        """todo"""
        raise NotImplementedError()

    def is_stopped(self, vid, actor):
        """ Return True if evaluation must be stop at this vertex. """
        return actor.block

    def eval_vertex_code(self, vid):
        """
        Evaluate the vertex vid.
        Can raise an exception if evaluation failed.
        """

        node = self._dataflow.actor(vid)

        try:
            ret = node.eval()
            # When an exception is raised, a flag is set.
            # So we remove it when evaluation is ok.
            if hasattr(node, 'raise_exception'):
                del node.raise_exception
                node.notify_listeners(('data_modified', ))
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
            raise EvaluationException(vid, node, e, \
                tb.format_tb(sys.exc_info()[2]))

    def get_parent_nodes(self, pid):
        """
        Return the list of parent node connected to pid
        The list contains tuples (port_pid, node_pid, actor)
        This list is sorted by the x value of the node
        """

        df = self._dataflow

        # For each connected node
        npids = [(npid, df.vertex(npid), df.actor(df.vertex(npid))) \
                     for npid in df.connected_ports(pid)]
        npids.sort(cmp=cmp_posx)

        return npids


class BrutEvaluation(AbstractEvaluation):
    """ Basic evaluation algorithm """

    def __init__(self, dataflow):

        AbstractEvaluation.__init__(self, dataflow)
        # a property to specify if the node has already been evaluated
        self._evaluated = set()

    def is_stopped(self, vid, actor):
        """ Return True if evaluation must be stop at this vertex """
        return actor.block or vid in self._evaluated

    def eval_vertex(self, vid, *args):
        """ Evaluate the vertex vid """

        df = self._dataflow
        actor = df.actor(vid)

        self._evaluated.add(vid)

        # For each inputs
        for pid in df.in_ports(vid):
            inputs = []

            cpt = 0
            # For each connected node
            for npid, nvid, nactor in self.get_parent_nodes(pid):
                if not self.is_stopped(nvid, nactor):
                    self.eval_vertex(nvid)

                inputs.append(nactor.get_output(df.local_id(npid)))
                cpt += 1

            # set input as a list or a simple value
            if (cpt == 1):
                inputs = inputs[0]
            if (cpt > 0):
                actor.set_input(df.local_id(pid), inputs)

        # Eval the node
        self.eval_vertex_code(vid)

    def eval(self, *args):
        """ Evaluate the whole dataflow starting from leaves"""
        df = self._dataflow

        # Unvalidate all the nodes
        self._evaluated.clear()

        # Eval from the leaf
        for vid in (vid for vid in df.vertices() if df.nb_out_edges(vid)==0):
            self.eval_vertex(vid)


class PriorityEvaluation(BrutEvaluation):
    """ Support priority between nodes and selective"""

    def eval(self, vtx_id=None, *args):
        """todo"""

        df = self._dataflow
        # Unvalidate all the nodes
        self._evaluated.clear()

        if (vtx_id is not None):
            return self.eval_vertex(vtx_id, *args)

        # Select the leafs (list of (vid, actor))
        leafs = [(vid, df.actor(vid))
              for vid in df.vertices() if df.nb_out_edges(vid)==0]

        leafs.sort(cmp_priority)

        # Excecute
        for vid, actor in leafs:
            self.eval_vertex(vid, *args)


class GeneratorEvaluation(AbstractEvaluation):
    """ Evaluation algorithm with generator / priority and selection"""

    def __init__(self, dataflow):

        AbstractEvaluation.__init__(self, dataflow)
        # a property to specify if the node has already been evaluated
        self._evaluated = set()
        self._in_evaluation = set()
        self.reeval = False # Flag to force reevaluation (for generator)

    def is_stopped(self, vid, actor):
        """ Return True if evaluation must be stop at this vertex """
        return actor.block or vid in self._evaluated

    def clear(self):
        """ Clear evaluation variable """
        self._evaluated.clear()
        self.reeval = False

    def eval_vertex(self, vid):
        """ Evaluate the vertex vid """

        df = self._dataflow
        actor = df.actor(vid)

        self._evaluated.add(vid)

        # For each inputs
        for pid in df.in_ports(vid):
            inputs = []

            cpt = 0
            # For each connected node
            for npid, nvid, nactor in self.get_parent_nodes(pid):
                # Do no reevaluate the same node
                if not self.is_stopped(nvid, nactor):
                    self.eval_vertex(nvid)

                inputs.append(nactor.get_output(df.local_id(npid)))
                cpt += 1

            # set input as a list or a simple value
            if (cpt == 1):
                inputs = inputs[0]
            if (cpt > 0):
                actor.set_input(df.local_id(pid), inputs)

        # Eval the node
        ret = self.eval_vertex_code(vid)

        # Reevaluation flag
        if (ret):
            self.reeval = ret

    def eval(self, vtx_id=None):

        df = self._dataflow

        if (vtx_id is not None):
            leafs = [(vtx_id, df.actor(vtx_id))]

        else:
            # Select the leafs (list of (vid, actor))
            leafs = [(vid, df.actor(vid))
                for vid in df.vertices() if df.nb_out_edges(vid)==0]

        leafs.sort(cmp_priority)

        # Execute
        for vid, actor in leafs:
            self.reeval = True
            while(self.reeval):
                self.clear()
                self.eval_vertex(vid)

        return False


from openalea.core.dataflow import SubDataflow
from openalea.core.interface import IFunction


class LambdaEvaluation(PriorityEvaluation):
    """ Evaluation algorithm with support of lambda / priority and selection"""

    def __init__(self, dataflow):
        PriorityEvaluation.__init__(self, dataflow)

        self.lambda_value = {} # lambda resolution dictionary

    def eval_vertex(self, vid, context, lambda_value, *args):
        """
        Evaluate the vertex vid
        @param context is a list a value to assign to lambdas

        This function is called both by the user (eval a node and its parents)
        and by the SubDataFlow evaluation.

        First the graph is traversed by the algorithm in a bottom-up way.
        The SubDataflow is stored in the inputs.
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
            if (interface is IFunction):
                transmit_cxt = None
                transmit_lambda = None
            else:
                transmit_cxt = context
                transmit_lambda = lambda_value

            cpt = 0 # parent counter

            # For each connected node
            for npid, nvid, nactor in self.get_parent_nodes(pid):

                # Do no reevaluate the same node
                if not self.is_stopped(nvid, nactor):
                    self.eval_vertex(nvid, transmit_cxt, transmit_lambda)

                outval = nactor.get_output(df.local_id(npid))
                # Lambda

                # We must consider 3 cases
                #  1) Lambda detection (receive a SubDataflow and
                # interface != IFunction)
                #
                #  2) Resolution mode (context is not None): we
                #      replace the lambda with value.

                if (isinstance(outval, SubDataflow)
                   and interface is not IFunction):

                    if (not context and not lambda_value):
                        # we are not in resolution mode
                        use_lambda = True
                    else:
                        # We set the context value for later use.
                        # We set resolved values into the dataflow.
                        # outval is a SubDataFlow. For this object, we have
                        # now a value.
                        # E.g. f(x=3). We replace x subdf by 3.
                        # If x is used elsewhere (f(x,x)), we referenced it
                        # in a dict.
                        if (not lambda_value.has_key(outval)):
                            try:
                                lambda_value[outval] = context.pop()
                            except Exception:
                                raise Exception("The number of lambda variables is insuffisant")

                        # We replace the value with a context value
                        outval = lambda_value[outval]

                inputs.append(outval)
                cpt += 1

            # set input as a list or a simple value
            if (cpt == 1):
                inputs = inputs[0]
            if (cpt > 0):
                actor.set_input(input_index, inputs)

        # Eval the node
        if (not use_lambda):
            ret = self.eval_vertex_code(vid)

        else:
            # set the node output with subdataflow
            for i in xrange(actor.get_nb_output()):
                actor.set_output(i, SubDataflow(df, self, vid, i))

    def eval(self, vtx_id=None, context=None):
        """
        Eval the dataflow from vtx_id with a particular context
        @param vtx_id: vertex id to start the evaluation
        @param context: list a value to assign to lambda variables
        """

        self.lambda_value.clear()

        if (context):
            # The evaluate, due to the recursion, is done fisrt in last out.
            # thus, we have to reverse the arguments to evaluate the function (FIFO).
            context.reverse()

        PriorityEvaluation.eval(self, vtx_id, context, self.lambda_value)
        self.lambda_value.clear() # do not keep context in memory


DefaultEvaluation = LambdaEvaluation
#DefaultEvaluation = GeneratorEvaluation


# from collections import deque


# class LambdaEvaluation (PriorityEvaluation):
# 	""" Evaluation algorithm with support of lambda / priority and selection"""

# 	def __init__ (self, dataflow):

# 		PriorityEvaluation.__init__(self, dataflow)


#         def scan_graph(self, vid, context):
#             """ Return the list of vextex id in the correct process order
#             starting from vid
#             @param vid: starting vertex id
#             @param context: variable context
#             """

#             df = self._dataflow

#             process_list = deque()
#             scan_list = deque([(vid, context)])

#             while(scan_list):

#                 (vid, context) = scan_list.popleft()
#                 process_list.appendleft((vid, context) )
#                 actor = df.actor(vid)

#                 # For each inputs
#                 for pid in df.in_ports(vid):

#                     # Determine if the context must be transmitted
#                     # If interface is IFunction it means that the node is a consumer
#                     # We do not propagate the context
#                     input_index = df.local_id(pid)
#                     interface = actor.input_desc[input_index].get('interface', None)
#                     transmit_cxt = None if (interface is IFunction) else context

#                     # For each connected node
#                     for npid in df.connected_ports(pid):
#                         nvid = df.vertex(npid)
#                         scan_list.append((nvid,  transmit_cxt))

#             return process_list



# 	def eval_vertex (self, vid, context, *args):
# 		""" Evaluate the graph starting at the vertex vid
#                 @param vid: starting vertex id
#                 @param context  list of values to assign to variables
#                 """

#                 lambda_value = {}

#                 # Get the node order
#                 process_list = self.scan_graph(vid, context)

#                 # Eval each node
#                 scanned = set()

#                 for vid, context in process_list:
#                     if (vid not in scanned):
#                         self.eval_one_vertex(vid, context, lambda_value)
#                     scanned.add(vid)


#         def get_output_value(self, nvid, nactor, npid):
#             """ Return the value of a node output """

#             return nactor.get_output(self._dataflow.local_id(npid))



#         def eval_one_vertex (self, vid, context, lambda_value):
# 		""" Evaluate only one vertex
#                 @param vid: id of vertex to evalaute
#                 @param context: list of values to assign to variables
#                 @param lambda_value: dictionary of previous assigned values
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

#                         outval = self.get_output_value(nvid, nactor, npid)

#                         # Lambda

#                         # We must consider 2 cases
#                         #  1) Lambda detection (receive a SubDataflow and interface != IFunction)
#                         #
#                         #  2) Resolution mode (context is not None): we
#                         #      replace the lambda with value

#                         if (isinstance(outval, SubDataflow)
#                            and interface is not IFunction):

#                             if (not context and not lambda_value):
#                                 # we are not in resolution mode
#                                 use_lambda = True
#                             else:
#                                 # We set the context value for later use
#                                 if (not lambda_value.has_key(outval)):
#                                     try:
#                                         lambda_value[outval] = context.pop()
#                                     except Exception,e:
#                                         print e, context, lambda_value
#                                         raise Exception("The number of lambda variables is insuffisant")

#                                 # We replace the value with a context value
#                                 outval = lambda_value[outval]


#                         inputs.append(outval)
#                         cpt += 1

#                     # set input as a list or a simple value
#                     if (cpt == 1): inputs = inputs[0]
#                     if (cpt > 0): actor.set_input(input_index, inputs)


#                 # Eval the node
#                 if (not use_lambda):
#                     ret = self.eval_vertex_code(vid)
#                 else:
#                     # tranmit a SubDataflow to following node
#                     for i in xrange(actor.get_nb_output()):
#                         actor.outputs[i] = SubDataflow(df, self, vid, i)



#         def eval (self, vtx_id=None, context=None):
#             """
#             Eval the dataflow from vtx_id with a particular context
#             @param vtx_id: vertex id to start the evaluation
#             @param context: list a value to assign to lambda variables
#             """

#             PriorityEvaluation.eval(self, vtx_id, context)



# from openalea.core.threadmanager import ThreadManager
# import thread

# class ParallelEvaluation(LambdaEvaluation):
#     """ Parallel execution of a dataflow """


#     def get_output_value(self, nvid, nactor, npid):
#             """ Return the value of a node output """

#             l = self.locks[nvid]

#             l.acquire()
#             v = nactor.get_output(self._dataflow.local_id(npid))
#             l.release()

#             return v


#     def eval_one_vertex (self, vid, context, lambda_value):
#         """ Evaluate only one vertex
#         @param vid: id of vertex to evalaute
#         @param context: list of values to assign to variables
#         @param lambda_value: dictionary of previous assigned values
#         """
#         LambdaEvaluation.eval_one_vertex(self, vid, context, lambda_value)
#         self.locks[vid].release()



#     def eval_vertex (self, vid, context, *args):
#         """ Evaluate the graph starting at the vertex vid
#         @param vid: starting vertex id
#         @param context list of values to assign to variables
#         """

#         lambda_value = {}

#         tm = ThreadManager()
#         tm.clear()

#         # Get the node order
#         process_list = self.scan_graph(vid, context)

#         # Synchronisation locks
#         self.locks = {}

#         for vid, context in process_list:

#             if (self.locks.has_key(vid)): continue
#             l = thread.allocate_lock()
#             l.acquire()
#             self.locks[vid] = l


#         # Eval each node
#         scanned = set()

#         for vid, context in process_list:
#             if (vid not in scanned):
#                 tm.add_task( self.eval_one_vertex, (vid, context, lambda_value))
#             scanned.add(vid)



# DefaultEvaluation = ParallelEvaluation
# #DefaultEvaluation = LambdaEvaluation
