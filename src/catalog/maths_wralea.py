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



def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library

    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package = Package("Catalog.Maths", metainfo)


    nf = Factory( name= "==", 
                  description= "Equality test", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "Equal",
                  )

    package.add_factory( nf )


    nf = Factory( name= ">", 
                  description= "Greater than test", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "Greater",
                  )

    package.add_factory( nf )


    nf = Factory( name= ">=", 
                  description= "greater or Equal test", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "GreaterOrEqual",
                  )

    package.add_factory( nf )

    nf = Factory( name= "and", 
                  description= "Boolean And", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "And",
                  )

    package.add_factory( nf )

    nf = Factory( name= "or", 
                  description= "Boolean Or", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "Or",
                  )

    package.add_factory( nf )

    nf = Factory( name= "not", 
                  description= "Boolean Not", 
                  category = "Condition", 
                  nodemodule = "maths",
                  nodeclass = "Not",
                  )

    package.add_factory( nf )

    nf = Factory( name= "+", 
                  description= "Addition", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Add",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "-", 
                  description= "Soustraction", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Sub",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "*", 
                  description= "Multiplication", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Mult",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "/", 
                  description= "Division", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Div",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "abs", 
                  description= "Absolute value", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Abs",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "cmp", 
                  description= "Compare 2 objects", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Cmp",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "**", 
                  description= "Power", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Pow",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )


    nf = Factory( name= "round", 
                  description= "Round value", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Round",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "min", 
                  description= "Minimum of a sequence", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Min",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "max", 
                  description= "Maximum of a sequence", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Max",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "randint", 
                  description= "Random integer", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "RandInt",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    nf = Factory( name= "print", 
                  description= "Console output", 
                  category = "Operations", 
                  nodemodule = "maths",
                  nodeclass = "Print",
                  widgetmodule = None,
                  widgetclass = None,
                  )


    package.add_factory( nf )

    pkgmanager.add_package(package)

