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
__revision__=" $Id: simple_models_factory.py 299 2007-01-29 10:30:01Z pradal $ "


from openalea.core.external import *


def define_factory(package):
    """ Define factories for arithmetics nodes """



    nf = Factory( name= "ax+b", 
                  description= "Linear function", 
                  category = "Function", 
                  nodemodule = "python_function",
                  nodeclass = "Linear",
                  )


    package.add_factory( nf )
    

    nf = Factory( name = "f op g",
                  description = "Create a function h: x-> f(x) op g(x)",
                  category  = "Function",
                  nodemodule = "python_function",
                  nodeclass = "Generator",
                  )
    
    package.add_factory( nf )


