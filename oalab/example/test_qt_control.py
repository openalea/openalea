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

from Qt import QtGui, QtWidgets

import openalea.oalab.service.qt_control as scontrol

from openalea.core.service.interface import new_interface, interfaces, load_interfaces
from openalea.core.control import Control
from openalea.core.control.manager import ControlManager

from openalea.oalab.control.qcontainer import QControlContainer
from openalea.oalab.control.model_view import ControlView, ControlModel

class CheckSizes(Ui_Form, QtGui.QWidget):

    def __init__(self, control, edit_mode='edit'):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        text = 'interface: %s, preferred widget: %s, edit mode: %s' % (control.interface, control.widget, edit_mode)
        self.l_title.setText(text)

        self._control = control

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
                layout.addWidget(QtWidgets.QLabel("X"))

        if valid_widget_shape:
            self._test_widget = m(self._control, shape=valid_widget_shape)
            self.layout_sample.addWidget(self._test_widget)
            self.cb_read.toggled.connect(self.on_mode_changed)
            self.cb_apply.toggled.connect(self.on_mode_changed)

        self._model = ControlModel(manager=self._qcontainer)
        self._view = ControlView()
        self._view.setModel(self._model)
        self._view.hideColumn(0)
        self.l_large_box.addWidget(self._view, 1, 1, 2, 1)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addActions(self._qcontainer.actions())
        menu.exec_(event.pos())

    def on_mode_changed(self, state):
        autoread = self.cb_read.isChecked()
        autoapply = self.cb_apply.isChecked()
        for widget in self._qtcontrols:
            widget.autoapply(self._control, autoapply)
            widget.autoread(self._control, autoread)
>>>>>>> MAJOR RESTRUCTURATION

from openalea.oalab.gui.control.widget_tester import ControlWidgetTester
from openalea.vpltk.qt.designer import generate_pyfile_from_uifile

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Test Qt controls')
    parser.add_argument('--iname', '-i', dest='iname', type=str, default='IInt',
                        help='interface name (ex: IInt, IBool, ..., def: IInt)')
    parser.add_argument('--value', '-v', dest='value', type=str, default='None',
                        help='evaluable string (ex: 1, True, "a", ...)')
    parser.add_argument('--constraints', '-c', dest='constraints', type=str,
                        default='{}',
                        help='evaluable constraints (def: {"min":1, max:"100"}')
    parser.add_argument('--widget', '-w', dest='widget', type=str, default=None,
                        help='prefered widget (ex: IntRadioButton  def: undef)')
    parser.add_argument('--list-interfaces', '-l', dest='list_interfaces', action='store_true',
                        help='list all known interfaces')
    parser.add_argument('--list-interface-widgets', dest='list_interface_widgets', action='store_true',
                        help='list all known interfaces')

    args = parser.parse_args()

    if args.list_interfaces or args.list_interface_widgets:
        inames = [interface.__name__ for interface in interfaces()]
        for interface in sorted(interfaces()):
            print '\033[41m', interface, '\033[0m', interface.__module__
            if args.list_interface_widgets:
                widgets = scontrol.qt_widget_plugins(interface.__name__)
                if widgets:
                    for plugin in widgets:
                        w = plugin.load()
                        print '    \033[36m%s\033[0m\n        plugin: %s\n        widget: %s)' % (plugin.name, plugin, w)
    else:
        instance = QtWidgets.QApplication.instance()
        if instance is None:
            app = QtWidgets.QApplication([])
        else:
            app = instance

        interface = new_interface(args.iname, value=eval(args.value), **eval(args.constraints))
        control = Control('a', interface, value=eval(args.value), widget=args.widget)
        w = ControlWidgetTester(control, sys.argv[2:])
        w.show()
        w.raise_()

        if instance is None:
            app.exec_()

#
# test_qt_control.py ends here
