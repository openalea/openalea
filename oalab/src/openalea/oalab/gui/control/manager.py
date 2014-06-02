
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener

from openalea.oalab.gui.control.model_view import ControlModel, ControlView
from openalea.oalab.control.manager import ControlManager

class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        self._manager = ControlManager()

        self.model_global = ControlModel(self._manager)
        self.model_local = ControlModel(self._manager)

        self.view_global = ControlView()
        self.view_global.setModel(self.model_global)
        self.view_global.pressed.connect(self.on_global_control_selected)

        self.view_local = ControlView()
        self.view_local.setModel(self.model_local)
        self.view_local.pressed.connect(self.on_local_control_selected)

        self.l_local_control_name = QtGui.QLabel()
        self.setModel(None)

        self._layout.addWidget(QtGui.QLabel("Global controls"))
        self._layout.addWidget(self.view_global)
        self._layout.addWidget(self.l_local_control_name)
        self._layout.addWidget(self.view_local)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._i = 1

    def on_global_control_selected(self, index):
        print 'global:',
        self.on_control_selected(index, self.model_global)

    def on_local_control_selected(self, index):
        print 'local:',
        self.on_control_selected(index, self.model_local)

    def on_control_selected(self, index, model):
        print model.control(index)

    def setModel(self, model_uid=None):
        if model_uid is None :
            self.l_local_control_name.setText("Local controls")
            self.model_local.set(False)
        else :
            self.l_local_control_name.setText("%s controls" % model_uid)
            self.model_local.set(model_uid)
