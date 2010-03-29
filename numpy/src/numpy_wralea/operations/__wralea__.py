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


__name__ = "openalea.numpy.math"
__alias__ = ["numpy.math"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'

__all__ = []

from openalea.core import Factory
from openalea.core.interface import *

list_type = ['bool', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'float96', 'complex64', 'complex128', 'complex192']


dot = Factory(name = "dot",
		description = "Dot product of two arrays",
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


cross = Factory(name = "cross",
		description = "Return the cross product of two (arrays of) vectors",
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
		description = "Return the cumulative product of elements along a given axis",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='axis', interface=IInt),
			  dict(name='dtype', interface=IEnumStr(list_type), value='float64'),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "cumprod",
		)

__all__.append("cumprod")


cumsum = Factory(name = "cumsum",
		description = "Return the cumulative sum of the elements along a given axis",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence),
			  dict(name='axis', interface=IInt),
			  dict(name='dtype', interface=IEnumStr(list_type), value='float64'),),
		outputs = (dict(name='array', interface= ISequence),),
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
                nodemodule = "math",
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


reshape = Factory(name = "reshape",
		description = "Gives a new shape to an array without changing its data",
		category = "numpy",
		inputs = (dict(name='array', interface=ISequence,
				showwidget=False),
			  dict(name='newshape', interface=ISequence),
			  dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
		outputs = (dict(name='array', interface= ISequence),),
                nodemodule = "numpy",
		nodeclass = "reshape",
		)

__all__.append("reshape")


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

