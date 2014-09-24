# -*- python -*-
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
__revision__ = "$Id: $"

import abc

class ControlABC:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        A control is an object with a name and a value.
        """
        self.name = "default"
        self.interface = None
        self.default()

    @abc.abstractmethod
    def default(self):
        """
        Reinitialize control to default value
        """
        self._value = 0

    def rename(self, name):
        self.name = name

    @abc.abstractmethod
    def edit(self, synchro):
        """
        Returns a widget able to edit data.
        """
        pass

    @abc.abstractmethod
    def view(self):
        """
        Returns a widget able to display data
        """

    @abc.abstractmethod
    def thumbnail(self):
        """
        Returns a preview
        """

    @abc.abstractmethod
    def value(self):
        """
        Returns current value.
        """

    @abc.abstractmethod
    def set_value(self, value):
        """
        Set input "data".
        If this method is called, data is used as initial value or replaces current value.
        Data passed as parameter is NEVER MODIFIED.

        For example, for a text editor, you can pass a sample text.
        This sample is a
          - starting point for editing
          - differs from control "default" (allow to custom controls)
          - can be view thanks to control
        """


from openalea.vpltk.qt import QtGui

class ObserverPanel(QtGui.QWidget):
    """
    Widget to display observers
    """
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        'connected to current_project.observer'
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def rename(self):
        pass

    def diplay_thumbnails(self):
        """
        Display thumbnails of all control.
        - List control
        - Call control.thumbnail() on each one
        """
        pass
