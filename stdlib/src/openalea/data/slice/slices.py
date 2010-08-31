# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
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
__revision__ = " $Id: tuples.py 2751 2010-08-12 12:51:20Z moscardi $ "

from os.path import join
from openalea.core import *


class Slice(Node):
    """
    Python Slice
    """
    def __call__(self, inputs):
        return slice(inputs[0], inputs[1], inputs[2]), 

