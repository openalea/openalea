# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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
===========================
Control plugin documentation
===========================
"""

from openalea.core.interface import IInterface


class ControlWidgetPlugin():
    controls = []
    name = 'ControlWidget'
    icon_path = None

    edit_shape = [] # ['large', 'line', 'small']
    view_shape = [] # ['large', 'line', 'small']
    create_shape = [] # ['large', 'line', 'small']
    paint = False

    @classmethod
    def load(cls):
        raise NotImplementedError




class IControlWidget(IInterface):
    """
    """

    def reset(self, value=None, *kargs):
        """
        Reset widget to default values.
        """

    def set(self, control):
        """
        Use control to preset widget.
        Starts to listen to control events and read control's values
        """

    def apply(self, control):
        """
        Update control with widget values.
        """

    def read(self, control):
        """
        Update widget with control values
        """

    def notify(self, sender, event):
        """
        Method called when Observed control changes.
        Generally, when control send an event "ValueChanged", we want to
        refresh widget with new value.
        """

class IWidgetSelector(IInterface):
    def __init__(self):
        """

        shape: None, line, icon
        """

    @classmethod
    def edit(self, control, shape=None):
        """
        Returns an instance of IControlWidget that modifies control in place.
        Control can be updated continuously or on explicit user action
        (click on apply button for instance)
        """

    @classmethod
    def view(self, control, shape=None):
        """
        Returns an instance of IControlWidget that view control.
        This function never modify control.
        If you finally want to modify it, you can call "apply" explicitly.
        """

    @classmethod
    def create(self, shape=None):
        """
        Returns an instance of IControlWidget that can generate controls.
        """

    @classmethod
    def snapshot(self, control, shape=None):
        """
        Returns a widget representing control
        """

    @classmethod
    def paint(self, control, painter, rectangle, option=None):
        """
        Paints widget using painter.
        This function never modify control.
        """


class IConstraintWidget(IInterface):
    def constraints(self):
        """
        Returns a dict "constraint name" -> "value"
        """


