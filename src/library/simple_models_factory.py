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
                  parameters = ["A", "B"],
                  
                  )


    package.add_factory( nf )
    

    nf = Factory( name= "inputfile", 
                  description= "File name", 
                  category = "Data Types", 
                  nodemodule = "simple_models",
                  nodeclass = "InputFile",
                  
                  widgetmodule = None,
                  widgetclass = None,
                  parameters = ["Filename"],
                  
                  )


    package.add_factory( nf )


    nf = Factory( name= "bool", 
                  description= "boolean", 
                  category = "Data Types", 
                  nodemodule = "simple_models",
                  nodeclass = "Bool",
                  
                  widgetmodule = None,
                  widgetclass = None,
                  parameters = ["Bool"],
                  
                  )


    package.add_factory( nf )



    nf = Factory( name = "float",
                  description = "Float Value",
                  category  = "Data Types",
                  nodemodule = "simple_models",
                  nodeclass = "Float",
                  widgetmodule = None,
                  widgetclass = None,
                  parameters = ["val"]
                  )

                      
    package.add_factory( nf )
