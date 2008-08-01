# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ catalog.functional """
__revision__=" $Id$ "


from openalea.core import *

__name__ = "openalea.functional"

__alias__ = ["catalog.functional"]

__version__ = '0.0.1'
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
                inputs = (dict(name="func_str",interface=ITextStr),),
                )


#     nf = Factory( name="ax+b", 
#                   description="Linear function", 
#                   category="Functional", 
#                   nodemodule="functional",
#                   nodeclass="Linear",
#                   )


#     package.add_factory( nf )
    

#     nf = Factory( name="f op g",
#                   description="Create a function h: x-> f(x) op g(x)",
#                   category="Functional",
#                   nodemodule="functional",
#                   nodeclass="Generator",
#                   )
    
#     package.add_factory(nf)








