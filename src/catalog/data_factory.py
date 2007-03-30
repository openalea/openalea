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
__revision__=" $Id: simple_models_factory.py 302 2007-01-29 17:54:57Z pradal $ "


from openalea.core import *


def define_factory(package):

    nf = Factory( name= "inputfile", 
                  description= "File name", 
                  category = "Data Types", 
                  nodemodule = "data",
                  nodeclass = "InputFile",
                  
                  widgetmodule = None,
                  widgetclass = None,
                 
                  )


    package.add_factory( nf )

    nf = Factory( name= "string", 
                  description= "String", 
                  category = "Data Types", 
                  nodemodule = "data",
                  nodeclass = "String",
                  
                  widgetmodule = None,
                  widgetclass = None,
                 
                  )


    package.add_factory( nf )


    nf = Factory( name= "bool", 
                  description= "boolean", 
                  category = "Data Types", 
                  nodemodule = "data",
                  nodeclass = "Bool",
                  
                  widgetmodule = None,
                  widgetclass = None,
                  
                  )


    package.add_factory( nf )


    nf = Factory( name = "float",
                  description = "Float Value",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "Float",
                  widgetmodule = None,
                  widgetclass = None,
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "int",
                  description = "Int Value",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "Int",
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "enumTest",
                  description = "String Enumeration",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "EnumTest",
                  widgetmodule = None,
                  widgetclass = None,
                  )

                      
    package.add_factory( nf )


    nf = Factory( name = "rgb",
                  description = "RGB tuple",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "RGB",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )


    
    nf = Factory( name = "list",
                  description = "Python list",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "List",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )


    nf = Factory( name = "dict",
                  description = "Python dictionary",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "Dict",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )


    nf = Factory( name = "tuple2",
                  description = "Python 2 uple",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "Tuple2",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )

    nf = Factory( name = "list9",
                  description = "Create a list with lots of elements.",
                  category  = "Data Types",
                  nodemodule = "data",
                  nodeclass = "List9",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )

