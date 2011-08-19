# -*- python -*-
# -*- coding: latin-1 -*-
#
#       operations : numpy package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################


__doc__ = """ openalea.numpy """
__revision__ = " $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *


__name__ = "openalea.numpy.math"


__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'


__all__ = []


list_type = ['bool', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'float96', 'complex64', 'complex128', 'complex192']

# for the convolve function:
modes = ['full','valid','same']

std =  Factory(name = "std",
    description = "Compute the standard deviation along the specified axis",
    authors='Eric Moscardi',
    category = "numpy",
    inputs = (
        dict(name='array', interface=None),
        dict(name='axis', interface=IInt,  value=None),
        dict(name='dtype', interface=None, value=None),
        dict(name='ddof', interface=IInt, value=0),
        ),
    outputs = None,
    nodemodule="numpy_math",
    nodeclass = "std",
    )
__all__.append("std")

dot = Factory(name = "dot",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='array', interface=ISequence),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "dot",
		)

__all__.append("dot")


clip = Factory(name = "clip",
		description = "Clip (limit) the values in an array",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='a_min', interface=IFloat),
			  dict(name='a_max', interface=IFloat),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "clip",
		)

__all__.append("clip")

mul = Factory(name = "multiply",
              category = "numpy",
              inputs = (dict(name='array', interface=ISequence),
                        dict(name='array', interface=ISequence),),
              outputs = (dict(name='array', interface= ISequence),),
              nodemodule = "numpy",
              nodeclass = "multiply",
              )

__all__.append("mul")


cross = Factory(name = "cross",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
		          dict(name='array', interface=ISequence),
			  dict(name='axisa', interface=IInt, value=-1),
			  dict(name='axisb', interface=IInt, value=-1),
			  dict(name='axisc', interface=IInt, value=-1),
			  dict(name='axis', interface=IInt),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "cross",
		)

__all__.append("cross")


cumprod = Factory(name = "cumprod",
#		description = "Return the cumulative product of elements along a given axis",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='axis', interface=IInt),
			  dict(name='dtype', interface=IEnumStr(list_type), value='float64'),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "cumprod",
		)

__all__.append("cumprod")


convolve = Factory(name = "convolve",
    description = "Return the cumulative product of elements along a given axis",
    category = "numpy",
    inputs = (
                dict(name='array', interface=ISequence),
                dict(name='array', interface=ISequence),
                dict(name='mode', interface=IEnumStr(modes), value='full'),),
    outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
    nodeclass = "convolve",
    )
__all__.append("convolve")


cumsum = Factory(name = "cumsum",
		description = "Return the cumulative sum of the elements along a given axis",
		category = "numpy",
		inputs = (dict(name='array', interface=None),
			  dict(name='axis', interface=IInt),
			  dict(name='dtype', interface=IEnumStr(list_type), value='float64'),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "cumsum",
		)

__all__.append("cumsum")


diff = Factory(name = "diff",
		description = "Calculate the n-th order discrete difference along given axis",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='n', interface=IInt, value=1),
			  dict(name='axis', interface=IInt, value=1),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "diff",
		)

__all__.append("diff")


#digitize = Factory(name = "digitize",
#		description = "Return the indices of the bins to which each value in input array belongs",
#		category = "numpy",
#		inputs = (dict(name='array', interface=ISequence),
#			  dict(name='bins', interface=ISequence),),
#		outputs = (dict(name='array', interface= ISequence),),
#               nodemodule = "numpy",
#		nodeclass = "digitize",
#		)

#__all__.append("digitize")


outer = Factory(name = "outer",
		description = "Compute the outer product of two vectors",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
		          dict(name='array', interface=ISequence),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "outer",
		)

__all__.append("outer")


inv = Factory(name = "inv",
		description = "Compute the (multiplicative) inverse of a matrix",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy_math",
		nodeclass = "inv",
		)

__all__.append("inv")


#poly1d = Factory(name = "poly1d",
#		description = "A one-dimensional polynomial class",
#		category = "numpy",
#		inputs = (dict(name='array', interface=ISequence),
#		          dict(name='r', interface=IBool, value=False),
#		          dict(name='variable', interface=IStr, value=None),),
#		outputs = (dict(name='array', interface= ISequence),),
#               nodemodule = "numpy",
#		nodeclass = "poly1d",
#		)

#__all__.append("poly1d")


putmask = Factory(name = "putmask",
		description = "Changes elements of an array based on conditional and input values",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence,
				showwidget=False),
			  dict(name='mask', interface=ISequence),
			  dict(name='value', interface=ISequence),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "putmask",
		)

__all__.append("putmask")

tan = Factory(name = "tan",
    description = "  Compute tangent element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "tan",
    )
__all__.append("tan")


cos = Factory(name = "cos",
    description = "  Cosine element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "cos",
    )
__all__.append("cos")


sin = Factory(name = "sin",
    description = "  Sine tangent element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "sin",
    )
__all__.append("sin")


arcsin = Factory(name = "arcsin",
    description = "   Inverse sine elementwise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arcsin",
    )
__all__.append("arcsin")


arccos = Factory(name = "arccos",
    description = "   Trigonometric inverse cosine, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arccos",
    )
__all__.append("arccos")


arctan = Factory(name = "arctan",
    description = "   Trigonometric inverse tangent, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arctan",
    )
__all__.append("arctan")


degrees = Factory(name = "degrees",
    description = "  Convert angles from radians to degrees.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "degrees",
    )
__all__.append("degrees")


radians = Factory(name = "radians",
    description = "  Convert angles from degrees to radians.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "radians",
    )
__all__.append("radians")



deg2rad = Factory(name = "deg2rad",
    description = "  Convert angles from degrees to radians.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "deg2rad",
    )
__all__.append("deg2rad")


rad2deg = Factory(name = "rad2deg",
    description = "  Convert angles from radians to degrees.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "rad2deg",
    )
__all__.append("rad2deg")


sinh = Factory(name = "sinh",
    description = " Hyperbolic sine, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "sinh",
    )
__all__.append("sinh")


cosh = Factory(name = "cosh",
    description = " Hyperbolic cosine, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "cosh",
    )
__all__.append("cosh")


tanh = Factory(name = "tanh",
    description = " Compute hyperbolic tangent element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "tanh",
    )
__all__.append("tanh")


arcsinh = Factory(name = "arcsinh",
    description = "  Inverse hyperbolic sine elementwise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arcsinh",
    )
__all__.append("arcsinh")


arccosh = Factory(name = "arccosh",
    description = "  Inverse hyperbolic cosine, elementwise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arccosh",
    )
__all__.append("arccosh")


arctanh = Factory(name = "arctanh",
    description = "  Inverse hyperbolic tangent elementwise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "arctanh",
    )
__all__.append("arctanh")


rint = Factory(name = "rint",
    description = " Round elements of the array to the nearest integer.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "rint",
    )
__all__.append("rint")


floor = Factory(name = "floor",
    description = "    Return the floor of the input, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "floor",
    )
__all__.append("floor")


ceil = Factory(name = "ceil",
    description = " Return the ceiling of the input, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "ceil",
    )
__all__.append("ceil")


trunc = Factory(name = "trunc",
    description = "    Return the truncated value of the input, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "trunc",
    )
__all__.append("trunc")


exp = Factory(name = "exp",
    description = "  Calculate the exponential of all elements in the input array.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "exp",
    )
__all__.append("exp")


expm1 = Factory(name = "expm1",
    description = "    Calculate exp(x) - 1 for all elements in the array.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "expm1",
    )
__all__.append("expm1")


exp2 = Factory(name = "exp2",
    description = " Calculate 2**p for all p in the input array.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "exp2",
    )
__all__.append("exp2")


log = Factory(name = "log",
    description = "  Natural logarithm, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "log",
    )
__all__.append("log")


log10 = Factory(name = "log10",
    description = "    Return the base 10 logarithm of the input array, element-wise",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "log10",
    )
__all__.append("log10")


sqrt = Factory(name = "sqrt",
    description = " Return the positive square-root of an array, element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "sqrt",
    )
__all__.append("sqrt")


square = Factory(name = "square",
    description = "   Return the element-wise square of the input.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "square",
    )
__all__.append("square")


absolute = Factory(name = "absolute",
    description = " Calculate the absolute value element-wise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "absolute",
    )
__all__.append("absolute")


fabs = Factory(name = "fabs",
    description = " Compute the absolute values elementwise.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "fabs",
    )
__all__.append("fabs")


sign = Factory(name = "sign",
    description = " Returns an element-wise indication of the sign of a number.",
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "sign",
    )
__all__.append("sign")

sign = Factory(name = "power",
    description = "wralea to numpy.power function",
    authors='Thomas Cokelaer',
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        dict(name='power', interface=IFloat, showwidget=False),
        ),
    outputs = (dict(name='array', interface= ISequence),), nodemodule="numpy",
    nodeclass = "power",
    )
__all__.append("power")

mean = Factory(name = "mean",
    description = "wralea to numpy.mean function",
    authors='Thomas Cokelaer',
    category = "numpy",
    inputs = (
        dict(name='array', interface=ISequence, showwidget=False),
        dict(name='axis', interface=IInt,  value=None),
        dict(name='dtype', interface=None, value=None),
        ),
    outputs = None,
    nodemodule="numpy",
    nodeclass = "mean",
    )
__all__.append("mean")

sum = Factory(name = "sum",
    description = "Sum of array elements over a given axis",
    authors='Eric Moscardi',
    category = "numpy",
    inputs = (
        dict(name='array', interface=None),
        dict(name='axis', interface=IInt,  value=None),
        dict(name='dtype', interface=IEnumStr(list_type), value='float64')),
    outputs = None,
    nodemodule="numpy_math",
    nodeclass = "wra_sum",
    )
__all__.append("sum")

min = Factory(name = "min",
    description = "Return the minimum along an axis",
    authors='Eric Moscardi',
    category = "numpy",
    inputs = (
        dict(name='array', interface=None),
        dict(name='axis', interface=IInt,  value=None),),
    outputs = None,
    nodemodule="numpy_math",
    nodeclass = "wra_min",
    )
__all__.append("min")

max = Factory(name = "max",
                description = "Return the maximum along an axis",
                authors='Eric Moscardi',
                category = "numpy",
                inputs = (dict(name='array', interface=None),
                          dict(name='axis', interface=IInt, value=None),),
                outputs = (dict(name='out', interface= None),),
                nodemodule = "numpy_math",
                nodeclass = "wra_max",
              )

__all__.append("max")

add = Factory(name = "add",
                description = "Add arguments element-wise",
                authors='Eric Moscardi',
                category = "numpy",
                inputs = (dict(name='x1', interface=None),
                          dict(name='x2', interface=None),),
                outputs = (dict(name='out', interface= None),),
                nodemodule = "numpy",
                nodeclass = "add",
              )

__all__.append("add")

