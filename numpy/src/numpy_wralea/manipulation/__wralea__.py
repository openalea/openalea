# -*- python -*-
# -*- coding: latin-1 -*-
#
#       manipulation : numpy package
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

__name__ = "openalea.numpy.manipulation"

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []


flatten = Factory( name = "flatten", 
                description = "Return a copy of the array collapsed into one dimension", 
                category = "numpy",
                inputs = (  dict(name='array', interface=None),
                            dict(name='order', interface=IEnumStr(["C", "F"]), value="C"),),
                outputs = (dict(name='y', interface= None),),
                nodemodule = "manipulation",
                nodeclass = "wra_flatten",
              )

__all__.append("flatten")

unique = Factory( name = "unique", 
                description = "Find the unique elements of an array", 
                category = "numpy",
                inputs = (  dict(name='array', interface=None),
                            dict(name='return_index', interface=IBool, value=False),
                            dict(name='return_inverse', interface=IBool, value=False),),
                outputs = (dict(name='unique', interface= None),),
                nodemodule = "numpy",
                nodeclass = "unique",
              )

__all__.append("unique")

reshape = Factory(name = "reshape",
		description = "Gives a new shape to an array without changing its data",
		category = "numpy",
		inputs = (dict(name='array', interface=None,
				showwidget=False),
			  dict(name='newshape', interface=ITuple),
			  dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "reshape",
		)

__all__.append("reshape")

ravel = Factory(name = "ravel",
		description = "Return a flattened array",
		category = "numpy",
		inputs = (dict(name='array', interface=None),
			  dict(name='order', interface=IEnumStr(['C', 'F']),value='C'),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "ravel",
		)

__all__.append("ravel")

transpose = Factory(name = "transpose",
		description = "Permute the dimensions of an array",
		category = "numpy",
		inputs = (dict(name='array', interface=None),
			  dict(name='axes', interface=IInt, value=None),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "transpose",
		)

__all__.append("transpose")

vstack = Factory(name = "vstack",
		description = "Stack arrays in sequence vertically (row wise)",
		category = "numpy",
		inputs = (dict(name='array', interface=ITuple),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "vstack",
		)

__all__.append("vstack")

hstack = Factory(name = "hstack",
		description = "Stack arrays in sequence horizontally (column wise)",
		category = "numpy",
		inputs = (dict(name='array', interface=ITuple),),
		outputs = (dict(name='array', interface= None),),
                nodemodule = "numpy",
		nodeclass = "hstack",
		)

__all__.append("hstack")

