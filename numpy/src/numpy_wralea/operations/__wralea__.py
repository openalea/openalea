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


__name__ = "openalea.numpy.operations"
__alias__ = ["numpy.operations"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []

from openalea.core import Factory
from openalea.core.interface import *


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

