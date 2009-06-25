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
scheduler unit tests
"""

__license__= "Cecill-C"
__revision__=" $Id"

from openalea.scheduler import Task,Scheduler

####################################
#
print "defines action functions"
#
####################################
def f1 () :
	print 'f1'

def f2 () :
	print 'f2'

def f3 () :
	print 'f3'

####################################
#
print "encapsulate function into tasks"
#
####################################
t1 = Task(f1,delay = 1,priority = 2)
t2 = Task(f2,delay = 2,priority = 1)
t3 = Task(f3,delay = 3,priority = 3)

####################################
#
print "create scheduler"
#
####################################
s = Scheduler()

#register tasks
s.register(t1, start_time = 0)
s.register(t2)
s.register(t3, start_time = 5)
	
####################################
#
print "run scheduler"
#
####################################
for cycle in s.run() :
	if cycle > 30 :
		break

