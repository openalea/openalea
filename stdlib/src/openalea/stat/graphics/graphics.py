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
"""Plotting routines"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core import *
from openalea.plotools import plotable

import rpy
from scipy import stats
import scipy
import pylab

__docformat__ = "restructuredtext en"

def Plot(x,y, xlab, ylab, main):
    """
    Plot y according to x

    :Parameters:
     - `x` : the coordinates of points in the plot. 
     - `y`: the y coordinates of points in the plot
     - `xlab`: a title for the x axis
     - `ylab`: a title for the y axis
     - `main`: a title for the plot
     
    :Types:
     - `x` : float list
     - `y`: float list
     - `xlab`: string
     - `ylab`: string
     - `main`: string

    :returns: a plot
    :returntype: None

    :attention: x and y must have the same length
    """

    rpy.r.plot(x,y,xlab=xlab, ylab=ylab, main=main)
    
    return (x,)


def Hist(x, k, xlab, main, freq):
    """
    Histogram of x

    :Parameters:
     - `x` : data 
     - `k`: number of classes
     - `xlab`: a title for the x axis
     - `main`: a title for the plot
     - `freq`: counts or densities
     
    :Types:
     - `x` : float list
     - `k`: int
     - `xlab`: string
     - `main`: string
     - `freq`: boolean

    :returns: an histogram
    :returntype: float list

    :attention: k must be greater or equal than 0
    """

    if k != 0:
        step = (max(x)-min(x))/k
        rpy.r.hist(x,xlab=xlab, main=main, br=rpy.r.seq(min(x),max(x),step), freq=freq)
        
    else:
        rpy.r.hist(x,xlab=xlab, main=main, freq=freq)
            
        
    return (x,)


def PlotDens(x):
    """
    Add the kernel density estimation

    :Parameters:
     - `x` : the coordinates of points in the plot. 
     
    :Types:
     - `x` : float list

    :returns: a plot
    :returntype: None

    :attention: x and y must have the same length
    """

    rpy.r.lines(rpy.r.density(x),col=2)
    
    return (x,)

