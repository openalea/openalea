# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

def range2n(x):
    l = []
    for i in range(x):
        l.append(2**i)
    return l

#Names of the enumeration
enum = [ "VERTEXADDITIONLOCK",
         "VERTEXDELETIONLOCK", 
         "EDGEADDITIONLOCK", 
         "EDGEDELETIONLOCK",
         "TOPOLOGICALLOCK",
         "EDITIONLEVELLOCK_1",
         "EDITIONLEVELLOCK_2",
         "EDITIONLEVELLOCK_3",
         "EDITIONLEVELLOCK_4",
         "EDITIONLEVELLOCK_5"]

#Values of the enumeration
values = range2n(len(enum))

#Delare the name/value pairs in module namespace
for e, v in zip(enum, values):
    exec(e +"=" + str(v))
    
#Fix some of them:
TOPOLOGICALLOCK=VERTEXADDITIONLOCK|VERTEXDELETIONLOCK|EDGEADDITIONLOCK|EDGEDELETIONLOCK

    
def make_interaction_level_decorator(dic=None):
    class InteractionLevelClass(object):
        FIMD = {} if not dic else dic #Function Interaction Mask Dictionary
        def __init__(self, level):
            self.level = level            
        def __call__(self, f):
            InteractionLevelClass.FIMD[f.__name__] = self.level
            return f
        @classmethod
        def add(cls, *others):
            ret = cls.FIMD.copy()
            for cl in others:
                ret.update(cl.FIMD)
            return ret
    return InteractionLevelClass