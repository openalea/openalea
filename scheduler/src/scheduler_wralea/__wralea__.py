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

from openalea.core import Factory
from openalea.core.interface import *

__name__ = "openalea.scheduler"
__alias__ = ['scheduler']
__version__ = '0.8.0'
__license__ = "Cecill-C"
__authors__ = 'Jerome Chopard'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Scheduler Node library.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'
__all__ = []

ccycle = Factory( name= "current_cycle", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "current_cycle",
                inputs=(dict(name="ini", interface=IInt,),),
                outputs=(dict(name="set", interface=IFunction,),
                         dict(name="get", interface=IFunction,),),
            )

__all__.append('ccycle')

task = Factory( name= "task", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "create_task",
                inputs=(dict(name="function", interface=IFunction,),
                        dict(name="delay", interface=IInt),
                        dict(name="priority", interface=IInt, value=0),
                        dict(name="name", interface=IStr, value=""),
                        dict(name="start", interface=IInt, value=0),),
                outputs=(dict(name="(task,start)", interface=ISequence,),),
                toscriptclass_name = "create_task_script",
            )

__all__.append('task')

scheduler = Factory( name= "scheduler", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "create_scheduler",
                inputs=(dict(name="tasks", interface=ISequence,),),
                outputs=(dict(name="scheduler", interface=None,),),
                toscriptclass_name = "create_scheduler_script",
            )

__all__.append('scheduler')

run = Factory( name= "run", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "run",
                inputs=(dict(name="scheduler",),
                        dict(name="nb_step", interface=IInt,),
                        dict(name="set_current_cycle", interface=IFunction, value=None),),
                outputs=(dict(name="scheduler", interface=None,),),
                toscriptclass_name = "run_script",
            )

__all__.append('run')

loop = Factory( name= "loop", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "create_loop",
                inputs=(dict(name="scheduler", interface=None),),
                outputs=(dict(name="scheduler", interface=None,),),
                toscriptclass_name = "create_loop_script",
            )

__all__.append('loop')

call = Factory( name= "call", 
                description= "",
                category = "",
                nodemodule = "scheduler",
                nodeclass = "call",
                inputs=(dict(name="func", interface=IFunction),),
                outputs=(dict(name="val", interface=None,),),
                toscriptclass_name = "call_script",
            )

__all__.append('call')

