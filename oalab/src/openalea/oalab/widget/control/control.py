# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

# -*- coding: utf-8 -*-

"""
This module define Qt controls, ie QWidget able to edit control's values.

For documentation, see :class:`~openalea.oalab.plugins.control`
"""

from openalea.deploy.shared_data import shared_data

import openalea.oalab

from openalea.oalab.control.widget import AbstractQtControlWidget
from openalea.oalab.widget.basic import QFloatSlider, QSpanSlider, QColormapBar

from Qt import QtCore, QtGui, QtWidgets

class BoolCheckBox(QtWidgets.QCheckBox, AbstractQtControlWidget):

    def __init__(self):
        QtWidgets.QCheckBox.__init__(self)
        AbstractQtControlWidget.__init__(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAutoFillBackground(True)
        self.value_changed_signal = self.stateChanged

    def reset(self, value=0, *kargs):
        self.setChecked(value)

    def setValue(self, value):
        return self.setChecked(value)

    def value(self, interface=None):
        return self.isChecked()

class StrLineEdit(QtWidgets.QLineEdit, AbstractQtControlWidget):

    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        AbstractQtControlWidget.__init__(self)
        self.setMinimumHeight(20)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAutoFillBackground(True)
        self.value_changed_signal = self.editingFinished

    def reset(self, value='', *kargs):
        self.setText(value)

    def setValue(self, value):
        return self.setText(value)

    def value(self, interface=None):
        return self.text()


class AbstractFloatWidget(AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        self.setValue(value)

    def read(self, control):
        mini = control.interface.min
        maxi = control.interface.max
        step = control.interface.step
        self.reset(control.value, minimum=mini, maximum=maxi, step=step)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()
        control.interface.step = self.step()


class FloatSlider(QtWidgets.QWidget, AbstractFloatWidget):
    valueChanged = QtCore.Signal(float)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.slider = QFloatSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtWidgets.QDoubleSpinBox()

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractFloatWidget.__init__(self)

        # To be compatible with tree or table views, slider must keep focus
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMinimumHeight(22)
        self.spinbox.setMinimumHeight(18)
        self.slider.setMinimumHeight(18)

        self.slider.floatValueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setFloatValue)
        # self.slider.floatValueChanged.connect(self.valueChanged)
        self.spinbox.valueChanged.connect(self.valueChanged)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.slider.setMinimum(minimum / step)
            self.spinbox.setMinimum(minimum)
        if maximum is not None:
            self.slider.setMaximum(maximum / step)
            self.spinbox.setMaximum(maximum)
        self.spinbox.setSingleStep(step)
        if step < 0.01:
            self.spinbox.setDecimals(3)
        else:
            self.spinbox.setDecimals(2)
        self.slider.setStep(step)

        self.setValue(value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.spinbox.minimum()
        control.interface.max = self.spinbox.maximum()
        control.interface.step = self.spinbox.singleStep()

    def value(self, interface=None):
        return self.spinbox.value()

    def step(self):
        # return self.slider.slider_step
        return self.spinbox.singleStep()

    def setValue(self, value):
        self.slider.setFloatValue(value)
        self.spinbox.setValue(value)


class FloatSpinBox(QtWidgets.QDoubleSpinBox, AbstractFloatWidget):

    def __init__(self):
        QtWidgets.QSpinBox.__init__(self)
        AbstractFloatWidget.__init__(self)
        self.value_changed_signal = self.valueChanged
        self.setMinimumHeight(18)
        self.setMinimumWidth(48)

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        self.setSingleStep(step)
        self.setValue(value)

    def step(self):
        return self.singleStep()


class FloatSimpleSlider(QFloatSlider, AbstractFloatWidget):

    def __init__(self):
        QFloatSlider.__init__(self)
        AbstractFloatWidget.__init__(self)
        self.value_changed_signal = self.floatValueChanged
        self.setMinimumWidth(18)

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum / step)
        if maximum is not None:
            self.setMaximum(maximum / step)
        self.setStep(step)
        self.setFloatValue(value)

    def step(self):
        return self.slider_step

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.step = self.step()
        control.interface.min = self.minimum() * self.step()
        control.interface.max = self.maximum() * self.step()
        control.value = self.value()


class AbstractIntWidget(AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        self.setValue(value)

    def read(self, control):
        mini = control.interface.min
        maxi = control.interface.max
        self.reset(control.value, minimum=mini, maximum=maxi)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()


class IntSpinBox(QtWidgets.QSpinBox, AbstractIntWidget):

    def __init__(self):
        QtWidgets.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


class IntSimpleSlider(QtWidgets.QSlider, AbstractIntWidget):

    def __init__(self):
        QtWidgets.QSlider.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


class IntSlider(QtWidgets.QWidget, AbstractIntWidget):
    valueChanged = QtCore.Signal(int)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtWidgets.QSpinBox()

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractIntWidget.__init__(self)

        # To be compatible with tree or table views, slider must keep focus
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMinimumHeight(22)
        self.spinbox.setMinimumHeight(18)
        self.slider.setMinimumHeight(18)

        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.valueChanged)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        if minimum is not None:
            self.slider.setMinimum(minimum)
            self.spinbox.setMinimum(minimum)
        if maximum is not None:
            self.slider.setMaximum(maximum)
            self.spinbox.setMaximum(maximum)

        self.setValue(value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.slider.minimum()
        control.interface.max = self.slider.maximum()

    def value(self, interface=None):
        return self.spinbox.value()

    def setValue(self, value):
        self.slider.setValue(value)
        self.spinbox.setValue(value)


class IntDial(QtWidgets.QDial, AbstractIntWidget):

    def __init__(self):
        QtWidgets.QDial.__init__(self)
        self.setNotchesVisible(True)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


class AbstractIntRangeWidget(AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)

    def reset(self, value=(0, 255), minimum=0, maximum=255, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        self.setValue(value)

    def read(self, control):
        mini = control.interface.min
        maxi = control.interface.max
        self.reset(control.value, minimum=mini, maximum=maxi)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()


class IntRangeSpinBoxes(QtWidgets.QWidget, AbstractIntRangeWidget):
    valueChanged = QtCore.Signal(tuple)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.start_spinbox = QtWidgets.QSpinBox()
        self.end_spinbox = QtWidgets.QSpinBox()

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractIntRangeWidget.__init__(self)

        self.start_spinbox.setMinimumHeight(18)
        self.end_spinbox.setMinimumHeight(18)

        self.start_spinbox.valueChanged.connect(self.end_spinbox.setMinimum)
        self.end_spinbox.valueChanged.connect(self.start_spinbox.setMaximum)
        self.start_spinbox.valueChanged.connect(self.notify_start_value_changed)
        self.end_spinbox.valueChanged.connect(self.notify_end_value_changed)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.start_spinbox)
        layout.addWidget(self.end_spinbox)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=(0, 255), minimum=None, maximum=None, **kwargs):
        if minimum is not None:
            self.start_spinbox.setMinimum(minimum)
        if maximum is not None:
            self.end_spinbox.setMaximum(maximum)
        self.start_spinbox.setMaximum(value[1])
        self.end_spinbox.setMinimum(value[0])

        self.setValue(value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.start_spinbox.minimum()
        control.interface.max = self.end_spinbox.maximum()

    def value(self, interface=None):
        return (self.start_spinbox.value(), self.end_spinbox.value())

    def setValue(self, value):
        self.start_spinbox.setValue(value[0])
        self.start_spinbox.setMaximum(value[1])
        self.end_spinbox.setValue(value[1])
        self.end_spinbox.setMinimum(value[0])

    def notify_start_value_changed(self, value):
        self.valueChanged.emit((value, self.end_spinbox.value()))

    def notify_end_value_changed(self, value):
        self.valueChanged.emit((self.start_spinbox.value(), value))


class IntRangeSimpleSlider(QSpanSlider, AbstractIntRangeWidget):
    valueChanged = QtCore.Signal(tuple)

    def __init__(self):
        QSpanSlider.__init__(self)
        AbstractIntRangeWidget.__init__(self)
        self.spanChanged.connect(self.notify_value_changed)
        self.value_changed_signal = self.valueChanged

    def reset(self, value=(0, 255), minimum=0, maximum=255, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        self.setSpan(value[0], value[1])

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()
        control.value = self.value()

    def notify_value_changed(self, lower_value, upper_value):
        self.valueChanged.emit((lower_value, upper_value))

    def setValue(self, value):
        self.setSpan(value[0], value[1])

    def value(self, interface=None):
        return (self.lowerValue(), self.upperValue())


class IntRangeSlider(QtWidgets.QWidget, AbstractIntRangeWidget):
    valueChanged = QtCore.Signal(tuple)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.start_spinbox = QtWidgets.QSpinBox()
        self.end_spinbox = QtWidgets.QSpinBox()
        self.slider = QSpanSlider(QtCore.Qt.Horizontal)

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractIntRangeWidget.__init__(self)

        # To be compatible with tree or table views, slider must keep focus
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMinimumHeight(22)
        self.start_spinbox.setMinimumHeight(18)
        self.end_spinbox.setMinimumHeight(18)
        self.slider.setMinimumHeight(18)

        self.slider.lowerPositionChanged.connect(self.start_spinbox.setValue)
        self.slider.lowerPositionChanged.connect(self.end_spinbox.setMinimum)
        self.slider.upperPositionChanged.connect(self.end_spinbox.setValue)
        self.slider.upperPositionChanged.connect(self.start_spinbox.setMaximum)

        self.start_spinbox.valueChanged.connect(self.slider.setLowerValue)
        self.end_spinbox.valueChanged.connect(self.slider.setUpperValue)

        self.start_spinbox.valueChanged.connect(self.end_spinbox.setMinimum)
        self.end_spinbox.valueChanged.connect(self.start_spinbox.setMaximum)
        self.start_spinbox.valueChanged.connect(self.notify_start_value_changed)
        self.end_spinbox.valueChanged.connect(self.notify_end_value_changed)

        self.slider.spanChanged.connect(self.notify_value_changed)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.start_spinbox)
        layout.addWidget(self.slider)
        layout.addWidget(self.end_spinbox)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=(0, 255), minimum=None, maximum=None, **kwargs):
        if minimum is not None:
            self.slider.setMinimum(minimum)
            self.start_spinbox.setMinimum(minimum)
        if maximum is not None:
            self.slider.setMaximum(maximum)
            self.end_spinbox.setMaximum(maximum)
        self.start_spinbox.setMaximum(value[1])
        self.end_spinbox.setMinimum(value[0])

        self.setValue(value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.slider.minimum()
        control.interface.max = self.slider.maximum()
        control.value = self.value()

    def value(self, interface=None):
        return (self.slider.lowerValue(), self.slider.upperValue())

    def setValue(self, value):
        self.slider.setSpan(value[0], value[1])
        self.start_spinbox.setValue(value[0])
        self.start_spinbox.setMaximum(value[1])
        self.end_spinbox.setValue(value[1])
        self.end_spinbox.setMinimum(value[0])

    def notify_value_changed(self, lower_value, upper_value):
        self.valueChanged.emit((lower_value, upper_value))

    def notify_start_value_changed(self, value):
        self.valueChanged.emit((value, self.end_spinbox.value()))

    def notify_end_value_changed(self, value):
        self.valueChanged.emit((self.start_spinbox.value(), value))


class ColormapRectangle(QColormapBar, AbstractQtControlWidget):
    valueChanged = QtCore.Signal(dict)

    def __init__(self):
        QColormapBar.__init__(self)

        self.setAutoFillBackground(True)

        AbstractQtControlWidget.__init__(self)
        self.setMinimumHeight(40)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=dict(name='grey', color_points=dict(
            [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))])), **kwargs):
        self.setValue(value)

    def read(self, control):
        self.reset(control.value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)


class ColormapSwitcher(QtWidgets.QWidget, AbstractQtControlWidget):
    valueChanged = QtCore.Signal(dict)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.colormap_bar = QColormapBar()
        self.colormap_bar.setMinimumHeight(20)
        self.colormap_bar.setMinimumWidth(120)

        self.colormap_name = "grey"

        # self.label = QtWidgets.QLabel(self)
        # self.label.setText("Colormap")

        self.combobox = QtWidgets.QComboBox(self)

        # self.setMinimumHeight(50)

        colormap_names = []
        # colormaps_path = Path(shared_data(tissuelab, 'colormaps/grey.lut')).parent
        colormaps_path = shared_data(openalea.oalab) / 'colormaps'
        for colormap_file in colormaps_path.walkfiles('*.lut'):
            colormap_name = str(colormap_file.name[:-4])
            colormap_names.append(colormap_name)
        colormap_names.sort()

        # map between string and combobox index
        self.map_index = {}
        for s in colormap_names:
            self.combobox.addItem(s)
            self.map_index[s] = self.combobox.count() - 1
        self.combobox.setCurrentIndex(self.map_index[self.colormap_name])

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractQtControlWidget.__init__(self)

        self.combobox.currentIndexChanged.connect(self.updateColormap)
        self.colormap_bar.valueChanged.connect(self.valueChanged)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # line = QtWidgets.QHBoxLayout(self)
        # line.setContentsMargins(0, 0, 0, 0)

        # line.addWidget(self.label)
        # line.addWidget(self.combobox)
        # layout.addLayout(line)
        layout.addWidget(self.combobox)
        layout.addWidget(self.colormap_bar)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=dict(name='grey', color_points=dict(
            [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))])), **kwargs):
        self.setValue(value)

    def read(self, control):
        self.reset(control.value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)

    def value(self, interface=None):
        return self.colormap_bar.value()

    def setValue(self, value):
        self.colormap_bar.setValue(value)
        self.colormap_name = value['name']
        self.combobox.setCurrentIndex(self.map_index[self.colormap_name])

    def updateColormap(self, colormap_index):
        self.colormap_name = self.combobox.itemText(colormap_index)

        from openalea.oalab.colormap.colormap_utils import colormap_from_file
        colormap_path = shared_data(openalea.oalab, 'colormaps/' + self.colormap_name + '.lut')

        colormap = colormap_from_file(colormap_path, name=self.colormap_name)
        self.setValue(dict(name=self.colormap_name, color_points=colormap._color_points))

#
# control.py ends here
