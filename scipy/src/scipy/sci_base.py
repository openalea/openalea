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
import scipy 


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
