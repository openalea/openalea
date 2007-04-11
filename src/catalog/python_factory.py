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
                  nodeclass = "getitem",
                  )

    package.add_factory( nf )


    nf = Factory( name = "setitem",
                  description = "Python __setitem__",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "setitem",
                  )

    package.add_factory( nf )


    nf = Factory( name = "delitem",
                  description = "Python __delitem__",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "delitem",
                  )

    package.add_factory( nf )



    nf = Factory( name = "append",
                  description = "Python append",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "append",
                  )
    
    package.add_factory( nf )


    nf = Factory( name = "keys",
                  description = "Python keys()",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "keys",
                  )

    package.add_factory( nf )

    
    nf = Factory( name = "values",
                  description = "Python values()",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "values",
                  )

    package.add_factory( nf )

    
    nf = Factory( name = "items",
                  description = "Python items()",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "items",
                  )

    package.add_factory( nf )



    nf = Factory( name = "range",
                  description = "Return an arithmetic progression of integers",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "pyrange",
                  )
    
    package.add_factory( nf )


    nf = Factory( name = "map",
                  description = "Apply a function on a sequence",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "pymap",
                  )
    
    package.add_factory( nf )
    

    nf = Factory( name = "filter",
                  description = "Apply a function on a sequence and return only true values",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "pyfilter",
                  )
    
    package.add_factory( nf )


    nf = Factory( name = "reduce",
                  description = "Apply a function of two arguments cumulatively to the items of a sequence",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "pyreduce",
                  )
    
    package.add_factory( nf )


    nf = Factory( name = "len",
                  description = "Return the number of items of a sequence or mapping.",
                  category  = "Python",
                  nodemodule = "python",
                  nodeclass = "pylen",
                  )
    
    package.add_factory( nf )


