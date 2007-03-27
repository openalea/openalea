# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
This module defines Interface classes (I/O types)
"""

__license__= "Cecill-C"
__revision__=" $Id$ "
    

class IInterface(object):
    """ Abstract base class for all interfaces """
    pass

class IFileStr(IInterface):
    """ File Path interface """
    pass


class IStr(IInterface):
    """ String interface """
    pass


class IFloat(IInterface):
    """ Float interface """
    
    def __init__(self, min = -2.**24, max = 2.**24):

        self.min = min
        self.max = max
    

class IInt(IInterface):
    """ Int interface """
    
    def __init__(self, min = -2**24, max = 2**24):

        self.min = min
        self.max = max


class IBool(IInterface):
    """ Bool interface """
    pass


class IEnumStr(IInterface):
    """ String enumeration """

    def __init__(self, enum = []):
        self.enum = enum


class IRGBColor(IInterface):
    """ RGB Color """
    pass

class ITuple3(IInterface):
    """ Tuple3 """
    def __init__(self):
        pass

class IFunction(IInterface):
    """ Function interface """
    pass

class ISequence(IInterface):
    """ Sequence interface (list, tuple, ...) """
    pass

class IDict(IInterface):
    """ Dictionary interface """
    pass



# Dictionary to map Interface with corresponding widget

from openalea.core.singleton import Singleton

class InterfaceMapper(dict):
    """
    Singleton class to map Interface with InterfaceWidget
    InterfaceMapper inherits from dict class
    """
    
    __metaclass__ = Singleton

    def __init__(self, *args):
        dict.__init__(self, *args)

    def declare_interface(self, interface, widget=None):
        """
        Declare an interface and its optional widget
        @param interface : IInterface class object
        @param widget : IInterfaceWidget class object
        """

        self[interface] = widget



class IWidgetMetaClass(type):
    """ InterfaceWidget Metaclass """
    
    def __init__(cls,name,bases,dic):
        super(IWidgetMetaClass,cls).__init__(name,bases,dic)
        if(cls.__interface__):
            InterfaceMapper().declare_interface(cls.__interface__, cls)



class IInterfaceWidget(object):
    """ Base class for widget associated to an interface """

    __metaclass__ = IWidgetMetaClass
    __interface__ = None


    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
  
        self.node = node
        self.param_str = parameter_str


    def update_state(self):
        """ Enable or disable widget depending of connection status """

        i = self.node.get_input_index(self.param_str)
        state = self.node.get_input_state(i)

        # By default, disable the entire widget
        try:
            if(state == "connected"):
                self.setEnabled(False)
            else:
                self.setEnabled(True)
        except:
            pass



################################################################################

# Functions from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/204197
# They resolv metaclass conflicts
# Title: SOLVING THE METACLASS CONFLICT
# Submitter: Michele Simionato (other recipes)
# Last Updated: 2005/04/11
# Version no: 1.4
# Category: OOP

################################################################################

# The simplest case where a metatype conflict happens is the following.
# Consider a class ``A`` with metaclass ``M_A`` and a class ``B`` with
# an independent metaclass ``M_B``; suppose we derive ``C`` from ``A``
# and ``B``. The question is: what is the metaclass of ``C`` ?
# Is it ``M_A`` or ``M_B`` ?


# The correct answer (see the book "Putting metaclasses to work" for a
# thoughtful discussion) is ``M_C``, where ``M_C`` is a metaclass that inherits
# from ``M_A`` and ``M_B``, as in the following graph, where instantiation
# is denoted by colon lines:


#              M_A     M_B
#               : \   / :
#               :  \ /  :
#               A  M_C  B
#                \  :  /
#                 \ : /
#                   C


# However, Python is not that magic, and it does not automatically create
# ``M_C``. Instead, it raises a ``TypeError``, warning the programmer of
# the possible confusion. The metatype conflict can be avoided
# by assegning the correct metaclass to ``C`` by hand:

# >>> class M_AM_B(M_A,M_B): pass
# ...
# >>> class C(A,B):
# ... __metaclass__=M_AM_B
# >>> C,type(C)
# (<class 'C'>, <class 'M_AM_B'>)

# In general, a class ``A(B, C, D , ...)`` can be generated without conflicts
# only if ``type(A)`` is a subclass of each of ``type(B), type(C), ...``

# It is possible to automatically avoid conflicts, by defining a smart
# class factory that generates the correct metaclass by looking at the
# metaclasses of the base classes. This is done via the ``classmaker``
# class factory, wich internally invokes the ``get_noconflict_metaclass``
# function.

# >>> from noconflict import classmaker
# >>> class C(A,B):
# ... __metaclass__=classmaker()
# >>> C
# <class 'C'>
# >>> type(C) # automatically generated metaclass
# <class 'noconflict._M_AM_B'>

# In order to avoid to generate twice the same metaclass, they
# are stored in a dictionary. In particular, when ``_generatemetaclass``
# is invoked with the same arguments it returns the same metaclass.

import inspect, types

 ############## preliminary: two utility functions #####################

def skip_redundant(iterable, skipset=None):
    "Redundant items are repeated items or items in the original skipset."
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item

            
def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))


# Store already generated class here
memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)
     
    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
        return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:         # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1: # another trivial case
        meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases: 
        raise TypeError("Incompatible root metatypes", needed_metas)
    else: # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = make_metaclass()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta


# Main factory Function

def make_metaclass(left_metas=(), right_metas=()):
    """ Generate a metaclass for multi-inherited class """
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class
