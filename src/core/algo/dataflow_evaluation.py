# -*- python -*-
# -*- coding: latin-1 -*-
#
#       Evaluator : openalea core package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
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
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

class BrutEvaluation (object) :
	"""
	use a dataflow to compute a value
	"""
	def __init__ (self, dataflow) :
		self._dataflow=dataflow
		#a property to specify if the node has already been evaluated
		self._evaluated={}
	
	def eval_vertex (self, vid) :
		df=self._dataflow
		evaluated=self._evaluated
		actor=df.actor(vid)
		#evalue les entrees du noeud
		for pid in df.in_ports(vid) :
			inputs=[]
			for npid in df.connected_ports(pid) :
				nvid=df.vertex(npid)
				if not evaluated[nvid] :
					self.eval_vertex(nvid)
				inputs.append(df.actor(nvid).get_output(df.port(npid).local_pid))
			actor.set_input(df.port(pid).local_pid,value_list=inputs)
		#evalue le noeud
		actor.eval()
		evaluated[vid]=True
		#retour
		return
	
	def eval (self) :
		"""
		evaluate the whole dataflow starting from leaves
		"""
		df=self._dataflow
		#remise a False de la propriete d'evaluation
		for vid in df.vertices() :
			self._evaluated[vid]=False
		#evaluation a partir des feuilles
		for vid in (vid for vid in df.vertices() if df.nb_out_edges(vid)==0) :
			self.eval_vertex(vid)
		#retour
		return

