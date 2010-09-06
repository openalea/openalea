# -*- python -*-
# -*- coding: latin-1 -*-
#
#    operations : numpy package
#
#    Copyright 2006 - 2010 INRIA - CIRAD - INRA
#
#    File author(s): Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
#                    Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#    Distributed under the Cecill-C License.
#    See accompanying file LICENSE.txt or copy at
#        http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#    OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################


__doc__ = """ openalea.numpy.io """
__revision__ = " $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *


__name__ = "openalea.numpy.io"

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'

__all__ = []


#save = Factory(name = "save",
#    description = "Save an array to a binary file in NumPy .npy format.",
#    category = "numpy",
#    inputs = (dict(name='filename', interface=IFileStr), dict(name='array', interface=ISequence)),
#    nodeclass = "save",
#)
#__all__.append("save")


mmap = ['r+', 'r', 'w+', 'c']
load = Factory( name = "load",
                description = "Load a pickled, .npy, or .npz binary file.",
                category = "numpy",
                inputs = (  dict(name='filename', interface= IFileStr), 
                            dict(name='mmap_mode', interface= IEnumStr(mmap))),
                outputs = (dict(name='array', interface= None),), 
                nodemodule = "numpy",
                nodeclass = "load",
                )
__all__.append("load")

#this one needs a little bit of work to have dynamic number args 
savez = Factory(name = "savez",
    description = "Save several arrays into a single, compressed file in .npz format.",
    category = "numpy",
    inputs = (dict(name='filename', interface=IStr), dict(name='array', interface=ISequence)),
    nodeclass = "savez",
)
