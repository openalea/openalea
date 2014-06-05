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


class IControlWidget(object):
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


class AbstractControlWidget(AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        self._control_in = None
        self._control_out = None
        self.value_changed_signal = None

    def set(self, control, autoread=True, autoapply=True):
        self.autoread(control, autoread)
        self.autoapply(control, autoapply)

    def autoread(self, control, auto=True):
        if auto is True:
            self._control_in = control
            self._control_in.register_listener(self)
            self.read(control)
        else:
            if self._control_in is not None:
                self._control_in.unregister_listener(self)
                self._control_in = None
            # unregister listener

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
            if self.value_changed_signal:
                self.value_changed_signal.connect(self.on_value_changed)
        else:
            self._control_out = None
            if self.value_changed_signal:
                self.disconnect(self, QtCore.SIGNAL(self.value_changed_signal.signal), self.on_value_changed)


    def on_value_changed(self, value):
        if self._control_out:
            self.apply(self._control_out)

    def apply(self, control):
        control.value = self.value()

    def read(self, control):
        self.reset(control.value)

    def notify(self, sender, event):
        signal, value = event
        if signal == 'value_changed':
            self.read(sender)

    def reset(self, value=0, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

class BoolCheckBox(QtGui.QCheckBox, AbstractControlWidget):

    def __init__(self):
        QtGui.QCheckBox.__init__(self)
        AbstractControlWidget.__init__(self)
        self.value_changed_signal = self.stateChanged

    def reset(self, value=0, *kargs):
        self.setChecked(value)

    def setValue(self, value):
        return self.setChecked(value)

    def value(self):
        return self.isChecked()

class AbstractIntWidget(AbstractControlWidget):
    def __init__(self):
        AbstractControlWidget.__init__(self)

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        self.setValue(value)
        if maximum is not None:
            self.setMinimum(minimum)
        if minimum is not None:
            self.setMaximum(maximum)

    def read(self, control):
        mini = control.interface.min
        maxi = control.interface.max
        self.reset(control.value, minimum=mini, maximum=maxi)

    def apply(self, control):
        AbstractControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()



class IntSpinBox(QtGui.QSpinBox, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged

class IntSimpleSlider(QtGui.QSlider, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSlider.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged

class IntSlider(QtGui.QWidget, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """
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
        self.setMinimumHeight(20)
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
        self.setValue(value)

        if minimum is not None:
            self.slider.setMinimum(minimum)
            self.spinbox.setMinimum(minimum)

        if maximum is not None:
            self.slider.setMaximum(maximum)
            self.spinbox.setMaximum(maximum)

    def apply(self, control):
        AbstractControlWidget.apply(self, control)
        control.interface.min = self.slider.minimum()
        control.interface.max = self.slider.maximum()

    def value(self):
        return self.spinbox.value()

    def setValue(self, value):
        self.slider.setValue(value)
        self.spinbox.setValue(value)

class IntDial(QtGui.QDial, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QDial.__init__(self)
        AbstractIntWidget.__init__(self)

