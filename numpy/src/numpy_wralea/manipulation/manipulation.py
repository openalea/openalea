# -*- python -*-
#
#       numpy: infos
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
"""

__license__= "Cecill-C"
__revision__ = " $Id $ "

import numpy as np

def wra_flatten(a, order='C'):
    return(a.flatten(order),)

wra_flatten.__doc__ = np.ndarray.flatten.__doc__
