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


class AbstractControlWidget(AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        self._control_in = None

    def set(self, control, autoread=True, autoapply=True):
        self.autoread(control, autoread)
        self.autoapply(control, autoapply)

    def apply(self, control):
        control.value = self.value()

    def read(self, control):
        self.reset(control.value)

    def notify(self, sender, event):
        # If autoread is False, widget is not registered as listener, so this method is never called automatically
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

    def on_value_changed(self, *args, **kwargs):
        raise NotImplementedError

    def reset(self, value=None, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

class AbstractQtControlWidget(AbstractControlWidget):
    def __init__(self):
        AbstractControlWidget.__init__(self)

        self._control_out = None
        self.value_changed_signal = None

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
            signal = self.value_changed_signal
            if signal:
                if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
                    signal.connect(self.on_value_changed)
                elif isinstance(signal, basestring):
                    self.connect(self, QtCore.SIGNAL(signal), self.on_value_changed)
                else:
                    raise NotImplementedError, 'Signal %s support is not implemented' % signal
        else:
            self._control_out = None
            signal = self.value_changed_signal
            if signal:
                if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
                    signal = signal.signal
                elif isinstance(signal, basestring):
                    pass
                else:
                    raise NotImplementedError, 'Signal %s support is not implemented' % signal
                self.disconnect(self, QtCore.SIGNAL(signal), self.on_value_changed)

    def on_value_changed(self, *args, **kwargs):
        if self._control_out:
            self.apply(self._control_out)

    def reset(self, value=None, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


