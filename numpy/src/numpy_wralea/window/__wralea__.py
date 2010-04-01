# -*- python -*-
# -*- coding: latin-1 -*-
#
#       operations : numpy package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA  
#
#       File author(s): Thomas Cokelaer <thomas.cokelaer@sophia.inria.fr>
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
#from openalea.core.interface import *


__name__ = "openalea.numpy.window"
__version__ = '0.99'
__license__ = 'CECILL-C'
__authors__ = 'Thomas Cokelaer, thomas.cokelaer@sophia.inria.fr'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping (window functions).'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__ = 'icon.png'

__all__ = ['window']

window = Factory(name = "window",  description = "window functions", category = "numpy", nodemodule = "vnumpy",  nodeclass = "window")



