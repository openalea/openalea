# -*- python -*-
# -*- coding: latin-1 -*-
#
#       Evaluator : openalea core package
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       VPlants WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide an algorithm to evaluate a dataflow
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

class BrutEvaluation (object) :
	""" Basic evaluation algorithm """
	
	def __init__ (self, dataflow) :

		self._dataflow = dataflow
		# a property to specify if the node has already been evaluated
		self._evaluated = set()

	
	def eval_vertex (self, vid) :
		""" Evaluate the vertex vid """
		
		df = self._dataflow
		actor = df.actor(vid)
		
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
		actor.eval()
		self._evaluated.add(vid)
	
	
	def eval (self) :
		""" Evaluate the whole dataflow starting from leaves"""
		df = self._dataflow
		
		# Unvalidate all the nodes
		self._evaluated.clear()

		# Eval from the leaf
		for vid in (vid for vid in df.vertices() if df.nb_out_edges(vid)==0) :
			self.eval_vertex(vid)

