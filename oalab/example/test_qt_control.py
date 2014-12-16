
from openalea.vpltk.qt import QtGui, QtCore
from control_sizes import Ui_Form

import openalea.oalab.service.qt_control as scontrol
from openalea.core.control import Control
from openalea.oalab.gui.control.qcontainer import QControlContainer


class CheckSizes(Ui_Form, QtGui.QWidget):

    def __init__(self, iname='IInt', widget=None, edit_mode='edit'):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        self.l_title.setText('%s, %s, %s' % (iname, widget, edit_mode))

        self._control = Control('a', iname, widget=widget)
        self._qcontainer = QControlContainer()
        self._qcontainer.add_control(self._control)
        self._qcontainer.create_actions(self)

#        m = getattr(scontrol, '%s_qt' % edit_mode)
        m = getattr(scontrol, 'qt_editor')

        self._qtcontrols = []

        valid_widget_shape = None
        for shape in ['vline', 'hline', 'small', 'large', 'responsive']:
            layout = getattr(self, 'l_%s' % shape)
            widget = m(self._control, shape=shape)
            if widget:
                layout.addWidget(widget)
                valid_widget_shape = shape
                self._qtcontrols.append(widget)
            else:
                layout.addWidget(QtGui.QLabel("X"))

        if valid_widget_shape:
            self._test_widget = m(self._control, shape=valid_widget_shape)
            self.layout_sample.addWidget(self._test_widget)
            self.cb_read.toggled.connect(self.on_mode_changed)
            self.cb_apply.toggled.connect(self.on_mode_changed)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        menu.addActions(self._qcontainer.actions())
        menu.exec_(event.pos())

    def on_mode_changed(self, state):
        autoread = self.cb_read.isChecked()
        autoapply = self.cb_apply.isChecked()
        for widget in self._qtcontrols:
            widget.autoapply(self._control, autoapply)
            widget.autoread(self._control, autoread)


if __name__ == '__main__':

    import sys

    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    w = CheckSizes(*sys.argv[1:])
    w.show()
    w.raise_()

    if instance is None:
        app.exec_()
