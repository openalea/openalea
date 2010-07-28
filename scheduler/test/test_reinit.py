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

evaluated = []

def f1 () :
    print 'f1'
    evaluated.append(1)

def f2 () :
    print 'f2'
    evaluated.append(2)

def f3 () :
    print 'f3'
    evaluated.append(3)

t1 = Task(f1,delay = 1,priority = 2)
t2 = Task(f2,delay = 2,priority = 1)
t3 = Task(f3,delay = 3,priority = 3)

def test1 () :
    global evaluated
    del evaluated[:]
    
    s = Scheduler()
    s.register(t1, start_time = 0)
    s.register(t2)
    s.register(t3, start_time = 5)
    
    #first run
    g = s.run()
    next_cycle = g.next()
    assert next_cycle == 1
    assert tuple(evaluated) == (1,)
    
    next_cycle = g.next()
    assert next_cycle == 2
    assert tuple(evaluated) == (1,1)
    
    next_cycle = g.next()
    assert next_cycle == 3
    assert tuple(evaluated) == (1,1,1,2)
    
    #reinit
    """g.reinit()
    
    #second run
    #g = s.run()
    next_cycle = g.next()
    assert next_cycle == 1
    assert tuple(evaluated) == (1,)
    
    next_cycle = g.next()
    assert next_cycle == 2
    assert tuple(evaluated) == (1,1)
    
    next_cycle = g.next()
    assert next_cycle == 3
    assert tuple(evaluated) == (1,1,1,2)
    """

