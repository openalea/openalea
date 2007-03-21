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



    nf = Factory( name= "add", 
                  description= "Addition", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Add",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "sub", 
                  description= "Soustraction", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Sub",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "mult", 
                  description= "Multiplication", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Mult",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "div", 
                  description= "Division", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Div",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "abs", 
                  description= "Absolute value", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Abs",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "cmp", 
                  description= "Compare 2 objects", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Cmp",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "pow", 
                  description= "Power", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Pow",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "round", 
                  description= "Round value", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Round",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "min", 
                  description= "Minimum of a sequence", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Min",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "max", 
                  description= "Maximum of a sequence", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Max",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "randint", 
                  description= "Random integer", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "RandInt",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "print", 
                  description= "Console output", 
                  category = "Operations", 
                  nodemodule = "arithmetics",
                  nodeclass = "Print",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )
