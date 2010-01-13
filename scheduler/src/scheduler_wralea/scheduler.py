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
__revision__=" $Id$ "

from openalea.scheduler import Scheduler,Task,Loop

from openalea.core import ScriptLibrary
from openalea.core.node import AbstractNode, Node
from openalea.core.dataflow import SubDataflow


def create_task (function, delay, priority, name, start) :
    task = Task(function,delay,priority,name)
    if start < 0 :
        start = None
    return (task,start),

def create_task_script (inputs, outputs) :
    lib = ScriptLibrary()
    function,delay,priority,name,start = inputs
    func,script = lib.name(function,"")
    (task,start), = outputs
    task = lib.register(task,"task_%s" % name)
    
    script += "from openalea.scheduler import Task\n"
    script += "%s = Task(%s,%d,%d,'%s')\n" % (task,func,delay,priority,name)
    
    return script

def create_scheduler (tasks) :
    scheduler = Scheduler()
    try :
        iter(tasks[1])
        for task,start_time in tasks :
            scheduler.register(task,start_time)
    except TypeError,IndexError :
        task,start_time = tasks
        scheduler.register(task,start_time)
    
    return scheduler,

def create_scheduler_script (inputs, outputs) :
    lib = ScriptLibrary()
    tasks, = inputs
    sch, = outputs
    sch = lib.register(sch,"sch")
    
    script = "from openalea.scheduler import Scheduler\n"
    script += "%s = Scheduler()\n" % sch
    
    try :
        iter(tasks[1])
        for task,start_time in tasks :
            task,script = lib.name(task,script)
            script += "%s.register(%s,%s)\n" % (sch,task,start_time)
    except TypeError,IndexError :
        task,start_time = tasks
        task,script = lib.name(task,script)
        script += "%s.register(%s,%s)\n" % (sch,task,start_time)
    
    return script

def run (scheduler, nb_step) :
    g = scheduler.run()
    for i in range(nb_step):
        next_cycle = g.next()
    return scheduler,

def run_scheduler_script (inputs, outputs) :
    lib = ScriptLibrary()
    sch,nb_step = inputs
    sch,script = lib.name(sch,"")
    
    script += "g = %s.run()\n" % sch
    script += "for i in range(%d) :\n" % nb_step
    script += "	g.next()\n\n"
    
    return script

def create_loop (scheduler) :
    return Loop(scheduler),

def create_loop_script (inputs, outputs) :
    lib = ScriptLibrary()
    sch, = inputs
    sch,script = lib.name(sch,"")
    loop, = outputs
    loop = lib.register(loop,"loop")
    
    script += "from openalea.scheduler import Loop\n"
    script += "%s = Loop(%s)\n" % (loop,sch)
    
    return script

def call (function) :
    return function(),

def call_script (inputs, outputs) :
    lib = ScriptLibrary()
    func, = inputs
    func,script = lib.name(func,"")
    val, = outputs
    val = lib.register(val,"val")
    
    script += "%s = %s()\n" % (val,func)
    
    return script


