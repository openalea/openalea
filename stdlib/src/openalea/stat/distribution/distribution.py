# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
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

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core import *
from openalea.plotools import plotable

import rpy
from scipy import stats
import scipy
import pylab

__docformat__ = "restructuredtext en"

def random_continuous_law(law ,n , args):
    """
    Generate random values from continuous distribution

    :Parameters:
     - `law`: distribution to simulate
     - `n` : number of random values
     - `args`: parameters of continuous distribution to simulate

    :Types:
     - `law`: string
     - `n`: int
     - `args`: float list

    :returns: the vector of the random values from continuous distributions
    :returntype: float list

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


################# normal distribution ###############
def dnorm(x , mean, sd):
    """
    Give the density of a normal distribution

    :Parameters:
     - `x`: values
     - `mean` : mean of the normal distribution
     - `sd`: standard deviation of the normal distribution

    :Types:
     - `x`: float list
     - `mean`: float
     - `sd`: float

    :returns: the vector of the density of values from a specific normal distribution
    :returntype: float list

    :attention:  sd must be greater or equal than 0
    """

    res = rpy.r.dnorm(x, mean, sd)

    return (res,)

def pnorm(x , mean, sd):
    """
    Give the cumulative distribution of a normal distribution

    :Parameters:
     - `x`: values
     - `mean` : mean of the normal distribution
     - `sd`: standard deviation of the normal distribution

    :Types:
     - `x`: float list
     - `mean`: float
     - `sd`: float

    :returns: the vector of the cumulative probabilies of values from a specific normal distribution
    :returntype: float list

    :attention:  sd must be greater or equal than 0
    """

    res = rpy.r.pnorm(x, mean, sd)

    return (res,)

def rnorm(n ,mean , sd):
    """
    Generate random values from normal distribution

    :Parameters:
     - `n` : number of random values
     - `mean` : mean of the normal distribution
     - `sd`: standard deviation of the normal distribution

    :Types:
     - `n`: int
     - `mean`: float
     - `sd`: float

    :returns: the vector of the random values from normal distribution
    :returntype: float list

    :attention: n must be greater than 0
    :attention: sd must be greater or equal than 0
     """

    res = rpy.r.rnorm(n, mean, sd) 

    return (res,)

############## end section normal distribution ########

################# poisson distribution ###############
def dpois(x , lambd):
    """
    Give the density of a poisson distribution

    :Parameters:
     - `x`: values
     - `lambd` : parameter of poisson distribution

    :Types:
     - `x`: float list
     - `lambd` : float

    :returns: the vector of the density of values from a specific poisson distribution
    :returntype: float list

    :attention: lambd must be greater than 0
     """

    res = rpy.r.dpois(x, lambd)

    return (res,)

def ppois(x , lambd):
    """
    Give the cumulative distribution of a poisson distribution

    :Parameters:
     - `x`: values
     - `lambd` : parameter of poisson distribution

    :Types:
     - `x`: float list
     - `lambd` : float

    :returns: the vector of the cumulative probabilies of values from a specific poisson distribution
    :returntype: float list

    :attention:  lambd must be greater than 0
    """

    res = rpy.r.ppois(x, lambd)

    return (res,)

def rpois(n , lambd):
    """
    Generate random values from poisson distribution

    :Parameters:
     - `n` : number of random values
     - `lambd` : parameter of poisson distribution

    :Types:
     - `n`: int
     - `lambd`: float

    :returns: the vector of the random values from poisson distribution
    :returntype: float list

    :attention: n must be greater than 0
    :attention: lambd must be greater than 0
    """

    res = rpy.r.rpois(n, lambd) 

    return (res,)

############## end section poisson distribution ########



def random_discrete_law(law ,n , args):
    """
    Generate random values from discrete distribution

    :Parameters:
     - `law`: distribution to simulate
     - `n` : number of random values
     - `args`: parameters of discrete distribution to simulate

    :Types:
     - `law`: string
     - `n`: int
     - `args`: float list

    :returns: the vector of the random values from discrete distributions
    :returntype: float list

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


