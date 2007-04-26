# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Data Node
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *


class InputFile(Node):
    """
A file path
Out :  the file path string
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        return ( str(inputs[0]),  )



class Bool(Node):
    """
Boolean value
Out :  the value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(False))


    def __call__(self, inputs):
        """ inputs is the list of input values """
        res= bool(inputs[0])
        self.set_caption(str(res))
        return ( res,  )



class Int(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0))


    def __call__(self, inputs):
        v = int(inputs[0])
        self.set_caption(str(v))
        return ( v, )


class Float(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))
       

    def __call__(self, inputs):
        """ inputs is the list of input values """
        res = float(inputs[0])
        self.set_caption('%.1f'%res)
        return ( res, )


class String(Node):
    """
String Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """


    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( str(inputs[0]), )




class EnumTest(Node):
    """
String enumeration Test
    """

    def __call__(self, inputs):
        return ( inputs[0], )


class RGB(Node):
    """
RGB Color
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( inputs[0], )


class List(Node):
    """
Python List
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        import copy
        return (copy.copy(inputs[0]), )


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


class List9(Node):
    """
    Python list with 8 entries.
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "i0", interface = None)
        self.add_input( name = "i1", interface = None)
        self.add_input( name = "i2", interface = None)
        self.add_input( name = "i3", interface = None)
        self.add_input( name = "i4", interface = None)
        self.add_input( name = "i5", interface = None)
        self.add_input( name = "i6", interface = None)
        self.add_input( name = "i7", interface = None)
        self.add_input( name = "i8", interface = None)
        self.add_output( name = "list", interface = ISequence) 

    def __call__(self, inputs):
        """ inputs is the list of input values """
        l= filter(None,inputs)
        return ( l, )
