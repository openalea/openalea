# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): CHAUBERT Florence <florence.chaubert@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *
from openalea.plotools import plotable

import rpy
from scipy import stats
import scipy
import pylab

def random_continuous_law(law ,n , args):
    """
    Generate random values from continuous distribution

    :Parameters:
     - 'law': distribution to simulate
     - 'n' : number of random values
     - 'args': parameters of continuous distribution to simulate

     :Types:
     - 'law': string
     - 'n': int
     - 'args': float list

     :Returns the vector of the random values from continuous distributions
     :Returntype: float list

     :attention:  n must be greater than 0
     """

    if law == 'norm':
        res = rpy.r.rnorm(n, mean = args[0], sd = args[1])
    else:
        if law == 'unif':
            res = rpy.r.runif(n, args[0], args[1])
        else:
           if law == 'exp':
               res = rpy.r.rexp(n, rate = args[0])

    return (res,)

def random_discrete_law(law ,n , args):
    """
    Generate random values from discrete distribution

    :Parameters:
     - 'law': distribution to simulate
     - 'n' : number of random values
     - 'args': parameters of discrete distribution to simulate

     :Types:
     - 'law': string
     - 'n': int
     - 'args': float list

     :Returns the vector of the random values from discrete distributions
     :Returntype: float list

     :attention:  n must be greater than 0
     """

    if law == 'binom':
        res = rpy.r.rbinom(n, size = args[0], prob = args[1])
    else:
        if law == 'pois':
            res = rpy.r.rpois(n, args[0])
        else:
           if law == 'geom':
               res = rpy.r.rgeom(n, prob = args[0])

    return (res,)

