# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Standard python functions for functional programming. """

__license__ =  "Cecill-C"
__revision__ = " $Id: parallel.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from openalea.core import Node, ITextStr

from IPython.kernel import client

def pmap(func, seq):
    """ map(func, seq) """
    
    tc = client.TaskClient()
    if func and seq:
        return ( tc.map(func, seq), )
    else:
        return ( [], )


