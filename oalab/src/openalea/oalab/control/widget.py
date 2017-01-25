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


from Qt import QtCore

from openalea.core.observer import AbstractListener

class AbstractControlWidget(AbstractListener):

    """
    Use this class to create a new user control.
    For Qt control, you may prefer AbstractQtControlWidget or OpenAleaControlWidget
    """

    def __init__(self):
        AbstractListener.__init__(self)
        self._control_in = None
        self._control_out = None

    def set(self, control, autoread=True, autoapply=True):
        # TODO: order is important due to auto synchronization! Fix it
        self._control_out = control
        self.autoread(control, autoread)
        self.autoapply(control, autoapply)

    def apply(self, control):
        control.value = self.value()

    def read(self, control):
        self.reset(control.value)

    def notify(self, sender, event):
        # If autoread is False, widget is not registered as listener,
        # so this method is never called automatically
        if event is None:
            return
        signal, value = event
        if signal == 'value_changed':
            self.read(sender)

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
        raise NotImplementedError

    def reset(self, value=None, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


class AbstractQtControlWidget(AbstractControlWidget):

    """
    Use this class if you want to create a Qt control widget from
    a classic Qt widget.

    A classic Qt widget is a widget with:
        - a method to get widget value (like value(), text(), isChecked(), ...)
        - a method to set widget value (like setValue(value), setText(text), ...)
        - a signal emit when value changes (valueChanged, toggled, ...)

    To Create you control widget, just define, if not exists:
        - reset(value, **constraints)
        - setValue(value)
        - value(interface=None)

    You must also define in __init__, what signal you want to use to track data changes:

    .. code-block::

        class MyControlWidget(MyWidget, AbstractQtControlWidget)
            def __init__(self):
                AbstractQtControlWidget.__init__(self)
                MyWidget.__init__(self)

                self.value_changed_signal = self.toggled
                # If you widget uses old style signal syntax, you can write
                self.value_changed_signal = 'toggled(bool)'
    """

    def __init__(self):
        AbstractControlWidget.__init__(self)

        self._control_out = None
        self.value_changed_signal = None

    def _connect(self, method):
        signal = self.value_changed_signal
        if signal:
            signal.connect(method)

            # if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
            #     signal.connect(method)
            # elif isinstance(signal, basestring):
            #     self.connect(self, QtCore.SIGNAL(signal), method)
            # else:
            #     raise NotImplementedError, 'Signal %s support is not implemented' % signal

    def _disconnect(self, method):
        signal = self.value_changed_signal
        if signal:
            if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
                signal = signal.signal
            elif isinstance(signal, basestring):
                pass
            else:
                raise NotImplementedError, 'Signal %s support is not implemented' % signal
            self.disconnect(self, QtCore.SIGNAL(signal), method)

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
            self._connect(self._on_value_changed)
        else:
            self._control_out = None
            self._disconnect(self._on_value_changed)

    def _on_value_changed(self, *args, **kwargs):
        if self._control_out:
            self.apply(self._control_out)

    def reset(self, value=None, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


class OpenAleaControlWidget(AbstractControlWidget):

    """
    Use this class if you want to create a Qt control widget from
    a visualea Node/Interface widget.
    """

    def __init__(self):
        self._control_out = None
        self._control_in = None
        AbstractControlWidget.__init__(self)

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
        else:
            self._control_out = None

    def read(self, control):
        self.reset(control.value, interface=control.interface)

    def reset(self, value=None, *kargs, **kwds):
        if hasattr(self, 'set_interface'):
            self.set_interface(kwds.get('interface'))
        if value is None:
            if self.__interface__:
                value = self.__interface__.default()
        if value is not None:
            self.setValue(value)

    def setValue(self, value):
        self.set_widget_value(value)

    def value(self, interface=None):
        return self.get_widget_value()

    def set_value(self, newval):
        if self._control_out:
            self._control_out.value = newval

    def get_value(self):
        if self._control_in:
            return self._control_in.value

    def get_state(self):
        return ""

    def internal_data(self):
        "return a dict: minimal"
        return dict()

    @classmethod
    def get_label(self, node, parameter_str):
        return ''

    def unvalidate(self):
        """
        Method called when data changes.
        We use this method to auto apply change if mode is enabled.
        """
        if self._control_out:
            self.apply(self._control_out)
