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


def pyrange(start=0, stop=0, step=1):
    """ range(start, stop, step) """

    return (range(start, stop, step),)

class List(Node):
    """Python List"""

    def __call__(self, inputs):
        """ inputs is the list of input value
        :param inputs: The stored value
        """
        import copy
        try:
            iter(inputs[0])
            return (copy.copy(inputs[0]), )
        except:
            return ([copy.copy(inputs[0])], )


def pymap(func, seq):
    """ map(func, seq) """

    if func is not None and seq is not None and len(seq):
        return ( map(func, seq), )
    else:
        return ( [], )
