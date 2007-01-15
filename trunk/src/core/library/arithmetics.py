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
Arithmetic nodes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



from core.core import Node


class Value(Node):
    """ Variable
    Input 0 : if connected, set the stored value
    Ouput 0 : transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.inputs  = [None]
        self.outputs  = [0.]

        self['val'] = 0.


    def __call__(self, inputs=()):
        """ inputs is the list of input values """
        
        i0=inputs[0]
        
        if(i0 != None) :
            self['val'] = i0

        return ( self['val'],  )
        

class Add(Node):
    """ Generic Addition
    Input 0 : First value to add
    Input 1 : Second value to add
    Output 0 : In0 + In1
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.inputs = [0., 0.]
        self.outputs = [0.]


    def __call__(self, inputs=() ):
        """ inputs is the list of input values """

        try:
            return ( sum(inputs), )
        except:
            return (0.,)


class Mult(Node):
    """ Generic Multiplication
    Input 0 : First value 
    Input 1 : Second value
    Output 0 : In0 * In1
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.inputs = [0., 0.]
        self.outputs = [0.]


    def __call__(self, inputs=() ):
        """ inputs is the list of input values """

        try:
            return ( inputs[0] * inputs[1], )
        except:
            return (0.,)


class Sub(Node):
    """ Generic Addition
    Input 0 : First value 
    Input 1 : Second value 
    Output 0 : In0 - In1
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.inputs = [0., 0.]
        self.outputs = [0.]


    def __call__(self, inputs=() ):
        """ inputs is the list of input values """

        try:
            return ( inputs[0] - inputs[1], )
        except:
            return (0.,)


class Div(Node):
    """ Generic Division
    Input 0 : First value 
    Input 1 : Second value
    Output 0 : In0 / In1
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.inputs = [0., 0.]
        self.outputs = [0.]


    def __call__(self, inputs=() ):
        """ inputs is the list of input values """

        try:
            return ( inputs[0] / inputs[1], )
        except:
            return (0.,)
