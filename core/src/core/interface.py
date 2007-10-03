# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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

from metaclass import make_metaclass
from singleton import Singleton
from observer import AbstractListener
import types

# Dictionary to map Interface with corresponding python type

class TypeInterfaceMap(dict):

    """
    Singleton class to map Interface with standard python type
    InterfaceWidgetMap inherits from dict class
    """
    
    __metaclass__ = Singleton

    def __init__(self, *args):
        dict.__init__(self, *args)

    def declare_interface(self, type, interface):
        """
        Declare an interface and its optional widget
        @param interface : IInterface class object
        @param type : Python type
        """
        
        if(type and not self.has_key(type)):
            self[type] = interface


class IInterfaceMetaClass(type):
    """
    IInterface Metaclass
    Allow to register corresponding python type
    """

    all = [] # all interfaces
    
    def __init__(cls,name,bases,dic):
        super(IInterfaceMetaClass,cls).__init__(name,bases,dic)
        TypeInterfaceMap().declare_interface(cls.__pytype__, cls)
        IInterfaceMetaClass.all.append(cls)
        
    def __repr__(cls):
        return cls.__name__



################################################################################

# Defaults interfaces


class IInterface(object):
    """ Abstract base class for all interfaces """
    __metaclass__ = IInterfaceMetaClass
    __pytype__ = None

    @classmethod
    def default(cls):
        return None
   


class IStr(IInterface):
    """ String interface """
    
    __pytype__ = types.StringType

    @classmethod
    def default(cls):
        return str()
    


class IFileStr(IStr):
    """ File Path interface """

    def __init__(self, filter="All (*.*)", save=False):
        self.filter = filter
        self.save = save



class IDirStr(IStr):
    """ Directory Path interface """
    pass


class ITextStr(IStr):
    """ Long String interface """
    pass



class IFloat(IInterface):
    """ Float interface """

    __pytype__ = types.FloatType
    
    def __init__(self, min = -2.**24, max = 2.**24):

        self.min = min
        self.max = max

    @classmethod
    def default(cls):
        return 0.
    

    

class IInt(IInterface):
    """ Int interface """

    __pytype__ = types.IntType
    
    def __init__(self, min = -2**24, max = 2**24):

        self.min = min
        self.max = max


class IBool(IInterface):
    """ Bool interface """

    __pytype__ = types.BooleanType

    @classmethod
    def default(cls):
        return False


class IEnumStr(IStr):
    """ String enumeration """

    def __init__(self, enum = []):
        self.enum = enum


class IRGBColor(IInterface):
    """ RGB Color """
    pass


class IDateTime(IInterface):
    """ DateTime """
    pass


class ITuple3(IInterface):
    """ Tuple3 """

    @classmethod
    def default(cls):
        return (None,None,None)


class IFunction(IInterface):
    """ Function interface """
    __pytype__ = types.FunctionType



class ISequence(IInterface):
    """ Sequence interface (list, tuple, ...) """
    __pytype__ = types.ListType

    @classmethod
    def default(cls):
        return list()

    

class IDict(IInterface):
    """ Dictionary interface """
    __pytype__ = types.DictType

    @classmethod
    def default(cls):
        return dict()




# Dictionary to map Interface with corresponding widget


class InterfaceWidgetMap(dict):
    """
    Singleton class to map Interface with InterfaceWidget
    InterfaceWidgetMap inherits from dict class
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



# Base class for interface widget
class IWidgetMetaClass(type):
    """ InterfaceWidget Metaclass """
    
    def __init__(cls,name,bases,dic):
        super(IWidgetMetaClass,cls).__init__(name,bases,dic)
        if(cls.__interface__):
            InterfaceWidgetMap().declare_interface(cls.__interface__, cls)



class IInterfaceWidget(AbstractListener):
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

        #i = self.node.get_input_index(self.param_str)
        state = self.node.get_input_state(self.param_str)

        # By default, disable the entire widget
        try:
            notconnected = bool(state != "connected")
            if(self.node.internal_data.get('minimal', False)):
                self.setVisible(notconnected)
            else:
                self.setEnabled(notconnected)
        except:
            pass


    def notify(self, sender, event):
        """ Notification sent by node """
        pass



