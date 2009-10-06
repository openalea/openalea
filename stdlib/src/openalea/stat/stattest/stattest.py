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

from openalea.core import Node
#from openalea.plotools import plotable

try:
    import rpy2.rpy_classic as rpy
    rpy.set_default_mode(rpy.BASIC_CONVERSION)

except:
    import rpy

#import numpy
from scipy import stats
#import scipy
#import pylab

__docformat__ = "restructuredtext en"

def chisqtest(x, y = [], p = []):
    """
    Compute the Chi-square test

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values
     - `y`: an optional (non-empty) numeric vector of data values
     - `p`: an optional (non_empty) numeric vector of probabilities

    :Types:
     - `x`: float list
     - `y`: float list
     - `p`: float list

    :returns: the p-value of the Chi-square test
    :returntype: float list

    :attention: the 2 vectors must have the same size and the sum of probabilities must be equal to 1   
    """
    
    if p == []:
        p = rpy.r.rep(1./len(x), len(x))
        
    if y == []:
        res = rpy.r.chisq_test(x, p=p)
        TestType = 'Chi-square goodness-of-fit test'
    else:
        res = rpy.r.chisq_test(x, y)
        TestType = "Chi-square test for contingency table, chi-square test" + \
            "for independence"

    pvalue = res['p.value']
    statistic = res['statistic']['X-squared']
    
    data = {'Test Type':TestType, 'p.value':pvalue, 'X-squared':statistic} 
    return data

def ttest(x, y = [],mu=0):
    """
    Compute the Student's t-test

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values
     - `y`: an optional (non-empty) numeric vector of data values
     - `mu`: a number indicating the true value of the mean

    :Types:
     - `x`: float list
     - `y`: float list
     - `mu`: float

    :returns: the p-value of the Student t-test
    :returntype: float list

    :attention: the 2 vectors must have the same size    
    """

    if y == [] :
        res = stats.stats.ttest_1samp(x, mu)
        TestType = 'One sample'
    else:
        res = stats.stats.ttest_ind(x, y)
        TestType = 'Two independent samples'

    pvalue = res[1]
    statistic = res[0]
    
    data = {'Test type': TestType, 'p.value':pvalue, 't.statistic':statistic} 
    return data


def kstest(x, y = [], cdf = '', args=[]):
    """
    Compute the Kolmogorov-Smirnov test

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values
     - `y`: an optional (non-empty) numeric vector of data values
     - `cdf`: a string to define the cumulative distribution to compare
     - `args`: parameters of cdf

    :Types:
     - `x`: float list
     - `y`: float list
     - `cdf`: string
     - `args`: float list

    :returns: the p-value of the Kolmogoros-Smirnov test
    :returntype: dict

    """

    if y == [] :
        res = stats.stats.kstest(x, cdf=cdf, args=args)
        TestType = 'One sample'
    else:
        res = stats.stats.ks_2samp(x, y)
        TestType = 'Two samples'

    pvalue = res[1]
    statistic = res[0]
    
    data = {'Test type': TestType, 'p.value':pvalue, 'ks.statistic':statistic} 
    return data   
