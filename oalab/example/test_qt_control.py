
from openalea.vpltk.qt import QtGui
import openalea.oalab.service.qt_control as scontrol
from openalea.core.service.interface import new_interface, interfaces, load_interfaces
from openalea.core.control import Control
from openalea.core.control.manager import ControlManager

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
        instance = QtGui.QApplication.instance()
        if instance is None:
            app = QtGui.QApplication([])
        else:
            app = instance

        interface = new_interface(args.iname, value=eval(args.value), **eval(args.constraints))
        control = Control('a', interface, value=eval(args.value), widget=args.widget)
        w = ControlWidgetTester(control, sys.argv[2:])
        w.show()
        w.raise_()

        if instance is None:
            app.exec_()
