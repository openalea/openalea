# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Core.Library 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core.external import *


def define_factory(package):
    """ Define factories for arithmetics nodes """



    nf = Factory( name= "linearmodel", 
                  description= "Linear Model", 
                  category = "Model", 
                  nodemodule = "simple_models",
                  nodeclass = "LinearModel",
                  
                  widgetmodule = None,
                  widgetclass = None,
                  
                  )


    package.add_factory( nf )
    

    nf = Factory( name= "inputfile", 
                  description= "File name", 
                  category = "Data Types", 
                  nodemodule = "simple_models",
                  nodeclass = "InputFile",
                  
                  widgetmodule = None,
                  widgetclass = None,
                 
                  )


    package.add_factory( nf )

    nf = Factory( name= "string", 
                  description= "String", 
                  category = "Data Types", 
                  nodemodule = "simple_models",
                  nodeclass = "String",
                  
                  widgetmodule = None,
                  widgetclass = None,
                 
                  )


    package.add_factory( nf )


    nf = Factory( name= "bool", 
                  description= "boolean", 
                  category = "Data Types", 
                  nodemodule = "simple_models",
                  nodeclass = "Bool",
                  
                  widgetmodule = None,
                  widgetclass = None,
                  
                  )


    package.add_factory( nf )


    nf = Factory( name = "float",
                  description = "Float Value",
                  category  = "Data Types",
                  nodemodule = "simple_models",
                  nodeclass = "Float",
                  widgetmodule = None,
                  widgetclass = None,
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "int",
                  description = "Int Value",
                  category  = "Data Types",
                  nodemodule = "simple_models",
                  nodeclass = "Int",
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "enumTest",
                  description = "String Enumeration",
                  category  = "Data Types",
                  nodemodule = "simple_models",
                  nodeclass = "EnumTest",
                  widgetmodule = None,
                  widgetclass = None,
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "rgb",
                  description = "RGB tuple",
                  category  = "Data Types",
                  nodemodule = "simple_models",
                  nodeclass = "RGB",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )

    nf = Factory( name = "map",
                  description = "Apply a function on a sequence",
                  category  = "Function",
                  nodemodule = "simple_models",
                  nodeclass = "Map",
                  )
    
    package.add_factory( nf )

    nf = Factory( name = "filter",
                  description = "Apply a function on a sequence and return only true values",
                  category  = "Function",
                  nodemodule = "simple_models",
                  nodeclass = "Filter",
                  )
    
    package.add_factory( nf )

    nf = Factory( name = "f(x) op g(x)",
                  description = "Create a function h: x-> f(x) op g(x)",
                  category  = "Function",
                  nodemodule = "simple_models",
                  nodeclass = "Generator",
                  )
    
    package.add_factory( nf )

    nf = Factory( name = "range",
                  description = "Return an arithmetic progression of integers",
                  category  = "Function",
                  nodemodule = "simple_models",
                  nodeclass = "Range",
                  )
    
    package.add_factory( nf )

    nf = Factory( name = "len",
                  description = "Return the number of items of a sequence or mapping.",
                  category  = "Function",
                  nodemodule = "simple_models",
                  nodeclass = "Len",
                  )
    
    package.add_factory( nf )
