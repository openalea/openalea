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
Python Nodes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


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


def setitem(obj, key, value):
    """ call __setitem__ on obj """
    ret = obj.__setitem__(key, value)
    return obj


def getitem(obj, key):
    """ call __getitem__ on obj"""

    ret = obj.__getitem__(key)
    return (ret,)


def delitem(obj, key):
    """ call __delitem__ on obj"""
    
    ret = obj.__delitem__(key)
    return (obj,)


def keys(obj):
    """ call keys() on obj """

    ret = obj.keys()
    return (ret,)


def values(obj):
    """ call values() on obj """

    ret = obj.values()
    return (ret,)


def items(obj):
    """ call items() on obj """

    ret = obj.items()
    return (ret,)


def append(obj=[], val=None):
    """ call append(val) on obj """
    ret = list(obj)
    ret.append(val)
    return (ret,)


def pyrange(start=0, stop=0, step=1):
    """ range(start, stop, step) """

    return (range(start, stop, step),)



def pylen(obj):
    """ len(obj) """

    f= None
    if callable(obj):
        f= lambda x: len(obj(x))
    else:
        f= len(obj)
    return ( f, )


