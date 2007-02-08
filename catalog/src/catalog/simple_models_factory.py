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


from openalea.core import *


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
    



