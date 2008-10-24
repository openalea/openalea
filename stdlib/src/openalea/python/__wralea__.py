# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ openalea.python """
__revision__ = " $Id$ "


from openalea.core import *


__name__ = "openalea.python"
__alias__ = ["catalog.python"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Python Node library.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []

# Factories
ifelse = Factory(name="ifelse", 
                 description="Condition", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_ifelse",
                 )


__all__.append('ifelse')

getitem = Factory( name="getitem",
                   description="Python __getitem__",
                   category="Python",
                   
                   inputs=[dict(name="a", interface=None), 
                           dict(name="b", interface=None, value=0),],
                   nodemodule="python",
                   nodeclass="py_getitem",
                   widgetmodule="python",
                   widgetclass="ListSelectorWidget",
                   )

__all__.append('getitem')


setitem = Factory(name="setitem",
                  description="Python __setitem__",
                  category="Python",
                  inputs=[dict(name="a", interface=None), dict(name="b", interface=None),],
                  nodemodule="operator",
                  nodeclass="setitem",
                  )

__all__.append('setitem')


delitem = Factory(name="delitem",
                 description="Python __delitem__",
                 category="Python",
                 nodemodule="python",
                 nodeclass="delitem",
                 )

__all__.append('delitem')


keys = Factory( name="keys",
                description="Python keys()",
                category="Python",
                nodemodule="python",
                nodeclass="keys",
                )

__all__.append('keys')

    
values = Factory(name="values",
                 description="Python values()",
                 category="Python",
                 nodemodule="python",
                 nodeclass="values",
                 )


__all__.append('values')

    
items = Factory(name="items",
                 description="Python items()",
                 category="Python",
                 nodemodule="python",
                 nodeclass="items",
                 )

__all__.append('items')

range_ = Factory(name="range",
                 description="Returns an arithmetic progression of integers",
                 category="Python",
                 nodemodule="python",
                 nodeclass="pyrange",
                 )
    

__all__.append('range_')


enum_ = Factory(name="enumerate",
                description="Returns a python enumerate object.",
                category="Python",
                nodemodule="python",
                nodeclass="pyenumerate",
                )
    
__all__.append('enum_')


len_ = Factory(name="len",
                 description="Returns the number of items of a sequence or mapping.",
                 category="Python",
                 nodemodule="python",
                 nodeclass="pylen",
                 )


__all__.append('len_')
    

print_ = Factory(name="print", 
                 description="Console output", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_print",
                 outputs=(),
                 lazy=False,
                 )


__all__.append('print_')


method_ = Factory(name="method", 
                  description="Calls object method", 
                  category="Python", 
                  nodemodule="python",
                  nodeclass="py_method",
                  )

__all__.append('method_')

    
    
getattr_ = Factory( name="getattr",
                    description="Gets class attribute",
                    category="Python",
                    nodemodule="python",
                    nodeclass="py_getattr",
                    
                    inputs=(dict(name="IN0", interface=None),
                            dict(name="class_attribute_name", interface=IStr)),
                    outputs=(dict(name="class_attribute", interface=None),),
                    )

__all__.append('getattr_')


eval_ = Factory( name="eval",
                  description="Eval str as python expression",
                  category="Python",
                  nodemodule="python",
                  nodeclass="py_eval",

                  inputs=(dict(name="expression", interface=ITextStr),),
                  outputs=(dict(name="result", interface=None),),
                  )


__all__.append('eval_')

exec_ = Factory( name="exec",
                  description="Exec str as python code",
                  category="Python",
                  nodemodule="python",
                  nodeclass="py_exec",

                  inputs=(dict(name="code", interface=ITextStr),),
                  outputs=(),
                  )


__all__.append('exec_')


zip_ = Factory( name="zip", 
                description="Zip 2 sequences", 
                category="Python", 
                nodemodule="python",
                nodeclass="py_zip",
                )


__all__.append('zip_')

flatten_ = Factory( name="flatten", 
              description="flatten list", 
              category="Python", 
              nodemodule="python",
              nodeclass="py_flatten",
              )


__all__.append('flatten_')

extract_ = Factory( name= "extract", 
                  description= "Extract element from a list or a dict", 
                  category = "Python", 
                  nodemodule = "python",
                  nodeclass = "extract",
                  inputs = [dict(name='indexable' , interface=ISequence, value=[]),
                            dict(name='keys' , interface=ISequence, value=[])
                            ],
                  outputs = [dict(name='list' , interface=ISequence)],
                    )

__all__.append('extract_')

pysum = Factory( name = "sum",
                 description= sum.__doc__, 
                 category = "Python", 
                 nodemodule = "python",
                 nodeclass = "pysum",
                 inputs = [dict(name='sequence' , interface=ISequence, value=[]),],
                 outputs = [dict(name='value')],
               )
__all__.append('pysum')

# DEPRECATED
fwrite = Factory(name="fwrite", 
                 description="File output", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_fwrite",
                 inputs=(dict(name="x", interface=IStr),
                         dict(name="filename", interface=IFileStr),
                         dict(name="mode", interface=IStr, value="w"),
                         ),
                 outputs=(),
                 lazy=False,
                 )

__all__.append('fwrite_')


fread = Factory(name="fread", 
                description="File input", 
                category="Python", 
                nodemodule="python",
                nodeclass="FileRead",
                inputs=(dict(name="filename", interface=IFileStr),
                        ),
                outputs=(dict(name="string", interface=IStr),),
                lazy = False,
                )



__all__.append('fread')
