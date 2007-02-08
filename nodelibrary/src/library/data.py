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
__revision__=" $Id: simple_models.py 331 2007-02-02 15:50:47Z dufourko $ "


from openalea.core import *


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

        v = int(inputs[0])
        self.set_caption(str(v))
        return ( v, )


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


class List(Node):
    """
    Python List
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "list", interface = ISequence, value = []) 
        self.add_output( name = "list", interface = ISequence) 

   
    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( inputs[0], )


class Dict(Node):
    """
    Python Dictionary
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "dict", interface = IDict, value = {}) 
        self.add_output( name = "dict", interface = IDict) 
        

    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( inputs[0], )


class Tuple2(Node):
    """
    Python 2 Uple generator
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "in0", interface = None, value = None)
        self.add_input( name = "in1", interface = None, value = None) 
        self.add_output( name = "tuple", interface = ISequence) 


    def __call__(self, inputs):
        """ inputs is the list of input values """
        
        return ( (inputs[0], inputs[1]), )
