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


def list_log( valist ):
    """
    Compute the log of each item of a list and change it to an array

    :Parameters:
     - 'list': a (non-empty) numeric vector of data values

    :Types:
     - 'list': float list

    :Returns the log list from the input list 
    :Returntype: float list

    """

    l = list( scipy.log( scipy.array( valist ) ) )
    return l,


def Load(path):
    """
    Read a .txt file 

    :Parameters:
     - 'path': path of the .txt file

     :Types:
     - 'x': string

     :Returns the file
     :Returntype: array
     """

    f = pylab.load(path)

    return f


def ExtractLigne(data,l, val):
    """
    Extract the lth row with elements different to val

    :Parameters:
     - 'data' : data 
     - 'l': row
     - 'val': comparison value

     :Types:
     - 'data' : array
     - 'l': int
     - 'val': float

     :Returns the lth row of data
     :Returntype: array

     :attention: l must be greater or equal than 0 
     """

    res = filter(lambda x: x!=val, data[l])

    return (res,)

def ExtractCol(data,c, val):
    """
    Extract the cth column with elements different to val

    :Parameters:
     - 'data' : data 
     - 'c': column
     - 'val': comparison value

     :Types:
     - 'data' : array
     - 'c': int
     - 'val': float

     :Returns the cth column of data
     :Returntype: array

     :attention: c must be greater or equal than 0 
     """

    res = filter(lambda x: x!=val, data[:,c])

    return (res,)


def Plot(x,y, xlab, ylab, main):
    """
    Plot y according to x

    :Parameters:
     - 'x' : the coordinates of points in the plot. 
     - 'y': the y coordinates of points in the plot
     - 'xlab': a title for the x axis
     - 'ylab': a title for the y axis
     - 'main': a title for the plot
     
     :Types:
     - 'x' : float list
     - 'y': float list
     - 'xlab': string
     - 'ylab': string
     - 'main': string

     :Returns a plot
     :Returntype: None

     :attention: x and y must have the same length
     """

    rpy.r.plot(x,y,xlab=xlab, ylab=ylab, main=main)
    
    return None


def Hist(x, k, xlab, main, freq):
    """
    Histogram of x

    :Parameters:
     - 'x' : data 
     - 'k': number of classes
     - 'xlab': a title for the x axis
     - 'main': a title for the plot
     - 'freq': counts or densities
     
     :Types:
     - 'x' : float list
     - 'k': int
     - 'xlab': string
     - 'main': string
     - 'freq': boolean

     :Returns an histogram
     :Returntype: float list

     :attention: k must be greater or equal than 0
     """

    if k != 0:
        step = (max(x)-min(x))/k
        rpy.r.hist(x,xlab=xlab, main=main, br=rpy.r.seq(min(x),max(x),step), freq=freq)
        
    else:
        rpy.r.hist(x,xlab=xlab, main=main, freq=freq)
            
        
    return None


def StatSummary( x ):
    """
    Compute the statistical summary (min, max, median, mean, sd) 

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the vector of the statistical summary
     :Returntype: float list

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
     - 'x': a (non-empty) numeric vector of data values 
     - 'y': an optionnal (non-empty) numeric vector of data values

     :Types:
     - 'x': float list
     - 'y': float list

     :Returns the vector of the correlation
     :Returntype: float list

     :attention:  x cannot be empty, x and y must have the same size
     """

    res = rpy.r.cor(x,y)
        
    data = {'Cor': res, 'x':x, 'y':y}

    return data


def Mean( x ):
    """
    Compute the statistical mean

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the mean 
     :Returntype: float

     :attention:  x cannot be empty
     """

    result = stats.stats.mean(x)

    return result


def Median( x ):
    """
    Compute the statistical median

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the median 
     :Returntype: float

     :attention:  x cannot be empty
     """

    result = stats.stats.median(x)

    return result

def Mode( x ):
    """
    Compute the statistical mode

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the mode 
     :Returntype: float list

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
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the variance 
     :Returntype: float

     :attention:  x cannot be empty
     """

    result = stats.stats.var(x)

    return result

def Std( x ):
    """
    Compute the statistical standard deviation

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the variance 
     :Returntype: float

     :attention:  x cannot be empty
     """

    result = stats.stats.std(x)

    return result

def Freq(x):

    """
    Compute the frequencies

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the frequencies 
     :Returntype: float list

     :attention:  x cannot be empty
     """

    count = rpy.r.table(x)
    co = list(count)

    freq = [float(co[0])/len(x)]
    for i in range(1,len(co)-1):
        freq.append(float(co[i])/len(x))
        
    
    x = rpy.r.sort(x)
    val = [x[0]]
    j = 0

    for i in range(1,len(x)-1):
        if x[i]!=val[j]:
            j = j+1
            val.append(x[i])

    
    data = {'values': val, 'counts': co, 'frequencies': freq}
    return data
