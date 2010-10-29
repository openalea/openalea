# -*- python -*-
# -*- coding: latin-1 -*-
#
#       math : numpy package
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

__license__ = "Cecill-C"
__revision__ = " $Id: $ "

def inv(array):
    from numpy import linalg
    return (linalg.inv(array))


def putmask(array, mask, values):
    import numpy as np
    return (np.putmask(array, mask, values))

def mean(array, axis=None, dtype=None):
    from numpy import mean
    return (mean(array, axis, dtype),)

def std(array, axis=None, dtype=None, ddof=0):
    from numpy import std
    return (std(a=array, axis=axis, dtype=dtype, ddof=ddof),)

def wra_sum(array, axis, dtype):
    from numpy import sum
    return (sum(a=array, axis=axis, dtype=dtype),)

wra_sum.__doc__ = sum.__doc__

def wra_min(array, axis):
    from numpy import min
    return (min(a=array, axis=axis),)

wra_min.__doc__ = min.__doc__

def wra_max(a, axis=None):
    from numpy import max
    return(max(a, axis=axis),)

wra_max.__doc__ = max.__doc__

