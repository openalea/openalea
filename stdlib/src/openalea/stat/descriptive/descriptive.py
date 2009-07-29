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
"""Set of statistical functions"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core import *
from openalea.plotools import plotable

try:
    import rpy2 as rpy
except:
    import rpy

from scipy import stats
import scipy
import pylab

__docformat__ = "restructuredtext en"

def list_log( x ):
    """
    Compute the log of each item of a list and change it to an array

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the log list from the input list
     
    :returntype: float list


    """

    l = list( scipy.log( scipy.array( x) ) )
    return l,


def StatSummary( x ):
    """
    Compute the statistical summary (min, max, median, mean, sd) 

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the vector of the statistical summary
    :returntype: float list

    :attention:  x cannot be empty
    """

    result = rpy.r.summary(x)
    minimum = result['Min.']
    maximum = result['Max.']
    median = result['Median']
    mean = result['Mean']
    sd = rpy.r.sd(x)

    data = {'minimum':minimum, 'maximum':maximum, 'median':median, 'mean':mean, 'standard deviation':sd}
    return data


def Corr( x , y ):#= []):
    """
    Compute the statistical correlation

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values 
     - `y`: an optionnal (non-empty) numeric vector of data values

    :Types:
     - `x`: float list
     - `y`: float list

    :returns: the vector of the correlation
    :returntype: float list

    :attention:  x cannot be empty, x and y must have the same size
    """

    res = rpy.r.cor(x,y)
        
    data = {'Cor': res, 'x':x, 'y':y}

    return data


def Mean( x ):
    """
    Compute the statistical mean

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the mean 
    :returntype: float

    :attention:  x cannot be empty
    """

    result = stats.stats.mean(x)

    return result


def Median( x ):
    """
    Compute the statistical median

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the median 
    :returntype: float

    :attention:  x cannot be empty
    """

    result = stats.stats.median(x)

    return result

def Mode( x ):
    """
    Compute the statistical mode

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the mode 
    :returntype: float list

    :attention:  x cannot be empty
    """

    res = stats.stats.mode(x)
    mode = list(res[0])
    count = list(res[1])

    data = {'modal value': mode, 'counts': count}
    return data

def Var( x ):
    """
    Compute the statistical variance

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the variance 
    :returntype: float

    :attention:  x cannot be empty
     """

    result = stats.stats.var(x)

    return result

def Std( x ):
    """
    Compute the statistical standard deviation

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the variance 
    :returntype: float

    :attention:  x cannot be empty
    """

    result = stats.stats.std(x)

    return result

def Freq(x):

    """
    Compute the frequencies

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the frequencies 
    :returntype: float list

    :attention:  x cannot be empty
     """

    count = rpy.r.table(x)
    co = list(count)

    freq = [float(co[0])/len(x)]
    for i in range(1,len(co)):
        freq.append(float(co[i])/len(x))
        
    
    x = rpy.r.sort(x)
    val = [x[0]]
    j = 0

    for i in range(1,len(x)):
        if x[i]!=val[j]:
            j = j+1
            val.append(x[i])

    
    data = {'values': val, 'counts': co, 'frequencies': freq}
    return data


def Density(x):
    """
    Compute the Kernel density estimation

    :Parameters:
     - `x`: a (non-empty) numeric vector of data values

    :Types:
     - `x`: float list

    :returns: the estimated density values 
    :returntype: float list

    :attention:  x cannot be empty
     """

    res = rpy.r.density(x)

    return res
