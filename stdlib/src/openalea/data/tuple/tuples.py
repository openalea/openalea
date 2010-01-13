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
__revision__ = " $Id: tuples.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from os.path import join
from openalea.core import *


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

