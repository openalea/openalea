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
Standard python functions for functional programming.
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "


from openalea.core import *
from operator import *

#//////////////////////////////////////////////////////////////////////////////

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


class IfElse(Node):
    """
    Conditional expression
    In[0] : Boolean value
    In[1] : Value 1
    In[2] : Value 2

    Out[0]: If In[0] is True return Value 1 else Value 2
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "Cond", interface = IBool, value = True)
        self.add_input( name = "Expr1", interface = None, value = None)
        self.add_input( name = "Expr2", interface = None, value = None)
            
        self.add_output( name = "Result", interface = None) 
        

    def __call__(self, inputs):

        c = self.get_input("Cond")

        if (bool(c)):
            return (self.get_input("Expr1"),)
        else:
            return (self.get_input("Expr2"),)


class Equal(Node):
    """
    Equality test
    Out[0] = In[0] == In[1]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = None, value = None)
        self.add_input( name = "V2", interface = None, value = None)
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        v2 = self.get_input("V2")
        
        return (v1 == v2,)

        
class Greater(Node):
    """
    Binary test
    Out[0] = In[0] > In[1]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = None, value = None)
        self.add_input( name = "V2", interface = None, value = None)
            
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        v2 = self.get_input("V2")
        
        return (v1 > v2,)
    

class GreaterOrEqual(Node):
    """
    Binary test
    Out[0] = In[0] >= In[1]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = None, value = None)
        self.add_input( name = "V2", interface = None, value = None)
            
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        v2 = self.get_input("V2")
        
        return (v1 >= v2,)


class And(Node):
    """
    Binary test
    Out[0] = In[0] and In[1]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = IBool, value = True)
        self.add_input( name = "V2", interface = IBool, value = True)
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        v2 = self.get_input("V2")
        return (v1 and v2,)


class Or(Node):
    """
    Binary test
    Out[0] = In[0] or In[1]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = IBool, value = True)
        self.add_input( name = "V2", interface = IBool, value = True)
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        v2 = self.get_input("V2")
        return (v1 or v2,)


class Not(Node):
    """
    Binary test
    Out[0] = not In[0]
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "V1", interface = IBool, value = True)
        self.add_output( name = "Result", interface = IBool) 
        

    def __call__(self, inputs):

        v1 = self.get_input("V1")
        return (not v1, )



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
        
        binop= None
        
        if not (f and g):
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

