# -*- coding: utf-8 -*-

from openalea.vpltk.qt import QtCore, QtGui
from openalea.oalab.gui.control.widget import AbstractQtControlWidget

"""
For documentation, see :class:`~openalea.oalab.plugins.control`
"""


class BoolCheckBox(QtGui.QCheckBox, AbstractQtControlWidget):

    def __init__(self):
        QtGui.QCheckBox.__init__(self)
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


class StrLineEdit(QtGui.QLineEdit, AbstractQtControlWidget):

    def __init__(self):
        QtGui.QLineEdit.__init__(self)
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



class QFloatSlider(QtGui.QSlider):

    floatValueChanged = QtCore.Signal(float)

    def __init__(self,orientation=QtCore.Qt.Horizontal):
        QtGui.QSlider.__init__(self,orientation)
        self.connect(self,QtCore.SIGNAL('valueChanged(int)'),self.notifyValueChanged)
        self.slider_step = 0.1
        self.floatValue = 0.0

    def notifyValueChanged(self,value):
        self.floatValue = value*self.slider_step
        self.floatValueChanged.emit(self.floatValue)

    def setFloatValue(self,value):
        self.setValue(int(value/self.slider_step))

    def value(self):
        return self.floatValue

    def setStep(self,step):
        self.slider_step = step


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
        # self.reset(control.value, minimum=mini, maximum=maxi, step=step)
        self.reset(control.value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()
        control.interface.step = self.step()


class FloatSlider(QtGui.QWidget, AbstractFloatWidget):
    valueChanged = QtCore.Signal(float)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.slider = QFloatSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QDoubleSpinBox()

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
        self.slider.floatValueChanged.connect(self.valueChanged)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.slider.setMinimum(minimum/step)
            self.spinbox.setMinimum(minimum)
        if maximum is not None:
            self.slider.setMaximum(maximum/step)
            self.spinbox.setMaximum(maximum)
        self.spinbox.setSingleStep(step)
        self.slider.setStep(step)

        self.setValue(value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.min = self.spinbox.minimum()
        control.interface.max = self.spinbox.maximum()
        control.interface.step = self.slider.slider_step

    def value(self, interface=None):
        return self.spinbox.value()

    def step():
        return self.slider.slider_step

    def setValue(self, value):
        self.slider.setFloatValue(value)
        self.spinbox.setValue(value)


class FloatSpinBox(QtGui.QDoubleSpinBox, AbstractFloatWidget):

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractFloatWidget.__init__(self)
        self.value_changed_signal = self.valueChanged

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

    def reset(self, value=1.0, minimum=0.0, maximum=1.0, step=0.01, **kwargs):
        if minimum is not None:
            self.setMinimum(minimum/step)
        if maximum is not None:
            self.setMaximum(maximum/step)
        self.setStep(step)
        self.setFloatValue(value)

    def step(self):
        return self.slider_step

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)
        control.interface.step = self.step()
        control.interface.min = self.minimum()*self.step()
        control.interface.max = self.maximum()*self.step()
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


class IntSpinBox(QtGui.QSpinBox, AbstractIntWidget):

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


class IntSimpleSlider(QtGui.QSlider, AbstractIntWidget):

    def __init__(self):
        QtGui.QSlider.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


class IntSlider(QtGui.QWidget, AbstractIntWidget):
    valueChanged = QtCore.Signal(int)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QSpinBox()

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

        layout = QtGui.QHBoxLayout(self)
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


class IntDial(QtGui.QDial, AbstractIntWidget):

    def __init__(self):
        QtGui.QDial.__init__(self)
        self.setNotchesVisible(True)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged
