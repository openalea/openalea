# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" Data Nodes """
__license__= "Cecill-C"
__revision__=" $Id: $ "

from os.path import join
from openalea.core import *

class List(Node):
    """
Python List
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        import copy
        try:
            iter( inputs[0] )
            return (copy.copy(inputs[0]), )
        except:
            return ([copy.copy(inputs[0])], )
            


def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None



