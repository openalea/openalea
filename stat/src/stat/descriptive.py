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
import scipy
import pylab


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

