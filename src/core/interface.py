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
    __metaclass__ = Singleton

    def __init__(self, *args):
        dict.__init__(self, *args)

    def declare_interface(self, interface, widget=None):
        """
        Declare an interface and its optional widget
        @param interface : IInterface class object
        @param widget : IInterfaceWidget class object
        """

        self[inteface] = widget




class IInterfaceWidget(object):
    """ Base class for widget associated to an interface """

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
