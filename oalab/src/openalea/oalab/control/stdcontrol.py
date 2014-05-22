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

