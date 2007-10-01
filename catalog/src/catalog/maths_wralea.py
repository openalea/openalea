# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
    metainfo = dict(version='0.0.1',
                    license='CECILL-C',
                    authors='OpenAlea Consortium',
                    institutes='INRIA/CIRAD',
                    description='Mathematical Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Math", metainfo)


    nf = Factory( name="==", 
                  description="Equality test", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_equal",
                  )

    package.add_factory(nf)


    nf = Factory( name=">", 
                  description="Greater than test", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_greater",
                  )

    package.add_factory(nf)


    nf = Factory( name=">=", 
                  description="greater or Equal test", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_greater_or_equal",
                  )

    package.add_factory(nf)


    nf = Factory( name="and", 
                  description="Boolean And", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_and",
                  )

    package.add_factory(nf)


    nf = Factory( name="or", 
                  description="Boolean Or", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_or",
                  )

    package.add_factory(nf)


    nf = Factory( name= "not", 
                  description="Boolean Not", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_not",
                  )

    package.add_factory(nf)

    nf = Factory( name="+", 
                  description="Addition", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_add",
                  )


    package.add_factory(nf)

    nf = Factory( name="-", 
                  description="Soustraction", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_sub",
                  )

    package.add_factory(nf)


    nf = Factory( name="*", 
                  description="Multiplication", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_mult",
                  )

    package.add_factory(nf)


    nf = Factory( name="/", 
                  description="Division", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_div",
                  )

    package.add_factory(nf)


    nf = Factory( name="abs", 
                  description="Absolute value", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_abs",
                  )


    package.add_factory(nf)

    nf = Factory( name="cmp", 
                  description="Compare 2 objects", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_cmp",
                  )


    package.add_factory(nf)


    nf = Factory( name="**", 
                  description="Power", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_pow",
                  )


    package.add_factory(nf)


    nf = Factory( name="cos", 
                  description="Cosinus", 
                  category="Math",
                  nodemodule="maths",
                  nodeclass="py_cos",
                  )

    package.add_factory(nf)

    nf = Factory( name="sin", 
                  description="Sinus", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_sin",
                  )

    package.add_factory(nf)

    nf = Factory( name="round", 
                  description="Round value", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_round",
                  )


    package.add_factory(nf)

    nf = Factory( name="min", 
                  description="Minimum of a sequence", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_min",
                  )


    package.add_factory(nf)

    nf = Factory( name="max", 
                  description="Maximum of a sequence", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_max",
                  )


    package.add_factory(nf)




    # Random function
    nf = Factory( name="randint", 
                  description="Random integer in range[a,b]", 
                  category="Math", 
                  nodemodule="random",
                  nodeclass="randint",
                  inputs=(dict(name='a', interface=IInt, value=0),
                          dict(name='b', interface=IInt, value=100),
                          ),
                  lazy = False,
                  )


    package.add_factory(nf)


    nf = Factory( name="random", 
                  description="Random float [0,1)", 
                  category="Math", 
                  nodemodule="random",
                  nodeclass="random",
                  lazy = False,
                  )


    package.add_factory(nf)

    nf = Factory( name="randlist", 
                  description="List of Random integer", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_randlist",
                  inputs=(dict(name='a', interface=IInt, value=0),
                          dict(name='b', interface=IInt, value=100),
                          dict(name='size', interface=IInt, value=10),
                          ),

                  lazy = False,
                  )


    package.add_factory(nf)

    pkgmanager.add_package(package)

