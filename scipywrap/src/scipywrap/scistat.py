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
from scipy import stats


def ttest(x,y = [],mu=0):
    """
    Compute the Student's t-test

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values
     - 'y': an optional (non-empty) numeric vector of data values
     - 'mu': a number indicating the true value of the mean

    :Types:
     - 'x': float list
     - 'y': float list
     - 'mu': float

     :Returns the p-value of the Student t-test
     :Returntype: float list

     :attention: the 2 vectors must have the same size    
     """

    if y == [] :
        res = stats.stats.ttest_1samp(x,mu)
        TestType = 'One sample'
    else:
        res = stats.stats.ttest_ind(x,y)
        TestType = 'Two independent samples'

    pvalue = res[1]
    statistic = res[0]
    
    data = {'Test type': TestType, 'p.value':pvalue, 't.statistic':statistic} 
    return data


def kstest(x,y = [], cdf = '', args=[]):
    """
    Compute the Kolmogorov-Smirnov test

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values
     - 'y': an optional (non-empty) numeric vector of data values
     - 'cdf': a string to define the cumulative distribution to compare
     - 'args': parameters of cdf

    :Types:
     - 'x': float list
     - 'y': float list
     - 'cdf': string
     - 'args': float list

     :Returns the p-value of the Kolmogoros-Smirnov test
     :Returntype: dict

     """

    print x


    if y == [] :
        res = stats.stats.kstest(x,cdf=cdf,args=args)
        TestType = 'One sample'
    else:
        res = stats.stats.ks_2samp(x,y)
        TestType = 'Two samples'

    pvalue = res[1]
    statistic = res[0]
    
    data = {'Test type': TestType, 'p.value':pvalue, 't.statistic':statistic} 
    return data   
