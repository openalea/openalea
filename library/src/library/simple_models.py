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
Models nodes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
from operator import *

class LinearModel(Node):
    """
Ax + B model 
Input 0 : x value
Ouput 0 : Ax + B
Parameters :
  A : linear coefficient
  B : intercept
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "X", interface = IFloat, value = 0.)
        self.add_input( name = "A", interface = IFloat, value = 0.)
        self.add_input( name = "B", interface = IFloat, value = 0.)
            
        self.add_output( name = "Y", interface = None) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """

        # We prefer here to get the value by key
        x = self.get_input_by_key("X")
        a = self.get_input_by_key("A")
        b = self.get_input_by_key("B")

        y = a*x + b

        return ( y,  )

#//////////////////////////////////////////////////////////////////////////////

class Range( Node ):
    """range(start= 0, stop, step= 1) -> list of integers

Return an arithmetic sequence of integers
Input:
  start: int
  stop: int
  step: int
Output:
  list of integers
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "start", interface = IInt, value= 0 ) 
        self.add_input( name = "stop", interface = IInt, value= 1 ) 
        self.add_input( name = "step", interface = IInt, value= 1 ) 
        self.add_output( name = "list", interface = ISequence ) 


    def __call__(self, inputs):
        return ( range(*inputs), )

#//////////////////////////////////////////////////////////////////////////////

