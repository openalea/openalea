# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Wralea for System nodes"""
__revision__ = " $Id$ "


from openalea.core.external import * #IGNORE:W0614
from openalea.core.pkgdict import protected


__name__ = "openalea.flow control"
__alias__ = ["system"]
__version__ = '1.0.0'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'System Node library.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []

annotation = Factory(name="annotation", 
                     description="Annotation", 
                     category="flow control", 
                     nodemodule="openalea.core.system.systemnodes",
                     nodeclass="AnnotationNode",
                     )

__all__.append('annotation')

iter = Factory(name="iter", 
                  description="Iteration", 
                  category="System", 
                  nodemodule="openalea.core.system.systemnodes",
                  nodeclass="IterNode",
                  inputs = (dict(name="generator", interface=None, value=None),
                            ),
                  outputs = ( dict(name="value", interface=None), ),

                  )
__all__.append('iter')

iter_with_delay = Factory(name="iter with delay", 
                  description="Iteration ", 
                  category="flow control", 
                  nodemodule="openalea.core.system.systemnodes",
                  nodeclass="IterWithDelayNode",
                  inputs = (dict(name="generator", interface=None, value=None),
                            dict(name="delay", interface=IInt, value=1),
                            ),
                  outputs = ( dict(name="value", interface=None), ),

                  )
__all__.append('iter_with_delay')

counter = Factory(name="counter", 
                  description="Count from start to stop, step by step ", 
                  category="flow control", 
                  nodemodule="openalea.core.system.systemnodes",
                  nodeclass="Counter",
                  inputs = (dict(name="start", interface=IInt, value=0),
                            dict(name="stop", interface=IInt, value=10),
                            dict(name="step", interface=IInt, value=1),
                            dict(name="dummy", interface=None),
                            ),
                  outputs = ( dict(name="value", interface=IInt), ),
                  delay = 1,
                  )
__all__.append('counter')

stop_simulation = Factory(name="stop simulation", 
                  description="Iteration ", 
                  category="flow control", 
                  nodemodule="openalea.core.system.systemnodes",
                  nodeclass="StopSimulation",
                  inputs = (dict(name="any object"),
                            dict(name="max nb cycles", interface=IInt, value=10),
                            ),
                  outputs = ( dict(name="any"), ),

                  )
__all__.append('stop_simulation')

rdv = Factory(name="rendez vous", 
              description="Synchronize 2 inputs", 
              category="flow control", 
              nodemodule="openalea.core.system.systemnodes",
              nodeclass="RDVNode",
              inputs = (dict(name="value", interface=None, value=None),
                        dict(name="control_flow", interface=None, value=None),
                        ),
              outputs = ( dict(name="value", interface=None), 
                          dict(name="flow result", interface=None),),

                 )

__all__.append('rdv')

poolreader = Factory( name="pool reader",
              description="Read data from the data pool.",
              category="flow control",
              nodemodule="openalea.core.system.systemnodes",
              nodeclass="PoolReader",
              inputs = (dict(name='Key', interface=IStr),),
              outputs = (dict(name='Obj', interface=None),),
              lazy = False,
              
              )
    
__all__.append('poolreader')

poolwriter = Factory(name="pool writer",
             description="Write data to the data pool.",
             category="flow control",
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="PoolWriter",
             inputs = (dict(name='Key', interface=IStr),
                       dict(name='Obj', interface=None),),
             outputs = (dict(name='Obj', interface=None),),
             lazy = False,
             )

__all__.append('poolwriter')

pool_rw = Factory(name="pool setdefault",
             description="pool.setdefault(key,value).",
             category="flow control",
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="PoolDefault",
             inputs = (dict(name='Key', interface=IStr),
                       dict(name='Value', interface=None),),
             outputs = (dict(name='Obj', interface=None),),
             lazy = False,
             )

__all__.append('pool_rw')


#     nf = Factory(name="list accumulator", 
#                  description="List accumulator", 
#                  category="System", 
#                  nodemodule="openalea.core.system.systemnodes",
#                  nodeclass="AccuList",
#                  inputs = (dict(name="value", interface=None, value=None),
#                            dict(name="varname", interface=IStr, value=None),
#                            ),
#                  outputs = ( dict(name="list", interface=ISequence), ),

#                  )

#     package.add_factory(nf)


#     nf = Factory(name="float accumulator", 
#                  description="Float accumulator", 
#                  category="System", 
#                  nodemodule="openalea.core.system.systemnodes",
#                  nodeclass="AccuFloat",
#                  inputs = (dict(name="value", interface=IFloat, value=0.),
#                            dict(name="varname", interface=IStr, value=None),
#                            ),
#                  outputs = ( dict(name="float", interface=IFloat), ),

#                  )

#     package.add_factory(nf)


init = Factory(name="init", 
             description="Value selector for graph initialisation", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="InitNode",
             inputs = (dict(name="val_init", interface=None, value=0.),
                       dict(name="value", interface=None, value=None),
                       dict(name="state", interface=IBool, value=True),
                       ),
             outputs = ( dict(name="value", interface=None), ),
             
             )

__all__.append('init')
 
    
X = Factory(name="X", 
             description="Function variable", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="LambdaVar",
             inputs = (dict(name="name", interface=IStr, value='x'),  ),
             outputs = ( dict(name="lambda", interface=None), ),
             )

__all__.append('X')

    
whileuni = Factory(name="while univariate", 
             description="While Loop (Univariate)", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="WhileUniVar",
             inputs = (dict(name="InitValue", interface=None, value=None),  
                       dict(name="Test", interface=IFunction, value=None),  
                       dict(name="Function", interface=IFunction, value=None),  
                       ),
             outputs = ( dict(name="Result", interface=None), ),
             )

__all__.append('whileuni')

    
whilemulti = Factory(name="while multivariate", 
             description="While Loop (Multivariate)", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="WhileMultiVar",
             inputs = (dict(name="InitValues", interface=ISequence, value=[]),  
                       dict(name="Test", interface=IFunction, value=None),  
                       dict(name="Functions", interface=IFunction, value=None),  
                       ),
             outputs = ( dict(name="Results", interface=ISequence), ),
             )


__all__.append('whilemulti')

whilemulti2 = Factory(name="while multivariate2", 
             description="While Loop (Multivariate)", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="while_multi2",
             inputs = (dict(name="InitValues", interface=ISequence, value=[]),  
                       dict(name="Test", interface=IFunction, value=None),  
                       dict(name="Functions", interface=IFunction, value=None),  
                       ),
             outputs = ( dict(name="Results", interface=ISequence), ),
             )


__all__.append('whilemulti2')

cmd = Factory(name=protected("command"), 
             description="Call a system command", 
             category="System", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="system_cmd",
             inputs = (dict(name="commands", interface=ISequence, value=[], 
                            desc='List of command strings'),  
                       ),
             outputs = ( dict(name="stdout", interface=None, desc='result'), 
                         dict(name="stderr", interface=None, desc='result'), ),
                     )



__all__.append('cmd')

_delay = Factory(name="delay", 
             description="Delay return the previous or an init value.", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="Delay",
             inputs = (dict(name="init", interface=None), 
                       dict(name="x", interface=None),
                       dict(name="reset", interface=IBool )),
             outputs = ( dict(name="previous", interface=None), ),
             lazy = False,
             )

__all__.append('_delay')


_for = Factory(name="for", 
             description="for Loop (Univariate)", 
             category="flow control", 
             nodemodule="openalea.core.system.systemnodes",
             nodeclass="For",
             inputs = (dict(name="InitValue", interface=None, value=None),  
                       dict(name="list", interface=ISequence, value=None),  
                       dict(name="Function", interface=IFunction, value=None),  
                       ),
             outputs = ( dict(name="Result", interface=None), ),
             )

__all__.append('_for')

