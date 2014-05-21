# -*- python -*-
#
#       Control classes for standard python types
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""
Control classes for standard python types
"""
__revision__ = "$Id: $"


from openalea.vpltk.qt import QtGui

class Control(object):
    """ Base Class for control """

    def __init__(self, name=None, value=None):
        super(Control, self).__init__()
        self.default()
        if name:
            self.name = name
        if value:
            self.value = value

    def save(self):
        """

        """
        return repr(self.value)

    def default(self):
        """
        Fill fields 'name' and ''value' with default values
        """
        raise NotImplementedError

    def edit(self):
        """
        Return a widget to edit object
        """
        raise NotImplementedError

    def thumbnail(self):
        """
        Return a widget to visualize object
        """
        raise NotImplementedError

class IntControl(Control):
    def __init__(self, name=None, value=None):
        super(IntControl, self).__init__(name, value)

    @classmethod
    def default(self):
        """
        Create a default control
        """
        self.name = "int"
        self.value = int()

    def edit(self):
        """
        Return a widget to edit object
        """
        pass

    def thumbnail(self):
        """
        Return a widget to visualize object
        """
        pass


class BoolControl(Control):
    def __init__(self, name=None, value=None):
        super(BoolControl, self).__init__(name, value)

    @classmethod
    def default(self):
        """
        Create a default control
        """
        self.name = "bool"
        self.value = bool()

    def edit(self):
        """
        Return a widget to edit object
        """
        pass

    def thumbnail(self):
        """
        Return a widget to visualize object
        """
        self.widg = QtGui.QLabel()
        self.widg.setText(self.value)
        return self.widg


class FloatControl(Control):
    def __init__(self, name=None, value=None):
        super(FloatControl, self).__init__(name, value)

    @classmethod
    def default(self):
        """
        Create a default control
        """
        self.name = "float"
        self.value = float()

    def edit(self):
        """
        Return a widget to edit object
        """
        pass

    def thumbnail(self):
        """
        Return a widget to visualize object
        """
        pass


import copy
from openalea.oalab.control.control import Control as Control2

class ColorListControl(Control2):
    """

    IIntControl is a Control with this specific method:
        - set_range(range), with range a couple of int.
    """
    interface = 'IColorList'

    def default(self):
        """
        Reinitialize control to default value
        """
        from openalea.plantgl.all import Material, Color3
        self._value = [
            Material("Color_0"),
            Material("Color_0", Color3(65, 45, 15)), # Brown
            Material("Color_2", Color3(30, 60, 10)), # Green
            Material("Color_3", Color3(60, 0, 0)), # Red
            Material("Color_4", Color3(60, 60, 15)), # Yellow
            Material("Color_5", Color3(0, 0, 60)), # Blue
            Material("Color_6", Color3(60, 0, 60)), # Purple
            ]

    def set_value(self, value):
        self._user_value = value
        self._value = [material for material in value]
        self.notify_change()

class IIntControl(Control2):
    """

    IIntControl is a Control with this specific method:
        - set_range(range), with range a couple of int.
    """
    interface = 'IInt'

    def default(self):
        """
        Reinitialize control to default value
        """
        self._value = int()
        self._range = (0, 100)

    def set_value(self, value):
        self._user_value = value
        self._value = copy.deepcopy(value)
        self.notify_change()

    # Methods specific to IInt
    ##########################
    def set_range(self, range):
        self._range = range

    def range(self):
        return self._range

