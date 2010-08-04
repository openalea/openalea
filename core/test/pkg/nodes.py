# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" Data Nodes for testing"""

__license__ = "Cecill-C"
__revision__ = " $Id: data.py 2445 2010-05-12 09:11:00Z pradal $ "

from os.path import join
from openalea.core import Node

class Float(Node):
    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))

    def __call__(self, inputs):
        res = float(inputs[0])
        self.set_caption('%.1f'%res)
        return (res, )

