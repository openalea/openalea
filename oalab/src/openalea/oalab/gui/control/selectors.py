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

from openalea.core.observer import AbstractListener
from openalea.oalab.gui.control.constraints import IntConstraintWidget
from openalea.vpltk.qt import QtGui, QtCore

class IWidgetSelector(AbstractListener):
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

class AbstractIntWidgetSelector(object):

    @classmethod
    def edit_constraints(cls):
        widget = IntConstraintWidget()
        return widget

from openalea.oalab.gui.control.widgets import IntSimpleSlider, IntSpinBox, IntSlider, IntDial, BoolCheckBox

class IntWidgetSelector(AbstractIntWidgetSelector):
    @classmethod
    def edit(cls, control, shape=None):
        if shape is None:
            shape = 'hline'

        if shape == 'hline':
            widget = IntSpinBox()
        elif shape == 'vline':
            widget = IntSimpleSlider()
            widget.setOrientation(QtCore.Qt.Vertical)
        elif shape in ('large', 'small', 'responsive'):
            widget = IntDial()
        else:
            widget = None
        return widget
