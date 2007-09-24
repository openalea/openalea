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
Standard python functions for functional programming.
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



#//////////////////////////////////////////////////////////////////////////////

def pymap(func, seq):
    """ map(func, seq) """

    if func and seq:
        return ( map(func,seq), )
    else:
        return ( [], )


def pyfilter(func, seq):
    """ filter(func, seq) """

    if func and seq:
        return ( filter(func,seq), )
    else:
        return ( [], )


def pyreduce(func, seq):
    """ filter(func, seq) """

    if func and seq:
        return ( reduce(func,seq), )
    else:
        return ( [], )



from openalea.core import *
from operator import *

class Linear(Node):
    """
Ax + B model 
Input 0 : A, B values
Ouput 0 : Ax + B
Parameters :
  A : linear coefficient
  B : intercept
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "A", interface = IFloat, value = 1.)
        self.add_input( name = "B", interface = IFloat, value = 0.)
            
        self.add_output( name = "f", interface = IFunction) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """

        # We prefer here to get the value by key
        a = self.get_input("A")
        b = self.get_input("B")

        f = lambda x: a*x + b

        return ( f,  )




class Generator( Node ):
    """h(x) = f(x) op g(x)

Create a function generator.
Input:
  f: function
  op: operator (==, +, -, <, <=, >, >=, and, or,... )
  f: function
Output:
  h: function
    """
    op_name= ["<","<=","==","!=",">=",">","+","-","*","/","is","is not","and",
              "or","%","**"]
    op_val=  [lt , le , eq , ne , ge , gt,add,sub,mul,div, is_, is_not , and_,
              or_ ,mod, pow]

    op_dict= dict(zip(op_name,op_val))
    
    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "f", interface = IFunction ) 
        self.add_input( name = "op", interface = IEnumStr(self.op_name),value= "==" ) 
        self.add_input( name = "g", interface = IFunction ) 
        self.add_output( name = "h", interface = IFunction ) 


    def __call__(self, inputs):

        f= self.get_input("f")
        op_key= self.get_input("op")
        g= self.get_input("g")

        op= self.op_dict[op_key]
        self.set_caption(op_key)
        
        binop= None
        
        if (f is None) and (g is None):
            return (binop,)
        
        if callable(f) and callable(g):
            binop= lambda x: op(f(x),g(x))
        elif callable(f): 
            binop= lambda x: op(f(x),g)
        elif callable(g): 
            binop= lambda x: op(f,g(x))
        else:
            binop= lambda x: op(f,g)

        return (binop,)

