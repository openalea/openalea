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


class InputFile(Node):
    """
A file path
Out :  the file path string
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "Filename", interface = IFileStr, value = "")
        self.add_output( name = "Filename", interface = IFileStr)
            
        

    def __call__(self, inputs):
        """ inputs is the list of input values """

        return ( str(inputs[0]),  )


class Bool(Node):
    """
Boolean value
Out :  the value
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "Bool", interface = IBool, value = False)
        self.add_output( name = "Bool", interface = IBool)
            
        

    def __call__(self, inputs):
        """ inputs is the list of input values """

        return ( bool(inputs[0]),  )


class Int(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "val", interface = IInt, value = 0) 
        self.add_output( name = "out", interface = IInt) 

    def __call__(self, inputs):
        
        return ( int(inputs[0]), )


class Float(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "val", interface = IFloat, value = 0.) 
        self.add_output( name = "out", interface = IFloat) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( float(inputs[0]), )


class String(Node):
    """
String Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "str", interface = IStr, value = "") 
        self.add_output( name = "str", interface = IStr) 
        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( str(inputs[0]), )


class EnumTest(Node):
    """
String enumeration Test
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "val", interface = IEnumStr(["enum1", "enum2", "enum3"]), value = "enum1") 
        self.add_output( name = "out", interface = IStr) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( inputs[0], )


class RGB(Node):
    """
RGB Color
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "rgb", interface = IRGBColor, value = (0,0,0)) 
        self.add_output( name = "rgb", interface = IStr) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( inputs[0], )

#//////////////////////////////////////////////////////////////////////////////

class Map( Node ):
    """Map(function, sequence) -> list

Apply a function on a sequence.
Input:
  function
  sequence (iterable)
Output:
  sequence
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "f", interface = IFunction ) 
        self.add_input( name = "seq", interface = ISequence ) 
        self.add_output( name = "list", interface = ISequence ) 


    def __call__(self, inputs):
        f= self.get_input_by_key("f")
        seq= self.get_input_by_key("seq")
        if f and seq:
            return ( map(f,seq), )
        else:
            return ( [], )

#//////////////////////////////////////////////////////////////////////////////

class Filter( Node ):
    """Filter(function, sequence) -> list

Apply a function on a sequence.
Input:
  function
  sequence (iterable)
Output:
  sequence
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "f", interface = IFunction ) 
        self.add_input( name = "seq", interface = ISequence ) 
        self.add_output( name = "list", interface = ISequence ) 


    def __call__(self, inputs):
        f= self.get_input_by_key("f")
        seq= self.get_input_by_key("seq")

        if f and seq:
            return ( filter(f,seq), )
        else:
            return ( [], )

#//////////////////////////////////////////////////////////////////////////////

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

        f= self.get_input_by_key("f")
        op_key= self.get_input_by_key("op")
        g= self.get_input_by_key("g")

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

class Len( Node ):
    __doc__= len.__doc__

    def __init__(self):

        Node.__init__(self)

        self.add_input ( name = "object", interface = None, value= [] ) 
        self.add_output( name = "n", interface = None ) 

    def __call__(self, inputs):
        obj= self.get_input_by_key("object")

        f= None
        if callable(obj):
            f= lambda x: len(obj(x))
        else:
            f= len(obj)
        return ( f, )
