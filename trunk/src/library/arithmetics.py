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



from openalea.core.external import *


class Value(Node):
    """ Variable
    Input 0 : if connected, set the stored value
    Ouput 0 : transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "val", interface = IFloat, value = 0.) 
        self.add_output( name = "out", interface = IFloat) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( inputs[0], )
        

class Add(Node):
    """ Generic Addition
    Input 0 : First value to add
    Input 1 : Second value to add
    Output 0 : In0 + In1
    """

    def __init__(self):

        Node.__init__(self)

        # defines I/O
        self.add_input( name = "In 0", interface = None, value = 0.)
        self.add_input( name = "In 1", interface = None, value = 0.)
            
        self.add_output( name = "Out", interface = None) 


    def __call__(self, inputs):
        """ inputs is the list of input values """

        return ( sum(inputs),)
        

