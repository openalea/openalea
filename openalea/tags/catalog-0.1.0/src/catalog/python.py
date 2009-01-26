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



class SetItem(Node):
    """
    Python __setitem__
    Input 0 : Python Object
    Input 1 : Index/Key
    Input2 : Value
    Output 0 : Modified Python Object
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = None)
        self.add_input( name = "key", interface = None, value = None)
        self.add_input( name = "value", interface = None, value = None) 
        self.add_output( name = "obj", interface = None) 
                

    def __call__(self, inputs):

        obj = inputs[0]
        p1 = inputs[1]
        p2 = inputs[2]
        ret = obj.__setitem__(p1,p2)
        return (obj , )


class GetItem(Node):
    """
    Python __getitem__
    Input 0 : Python Object
    Input 1 : Index/Key
    Output 0: Result of the getitem call
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = None)
        self.add_input( name = "key", interface = None, value = None)
        self.add_output( name = "result", interface = None) 

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        p1 = inputs[1]
        ret = obj.__getitem__(p1)
        return (ret, )


class DelItem(Node):
    """
    Python __delitem__
    Input 0 : Python Object
    Input 1 : Index/Key
    Output 0: Modified Python Object
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = None)
        self.add_input( name = "key", interface = None, value = None)
        self.add_output( name = "obj", interface = None) 

    def __call__(self, inputs):

        obj = inputs[0]
        p1 = inputs[1]
        ret = obj.__delitem__(p1)
        return (obj, )


class Keys(Node):
    """
    Python keys() function
    Input 0 : Dictionary
    Output 0: Key list
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = IDict, value = {})
        self.add_output( name = "list", interface = None) 

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        ret = obj.keys()
        return (ret, )


class Values(Node):
    """
    Python values() function
    Input 0 : Dictionary
    Output 0: List of values
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = IDict, value = {})
        self.add_output( name = "list", interface = None) 


    def __call__(self, inputs):

        obj = inputs[0]
        ret = obj.values()
        return (ret, )


class Items(Node):
    """
    Python items() function
    Input 0 : Dictionary
    Output 0: List of items tuple
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = {})
        self.add_output( name = "list", interface = None) 

    def __call__(self, inputs):

        obj = inputs[0]
        ret = obj.items()
        return (ret, )


class Append(Node):
    """
    Python list append(...) function
    Input 0 : List
    Input 1 : Value to append
    Output 0 : Modified list
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = ISequence, value = [])
        self.add_input( name = "append", interface = None, value = None)
        self.add_output( name = "list", interface = None) 

    def __call__(self, inputs):

        obj = inputs[0]
        p1 = inputs[1]
        obj.append(p1)
        return (obj, )


class SortList(Node):
    """
    Sort a list
    Input 0 : List
    Output 0 : Sorted list
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = ISequence, value = [])
        self.add_output( name = "list", interface = None) 

    def __call__(self, inputs):

        obj = inputs[0]
        obj.sort()
        return (obj, )


class ReverseList(Node):
    """
    Reverse a List
    Input 0 : List
    Output 0 : Reversed list
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = ISequence, value = [])
        self.add_output( name = "list", interface = None) 

    def __call__(self, inputs):

        obj = inputs[0]
        obj.reverse()
        return (obj, )



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
        self.add_input( name = "seq", interface = ISequence, value = [] ) 
        self.add_output( name = "list", interface = ISequence ) 


    def __call__(self, inputs):
        f= self.get_input_by_key("f")
        seq= self.get_input_by_key("seq")
        if f and seq:
            return ( map(f,seq), )
        else:
            return ( [], )


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
        self.add_input( name = "seq", interface = ISequence, value = [] ) 
        self.add_output( name = "list", interface = ISequence ) 


    def __call__(self, inputs):
        f= self.get_input_by_key("f")
        seq= self.get_input_by_key("seq")

        if f and seq:
            return ( filter(f,seq), )
        else:
            return ( [], )


class Reduce( Node ):
    __doc__ = reduce.__doc__

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "f", interface = IFunction ) 
        self.add_input( name = "seq", interface = ISequence, value = [] ) 
        self.add_output( name = "value", interface = None ) 


    def __call__(self, inputs):
        f= self.get_input_by_key("f")
        seq= self.get_input_by_key("seq")

        if f and seq:
            return ( reduce(f,seq), )
        else:
            return ( None, )


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




