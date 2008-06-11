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

import pylab

__docformat__ = "restructuredtext en"

def Load(path):
    """
    Read a .txt file 

    :Parameters:
     - `path`: path of the .txt file

    :Types:
     - `path`: string

    :returns: the file
    :returntype: array
    """

    f = pylab.load(path)

    return f


def ExtractLigne(data,l, val):
    """
    Extract the lth row with elements different to val

    :Parameters:
     - `data` : data 
     - `l`: row
     - `val`: comparison value

    :Types:
     - `data` : array
     - `l`: int
     - `val`: float

    :returns: the lth row of data
    :returntype: array

    :attention: l must be greater or equal than 0 
    """

    res = filter(lambda x: x!=val, data[l])

    return (res,)

def ExtractCol(data,c, val):
    """
    Extract the cth column with elements different to val

    :Parameters:
     - `data` : data 
     - `c`: column
     - `val`: comparison value

    :Types:
     - `data` : array
     - `c`: int
     - `val`: float

    :returns: the cth column of data
    :returntype: array

    :attention: c must be greater or equal than 0 
    """

    res = filter(lambda x: x!=val, data[:,c])

    return (res,)


