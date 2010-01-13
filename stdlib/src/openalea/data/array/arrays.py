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

from array import array
from openalea.core import Node, ISequence, IEnumStr


class PyArray(Node):
    """
    Python array
    """
    typecodes = ['c', 'b', 'B', 'u', 'i', 'I', 'l', 'L', 'f', 'd']
    codename = ['character',
                'signed integer (1)', 
                'unsigned integer (1)',
                'unicode character (2)',
                'signed integer (2)', 
                'unsigned integer (2)',
                'signed integer (4)', 
                'unsigned integer (4)',
                'floating point (4)',
                'floating point (8)',
                ]

    def __init__(self):
        Node.__init__(self)

        self.typedict = dict(zip(self.codename, self.typecodes))
        self.add_input(name='typecode', interface=IEnumStr(self.codename), 
                       value='signed integer (4)')
        self.add_input(name='values', interface=ISequence)
        self.add_output(name='array', interface=ISequence)

    def __call__(self, inputs):
        """ inputs is the list of input values """
        typecode = inputs[0]
        values = inputs[1]

        code = self.typedict[typecode]

        return (array(code, values),)

