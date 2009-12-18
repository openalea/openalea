# -*- python -*-
#
#       scheduler: organize tasks in time
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""
node definition for scheduler package
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

from openalea import scheduler as sch

from openalea.core.node import AbstractNode, Node
from openalea.core.dataflow import SubDataflow


def create_task (function, delay, priority, name, start) :
    task = sch.Task(function,delay,priority,name)
    if start < 0 :
        start = None
    return (task,start),

def create_scheduler (tasks) :
    scheduler = sch.Scheduler()
    try :
        iter(tasks[1])
        for task,start_time in tasks :
            scheduler.register(task,start_time)
    except TypeError,IndexError :
        task,start_time = tasks
        scheduler.register(task,start_time)
    
    return scheduler,

def run (scheduler, nb_step) :
    g = scheduler.run()
    for i in range(nb_step):
        next_cycle = g.next()
    return scheduler,

def call (function) :
	return function(),


