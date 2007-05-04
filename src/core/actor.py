# -*- python -*-
# -*- coding: latin-1 -*-
#
#       Functor : openalea core package
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
This module provide an actor interface
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

class IActor (object) :
	"""
	interface to emulate a function
	"""
	def eval (self) :
		raise NotImplementedError
	
	def set_input (self, key, value_list) :
		raise NotImplementedError
	
	def output (self, key) :
		raise NotImplementedError

