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
This module defines a loop to evaluate
a scheduler in a different thread
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from time import sleep
from threading import Thread

class Loop (object) :
	"""Create a thread to evaluate a scheduler.
	"""
	def __init__ (self, scheduler, post_step_func = None) :
		"""Initialise the loop.
		
		scheduler: a scheduler to manage each step
		post_step_func: a function that will be
		                called after each step
		"""
		self._scheduler = scheduler
		self._gen = scheduler.run()
		self._post_step_func = post_step_func
		self._running = False
		self._thread = None
		self._current_step = 0
	
	###############################################
	#
	#    accessors
	#
	###############################################
	def running (self) :
		"""Tell wether the loop is currently running.
		"""
		return self._running
	
	def current_step (self) :
		"""Current step reached by the scheduler.
		"""
		return self._current_step
	
	def step (self) :
		"""Perform one step of the scheduler
		in the current thread.
		"""
		self._current_step = self._gen.next()
		if self._post_step_func is not None :
			self._post_step_func()
		return self._current_step
	
	def _loop (self) :
		"""Internal function that advance from one step.
		"""
		while True :
			if not self._running :
				return
			self.step()
			sleep(0.01)
	
	def play (self) :
		"""Create a thread and evaluate the
		scheduler infinitely.
		"""
		self._running = True
		self._thread = Thread(None,self._loop)
		self._thread.start()
	
	def pause (self) :
		"""Pause the current thread.
		Wait for the current step to be finished
		before exiting the thread.
		"""
		self._running = False
		if self._thread is not None :
			while self._thread.isAlive() :
				sleep(0.01)
			self._thread = None
