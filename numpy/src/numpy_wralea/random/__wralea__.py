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


__doc__ = """ openalea.numpy.random """
__revision__ = " $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *


__name__ = "openalea.numpy.random"

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'

__all__ = []
    
rand = Factory(name = "rand",
    description = "Random values in a given shape.",
    authors=['Eric Moscardi'],
    category = "numpy",
    inputs = (dict(name='d', interface=IInt),),
    outputs = (dict(name='array', interface= None),),
    nodemodule = "vnumpy",
    nodeclass = "wra_rand",
    )

__all__.append("rand")

randn = Factory(name = "randn",
    description = "Return a sample (or samples) from the “standard normal” distribution.",
    authors=['Thomas Cokelaer','Eric Moscardi'],
    category = "numpy",
    inputs = (dict(name='n', interface=IInt),),
    outputs = (dict(name='array', interface= None),),
    nodemodule = "vnumpy",
    nodeclass = "wra_randn",
    )

__all__.append("randn")

random = Factory(name = "random",
    description = "Return random floats in the half-open interval [0.0, 1.0).",
    authors=['Eric Moscardi'],
    category = "numpy",
    inputs = (dict(name='size', interface=ITuple),),
    outputs = (dict(name='array', interface= None),),
    nodemodule = "vnumpy",
    nodeclass = "wra_random",
    )

__all__.append("random")

standard_normal = Factory(name = "standard_normal",
    description = "Returns samples from a Standard Normal distribution (mean=0, stdev=1).",
    authors='Eric Moscardi',
    category = "numpy",
    inputs = (dict(name='size', interface=ITuple),),
    outputs = (dict(name='array', interface= None),),
    nodemodule = "vnumpy",
    nodeclass = "wra_standard_normal",
    )

__all__.append("standard_normal")


uniform = Factory(name = "uniform",
    description = "Draw samples from a uniform distribution.",
    authors='Thomas Cokelaer',
    category = "numpy",
    inputs = (dict(name='low', interface=IFloat, value=0.0),
            dict(name='high', interface=IFloat, value=1.0),
            dict(name='size', interface=IInt, value=1)),
    outputs = (dict(name='ndarray', interface= None),),
    nodemodule = "vnumpy",
    nodeclass = "wra_uniform",
    )

__all__.append("uniform")
