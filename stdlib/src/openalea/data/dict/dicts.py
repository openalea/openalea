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
""" Data Nodes """

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import Node


class Dict(Node):
    """
    Python Dictionary
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        import copy
        return (copy.copy(inputs[0]), )


class Pair(Node):
    """
    Python 2-uple generator
    """

    def __call__(self, inputs):
        return ( (inputs[0], inputs[1]), )


class Tuple3(Node):
    """
    Python 2-uple generator
    """

    def __call__(self, inputs):
        return ( (inputs[0], inputs[1], inputs[2]), )


def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None



