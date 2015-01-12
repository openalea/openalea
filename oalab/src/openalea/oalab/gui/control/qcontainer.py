# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
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

from openalea.vpltk.qt import QtCore, QtGui
from openalea.core.control import Control
from openalea.core.control.manager import ControlContainer


class QControlContainer(QtCore.QObject, ControlContainer):
    controlValueChanged = QtCore.Signal(object, object)

    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self)
        ControlContainer.__init__(self, *args, **kwargs)
        self._action = {}
        self._control = {}

    def notify(self, sender, event):
        if isinstance(sender, Control):
            signal, data = event
            if signal == 'value_changed':
                self.controlValueChanged.emit(sender, data)
                if 'IBool' in str(sender.interface.__class__):
                    action = self._action[sender]
                    action.setChecked(sender.value)

    def create_actions(self, parent):
        for control in self.controls():
            interface = control.interface
            alias = control.alias
            action = QtGui.QAction(alias, parent)
            self._control[action] = control
            self._action[control] = action
            if'IBool' in str(interface.__class__):
                action.setCheckable(True)
                action.setChecked(control.value)
                action.toggled.connect(self._on_action_toggled)
            else:
                action.triggered.connect(self._on_action_triggered)

    def actions(self):
        return self._action.values()

    def _on_action_triggered(self, *args):
        control = self._control[self.sender()]

        from openalea.oalab.service.qt_control import qt_dialog
        value = qt_dialog(control, autoapply=False)
        if value is not None:
            control.value = value

    def _on_action_toggled(self, toggled):
        control = self._control[self.sender()]
        control.value = toggled
