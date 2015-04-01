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

from openalea.vpltk.qt import QtGui, QtCore

from openalea.core.observer import AbstractListener

from openalea.oalab.plugins.controls.constraints import IntConstraintWidget, FloatConstraintWidget
from openalea.oalab.plugins.controls.widgets import IntSimpleSlider, IntSpinBox, IntSlider, IntDial
from openalea.oalab.plugins.controls.widgets import FloatSlider, FloatSpinBox, FloatSimpleSlider
from openalea.oalab.plugins.controls.widgets import BoolCheckBox
from openalea.oalab.plugins.controls.widgets import IntRangeSpinBoxes, IntRangeSimpleSlider, IntRangeSlider
from openalea.oalab.plugins.controls.widgets import ColormapRectangle, ColormapSwitcher

from openalea.oalab.plugins.controls.painters import PainterColormap


class IntWidgetSelector(object):

    @classmethod
    def edit(cls, control, shape=None):
        if shape is None:
            shape = 'hline'

        if shape == 'hline':
            widget = IntSlider()
        elif shape == 'vline':
            widget = IntSimpleSlider()
            widget.setOrientation(QtCore.Qt.Vertical)
        elif shape in ('large', 'small', 'responsive'):
            widget = IntDial()
        else:
            widget = None
        return widget

    @classmethod
    def edit_constraints(cls):
        widget = IntConstraintWidget()
        return widget


class FloatWidgetSelector(object):

    @classmethod
    def edit(cls, control, shape=None):
        if shape is None:
            shape = 'hline'

        elif shape in ('large', 'hline'):
            # widget = FloatSimpleSlider()
            widget = FloatSlider()
            # widget = FloatSpinBox()
        elif shape == 'vline':
            widget = FloatSimpleSlider()
            widget.setOrientation(QtCore.Qt.Vertical)
            # widget = FloatSpinBox()
        elif shape in ('small', 'responsive'):
            widget = FloatSpinBox()
        else:
            widget = None
        return widget

    @classmethod
    def edit_constraints(cls):
        widget = FloatConstraintWidget()
        return widget


class IntRangeWidgetSelector(object):

    @classmethod
    def edit(cls, control, shape=None):
        if shape is None:
            shape = 'hline'

        elif shape in ('large', 'hline'):
            widget = IntRangeSimpleSlider()
        elif shape == 'vline':
            widget = IntRangeSimpleSlider()
            widget.setOrientation(QtCore.Qt.Vertical)
        elif shape in ('small', 'responsive'):
            widget = IntRangeSpinBoxes()
        else:
            widget = None
        return widget

    @classmethod
    def edit_constraints(cls):
        widget = IntConstraintWidget()
        return widget


class ColormapWidgetSelector(object):

    @classmethod
    def edit(cls, control, shape=None):
        if shape is None:
            shape = 'hline'

        elif shape in ('hline', 'responsive', 'large'):
            widget = ColormapSwitcher()
        elif shape == 'vline':
            widget = ColormapRectangle()
            widget.setOrientation(QtCore.Qt.Vertical)
        elif shape in ('small'):
            widget = ColormapRectangle()
        else:
            widget = None
        return widget

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterColormap()
