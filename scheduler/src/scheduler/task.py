# -*- python -*-
#
#       scheduler: simple scheduling of tasks
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Christophe Pradal <christophe.pradal@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""
This module defines the Task object, an atomic event
to be evaluated by a scheduler
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

class Task (object) :
	"""Handle a function that will be called regularly.
	
	Atomic even handled by a scheduler
	"""
	def __init__ (self, func, delay, priority, name = "") :
		"""Intialiser the task.
		
		func: the function that will be called
		delay: frequency of call to the function
		priority: a way to order different task that
		          must be executed at the same time
		"""
		assert callable(func)
		self._func = func
		self._delay = delay
		self._priority = priority
		self._name = name
		
		self._evaluate = True
	
	###############################################
	#
	#	accessors
	#
	###############################################
	def func (self) :
		"""Retrieve the associated function.
		"""
		return self._func
	
	def delay (self) :
		"""Retrieve the frequency of this task.
		"""
		return self._delay
	
	def priority (self) :
		"""Retrieve the priority of this task.
		"""
		return self._priority
	
	def name (self) :
		"""Retrieve the name of this task.
		"""
		return self._name
	###############################################
	#
	#	evaluation of the function
	#
	###############################################
	def enable_evaluation (self, enable) :
		"""Set the evaluation of the associated function.
		
		enable: bool
		"""
		self._evaluate = enable
	
	def evaluate (self) :
		"""Call the associated function.
		"""
		if self._evaluate :
			self._func()
		return self._delay

