# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__= """ Catalog.Math """

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
import math

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
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="eq",
                  )
    
    package.add_factory(nf)

    nf = Factory( name="!=", 
                  description="Equality test", 
                  category="Math",
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="ne",
                  )

    package.add_factory(nf)


    nf = Factory( name=">", 
                  description="Greater than test", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="ge",
                  )

    package.add_factory(nf)


    nf = Factory( name=">=", 
                  description="greater or Equal test", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="ge",
                  )

    package.add_factory(nf)


    nf = Factory( name="and", 
                  description="Boolean And", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IBool, value=True), 
                          dict(name="b", interface=IBool, value=True),),
                  nodemodule="operator",
                  nodeclass="and_",
                  )

    package.add_factory(nf)


    nf = Factory( name="or", 
                  description="Boolean Or", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IBool, value=True), 
                          dict(name="b", interface=IBool, value=True),),
                  nodemodule="operator",
                  nodeclass="or_",
                  )

    package.add_factory(nf)

    nf = Factory( name="xor", 
                  description="Boolean XOR", 
                  category="Math",
                  inputs=(dict(name="a", interface=IBool, value=True), 
                          dict(name="b", interface=IBool, value=True),),
                  nodemodule="operator",
                  nodeclass="xor",
                  )

    package.add_factory(nf)


    nf = Factory( name= "not", 
                  description="Boolean Not", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IBool, value=True),),
                  nodemodule="operator",
                  nodeclass="not_",
                  )

    package.add_factory(nf)

    nf = Factory( name="+", 
                  description="Addition", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="add",
                  )


    package.add_factory(nf)

    nf = Factory( name="-", 
                  description="Soustraction", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  
                  nodemodule="operator",
                  nodeclass="sub",
                  )

    package.add_factory(nf)

    nf = Factory( name="neg", 
                  description="Negative", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), ),
                  nodemodule="operator",
                  nodeclass="neg",
                  )

    package.add_factory(nf)

    nf = Factory( name="*", 
                  description="Multiplication", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="mul",
                  )

    package.add_factory(nf)


    nf = Factory( name="/", 
                  description="Division", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=1),),
                  
                  nodemodule="operator",
                  nodeclass="div",
                  )

    package.add_factory(nf)

    nf = Factory( name="%", 
                  description="Modulo", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0), 
                          dict(name="b", interface=IInt, value=0),),
                  
                  nodemodule="operator",
                  nodeclass="mod",
                  )

    package.add_factory(nf)


    nf = Factory( name="abs", 
                  description="Absolute value", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IInt, value=0),),
                  nodemodule="operator",
                  nodeclass="abs",
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
                  inputs=(dict(name="a", interface=IInt, value=1), 
                          dict(name="b", interface=IInt, value=1),),
                  nodemodule="operator",
                  nodeclass="pow",
                  )

    package.add_factory(nf)

    # Trigonometry
    nf = Factory( name="cos", 
                  description="Cosinus", 
                  category="Math",
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="cos",
                  )

    package.add_factory(nf)


    nf = Factory( name="sin", 
                  description="Sinus", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="sin",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="tan", 
                  description="Tangent", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="tan",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="acos", 
                  description="Arccosinus", 
                  category="Math",
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="acos",
                  )

    package.add_factory(nf)


    nf = Factory( name="asin", 
                  description="Arcsinus", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="asin",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="atan", 
                  description="Arctangent", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="atan",
                  )

    package.add_factory(nf)


    nf = Factory( name="radians", 
                  description="Degrees to radians converter", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="radians",
                  )

    package.add_factory(nf)


    nf = Factory( name="degrees", 
                  description="Radians to degrees converter", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="degrees",
                  )

    package.add_factory(nf)


    nf = Factory( name="round", 
                  description="Round value", 
                  category="Math", 
                  nodemodule="maths",
                  nodeclass="py_round",
                  )


    package.add_factory(nf)


    nf = Factory( name="floor", 
                  description="floor of x", 
                  category="Math", 
                  inputs=(dict(name="x", interface=IFloat, value=0.),),
                  outputs=(dict(name="y", interface=IFloat), ),
                  nodemodule="math",
                  nodeclass="floor",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="ceil", 
                  description="Ceil of x", 
                  category="Math", 
                  inputs=(dict(name="x", interface=IFloat, value=0.),),
                  outputs=(dict(name="y", interface=IInt), ),
                  nodemodule="math",
                  nodeclass="ceil",
                  )


    package.add_factory(nf)


    nf = Factory( name="sqrt", 
                  description="Square root", 
                  category="Math", 
                  inputs=(dict(name="x", interface=IFloat, value=0.),),
                  nodemodule="math",
                  nodeclass="sqrt",
                  )

    package.add_factory(nf)


    nf = Factory( name="log10", 
                  description="Base 10 logarithm", 
                  category="Math", 
                  inputs=(dict(name="x", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="log10",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="log", 
                  description="Logarithm", 
                  category="Math", 
                  inputs=(dict(name="a", interface=IFloat, value=0.), 
                          dict(name="base", interface=IFloat, value=math.e),),
                  nodemodule="math",
                  nodeclass="log",
                  )

    package.add_factory(nf)

    
    nf = Factory( name="exp", 
                  description="Exponential", 
                  category="Math", 
                  inputs=(dict(name="x", interface=IFloat, value=0.), ),
                  nodemodule="math",
                  nodeclass="exp",
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

