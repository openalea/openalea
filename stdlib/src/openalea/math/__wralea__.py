# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__= """catalog.math """

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core.external import *
import math

__name__ = "openalea.math"
__alias__ = ["catalog.math"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Mathematical Node library.'
__url__ = 'http://openalea.gforge.inria.fr'


__all__= []

equal = Factory( name="==", 
        description="Equality test", 
        category="Math",
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="eq",
        )

__all__.append('equal')


diff = Factory( name="!=", 
        description="Equality test", 
        category="Math",
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="ne",
        )
__all__.append('diff')




sup = Factory( name=">", 
        description="Greater than test", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="gt",
        )

__all__.append('sup')


supeq = Factory( name=">=", 
        description="greater or Equal test", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="ge",
        )

__all__.append('supeq')

inf = Factory( name="<", 
        description="Lesser than test", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="lt",
        )

__all__.append('inf')


infeq = Factory( name="<=", 
        description="Less or Equal test", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="le",
        )

__all__.append('infeq')

and_ = Factory( name="and", 
               description="Boolean And", 
               category="Math", 
               inputs=(dict(name="a", interface=IBool, value=True), 
                       dict(name="b", interface=IBool, value=True),),
               nodemodule="operator",
               nodeclass="and_",
               )

__all__.append('and_')


or_ = Factory( name="or", 
        description="Boolean Or", 
        category="Math", 
        inputs=(dict(name="a", interface=IBool, value=True), 
            dict(name="b", interface=IBool, value=True),),
        nodemodule="operator",
        nodeclass="or_",
        )


__all__.append('or_')

xor_ = Factory( name="xor", 
        description="Boolean XOR", 
        category="Math",
        inputs=(dict(name="a", interface=IBool, value=True), 
            dict(name="b", interface=IBool, value=True),),
        nodemodule="operator",
        nodeclass="xor",
        )

__all__.append('xor_')

not_ = Factory( name= "not", 
        description="Boolean Not", 
        category="Math", 
        inputs=(dict(name="a", interface=IBool, value=True),),
        nodemodule="operator",
        nodeclass="not_",
        )

__all__.append('not_')


plus = Factory( name="+", 
        description="Addition", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="add",
        )

__all__.append('plus')


minus = Factory( name="-", 
        description="Soustraction", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),

        nodemodule="operator",
        nodeclass="sub",
        )

__all__.append('minus')


neg = Factory( name="neg", 
        description="Negative", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), ),
        nodemodule="operator",
        nodeclass="neg",
        )

__all__.append('neg')


times = Factory( name="*", 
        description="Multiplication", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="mul",
        )

__all__.append('times')


div = Factory( name="/", 
        description="Division", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=1),),

        nodemodule="operator",
        nodeclass="div",
        )

__all__.append('div')


mod = Factory( name="%", 
        description="Modulo", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0), 
            dict(name="b", interface=IInt, value=0),),

        nodemodule="operator",
        nodeclass="mod",
        )

__all__.append('mod')


abs = Factory( name="abs", 
        description="Absolute value", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=0),),
        nodemodule="operator",
        nodeclass="abs",
        )

__all__.append('abs')


cmp = Factory( name="cmp", 
        description="Compare 2 objects", 
        category="Math", 
        nodemodule="maths",
        nodeclass="py_cmp",
        )

__all__.append('cmp')


pow = Factory( name="**", 
        description="Power", 
        category="Math", 
        inputs=(dict(name="a", interface=IInt, value=1), 
            dict(name="b", interface=IInt, value=1),),
        nodemodule="operator",
        nodeclass="pow",
        )


# Trigonometry
cos = Factory( name="cos", 
        description="Cosinus", 
        category="Math",
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="cos",
        )

__all__.append('cos')


sin = Factory( name="sin", 
        description="Sinus", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="sin",
        )

__all__.append('sin')


tan = Factory( name="tan", 
        description="Tangent", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="tan",
        )

__all__.append('tan')


acos = Factory( name="acos", 
        description="Arccosinus", 
        category="Math",
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="acos",
        )

__all__.append('acos')


asin = Factory( name="asin", 
        description="Arcsinus", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="asin",
        )

__all__.append('asin')


atan = Factory( name="atan", 
        description="Arctangent", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="atan",
        )

__all__.append('atan')


radians = Factory( name="radians", 
        description="Degrees to radians converter", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="radians",
        )

__all__.append('radians')


degrees = Factory( name="degrees", 
        description="Radians to degrees converter", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="degrees",
        )

__all__.append('degrees')


round = Factory( name="round", 
        description="Round value", 
        category="Math", 
        nodemodule="maths",
        nodeclass="py_round",
        )

__all__.append('round')


floor = Factory( name="floor", 
        description="floor of x", 
        category="Math", 
        inputs=(dict(name="x", interface=IFloat, value=0.),),
        outputs=(dict(name="y", interface=IFloat), ),
        nodemodule="math",
        nodeclass="floor",
        )

__all__.append('floor')


ceil = Factory( name="ceil", 
        description="Ceil of x", 
        category="Math", 
        inputs=(dict(name="x", interface=IFloat, value=0.),),
        outputs=(dict(name="y", interface=IInt), ),
        nodemodule="math",
        nodeclass="ceil",
        )

__all__.append('ceil')


sqrt = Factory( name="sqrt", 
        description="Square root", 
        category="Math", 
        inputs=(dict(name="x", interface=IFloat, value=0.),),
        nodemodule="math",
        nodeclass="sqrt",
        )

__all__.append('sqrt')


log10 = Factory( name="log10", 
        description="Base 10 logarithm", 
        category="Math", 
        inputs=(dict(name="x", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="log10",
        )

__all__.append('log10')


log = Factory( name="log", 
        description="Logarithm", 
        category="Math", 
        inputs=(dict(name="a", interface=IFloat, value=0.), 
            dict(name="base", interface=IFloat, value=math.e),),
        nodemodule="math",
        nodeclass="log",
        )

__all__.append('log')


exp = Factory( name="exp", 
        description="Exponential", 
        category="Math", 
        inputs=(dict(name="x", interface=IFloat, value=0.), ),
        nodemodule="math",
        nodeclass="exp",
        )

__all__.append('exp')


min = Factory( name="min", 
        description="Minimum of a sequence", 
        category="Math", 
        nodemodule="maths",
        nodeclass="py_min",
        )

__all__.append('min')



max = Factory( name="max", 
        description="Maximum of a sequence", 
        category="Math", 
        nodemodule="maths",
        nodeclass="py_max",
        )

__all__.append('max')



# Random function
randint = Factory( name="randint", 
        description="Random integer in range[a,b]", 
        category="Math", 
        nodemodule="random",
        nodeclass="randint",
        inputs=(dict(name='a', interface=IInt, value=0),
            dict(name='b', interface=IInt, value=100),
            ),
        lazy = False,
        )

__all__.append('randint')



random = Factory( name="random", 
        description="Random float [0,1)", 
        category="Math", 
        nodemodule="random",
        nodeclass="random",
        lazy = False,
        )

__all__.append('random')


randlist = Factory( name="randlist", 
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


__all__.append('randlist')

