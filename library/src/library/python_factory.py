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



    nf = Factory( name = "getitem",
                  description = "Python __getitem__",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "GetItem",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )

    nf = Factory( name = "setitem",
                  description = "Python __setitem__",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "SetItem",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )

    nf = Factory( name = "append",
                  description = "Python append",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "Append",
                  widgetmodule = None,
                  widgetclass = None,
                  )

    
    package.add_factory( nf )
