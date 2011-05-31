# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ openalea.function operator """
__revision__=" $Id$ "


from openalea.core import *

__name__ = "openalea.function operator"

__alias__ = ["catalog.functional", "openalea.functional"]

__version__ = '0.0.2'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Functional Node library.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = ['map_', 'filter_', 'reduce_', 'apply_', 'func']    


map_ = Factory( name="map",
               description="Apply a function on a sequence",
               category="Functional",
               inputs=(dict(name='func', interface=IFunction), 
                       dict(name='seq', interface=ISequence)),
               nodemodule="functional",
               nodeclass="pymap",
               )


filter_ = Factory( name="filter",
                   description="Apply a function on a sequence and return only true values",
                   category="Functional",
                   inputs=(dict(name='func', interface=IFunction), 
                           dict(name='seq', interface=ISequence)),

                   nodemodule="functional",
                   nodeclass="pyfilter",
                  )
    
reduce_ = Factory( name="reduce",
                   description="Apply a function of two arguments cumulatively to the items of a sequence",
                   category="Functional",
                   inputs=(dict(name='func', interface=IFunction), 
                           dict(name='seq', interface=ISequence)),
                   
                   nodemodule="functional",
                   nodeclass="pyreduce",
                   )


    
apply_ = Factory( name="apply",
              description="Apply a function with arguments",
              category="Functional",
              inputs=(dict(name='func', interface=IFunction), 
                      dict(name='seq', interface=ISequence)),
              
              nodemodule="functional",
              nodeclass="pyapply",
              )


func = Factory( name="function",
                description="Creates a function from a python string",
                category="Functional",
                nodemodule="functional",
                nodeclass="pyfunction",
                )
ifelse= Factory( name="ifelse",
                description="Execute two dataflow functions depending on a condition",
                category="Functional",
                   inputs=(dict(name='value',), 
                           dict(name='condition', interface=IBool), 
                           dict(name='function1', interface=IFunction), 
                           dict(name='function2', interface=IFunction), 
                           ),
                nodemodule="functional",
                nodeclass="pyifelse",
                )
