# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : numpy package
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

import numpy as np

def wra_array(array, dtype, copy, order, subok, ndim):
    return (np.array(array, dtype=dtype, copy=copy, order=order, subok=subok, ndmin=ndim))

def zeros(shape, dtype, order):
    return (np.zeros(shape, dtype=dtype, order=order))

def ones(shape, dtype, order):
    return (np.ones(shape, dtype=dtype, order=order))

def empty(shape, dtype, order):
    return (np.empty(shape, dtype=dtype, order=order))

def arange(start, stop, step, dtype):
    return (np.arange(start, stop, step, dtype=dtype))

def linspace(start, stop, num, endpoint, retstep):
    return (np.linspace(start, stop, num=num, endpoint=endpoint, retstep=retstep))

def wra_fromfunction(f, shape, dtype):
    return (np.fromfunction(f,shape,dtype=dtype))
