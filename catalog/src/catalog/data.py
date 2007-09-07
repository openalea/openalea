# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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


from openalea.core.datapool import DataPool

class PoolReader(Node):
    """
In : Name (key)
Out : Object (value)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = self.pool.get(key)
        if key in self.pool:
            self.set_caption(str(key))
        return (obj, )


class PoolWriter(Node):
    """
In :  Name (String), Object (Any)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = inputs[1]
        self.set_caption(str(key)+' : '+str(obj))
        self.pool[key] = obj



def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None



