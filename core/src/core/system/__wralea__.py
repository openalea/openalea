# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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

__doc__="""
Wralea for System nodes
"""

__revision__=" $Id$ "


from openalea.core import *


__name__ = "system"
__version__ = '0.0.1'
__license__= "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'System Node library.'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = []

annotation = Factory(name="annotation", 
                     description="Annotation", 
                     category="System", 
                     nodemodule="systemnodes",
                     nodeclass="AnnotationNode",
                     )

__all__.append('annotation')

#     nf = Factory(name="iter", 
#                  description="Iteration", 
#                  category="System", 
#                  nodemodule="systemnodes",
#                  nodeclass="IterNode",
#                  inputs = (dict(name="generator", interface=None, value=None),
#                            ),
#                  outputs = ( dict(name="value", interface=None), ),

#                  )

rdv = Factory(name="rendez vous", 
              description="Synchronize 2 inputs", 
              category="System", 
              nodemodule="systemnodes",
              nodeclass="RDVNode",
              inputs = (dict(name="value", interface=None, value=None),
                        dict(name="control_flow", interface=None, value=None),
                        ),
              outputs = ( dict(name="value", interface=None), ),

                 )

__all__.append('rdv')

poolreader = Factory( name="pool reader",
              description="Read data from the data pool.",
              category="System",
              nodemodule="systemnodes",
              nodeclass="PoolReader",
              inputs = (dict(name='Key', interface=IStr),),
              outputs = (dict(name='Obj', interface=None),),
              lazy = False,
              
              )
    
__all__.append('poolreader')

poolwriter = Factory(name="pool writer",
             description="Write data to the data pool.",
             category="System",
             nodemodule="systemnodes",
             nodeclass="PoolWriter",
             inputs = (dict(name='Key', interface=IStr),
                       dict(name='Obj', interface=None),),
             lazy = False,
             )

__all__.append('poolwriter')



#     nf = Factory(name="list accumulator", 
#                  description="List accumulator", 
#                  category="System", 
#                  nodemodule="systemnodes",
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
#                  nodemodule="systemnodes",
#                  nodeclass="AccuFloat",
#                  inputs = (dict(name="value", interface=IFloat, value=0.),
#                            dict(name="varname", interface=IStr, value=None),
#                            ),
#                  outputs = ( dict(name="float", interface=IFloat), ),

#                  )

#     package.add_factory(nf)


#     nf = Factory(name="init", 
#                  description="Value selector for graph initialisation", 
#                  category="System", 
#                  nodemodule="systemnodes",
#                  nodeclass="InitNode",
#                  inputs = (dict(name="val_init", interface=None, value=0.),
#                            dict(name="value", interface=None, value=None),
#                            dict(name="state", interface=IBool, value=True),
#                            ),
#                  outputs = ( dict(name="value", interface=None), ),

#                  )

#     package.add_factory(nf)
 
    
X = Factory(name="X", 
             description="Function variable", 
             category="System", 
             nodemodule="systemnodes",
             nodeclass="LambdaVar",
             inputs = (dict(name="name", interface=IStr, value='x'),  ),
             outputs = ( dict(name="lambda", interface=None), ),
             )

__all__.append('X')

    
whileuni = Factory(name="while univariate", 
             description="While Loop (Univariate)", 
             category="System", 
             nodemodule="systemnodes",
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
             category="System", 
             nodemodule="systemnodes",
             nodeclass="WhileMultiVar",
             inputs = (dict(name="InitValues", interface=ISequence, value=[]),  
                       dict(name="Test", interface=IFunction, value=None),  
                       dict(name="Functions", interface=IFunction, value=None),  
                       ),
             outputs = ( dict(name="Results", interface=ISequence), ),
             )


__all__.append('whilemulti')


os_system = Factory(name="os.system", 
             description="Call a system command", 
             category="System", 
             nodemodule="os",
             nodeclass="system",
             inputs = (dict(name="command", interface=IStr, value='', desc='command string'),  
                       ),
             outputs = ( dict(name="result", interface=None), ),
             )


__all__.append('os_system')
