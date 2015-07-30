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

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.widget.pages import WelcomePage
from openalea.core.service.plugin import plugins
from openalea.core.service.introspection import label
from openalea.oalab.utils import obj_icon, ModalDialog


class PluginSelector(WelcomePage):
    pluginSelected = QtCore.Signal(object)

    def __init__(self, category, parent=None):
        WelcomePage.__init__(self, parent=parent)

        self._actions = {}
        self._sorted_actions = []
        for plugin_class in plugins(category):
            action = QtGui.QAction(obj_icon(plugin_class), label(plugin_class), self)
            action.triggered.connect(self._on_action_triggered)
            self._actions[action] = plugin_class
            self._sorted_actions.append(action)

        self.set_actions(self._sorted_actions)

    def _on_action_triggered(self):
        plugin_class = self._actions[self.sender()]
        self.plugin_class = plugin_class
        self.pluginSelected.emit(plugin_class)

    def resize(self, *args, **kwargs):
        WelcomePage.resize(self, *args, **kwargs)
        self.set_actions(self._sorted_actions)


def select_plugin(category, parent=None, **kwargs):
    """
    kwargs:
        - size: tuple (width, height) [default: (640,480)]
        - title: unicode [default: "Select plugin"]
    """
    size = kwargs.pop('size', (640, 480))
    title = kwargs.pop('title', 'Select plugin')
    selector = PluginSelector(category)
    selector.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    selector.resize(*size)
    dialog = ModalDialog(selector, parent=parent, buttons=QtGui.QDialogButtonBox.Cancel)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.resize(*size)
    dialog.setWindowTitle(title)
    selector.pluginSelected.connect(dialog.accept)
    if dialog.exec_():
        plugin_class = selector.plugin_class
    else:
        plugin_class = None
    del dialog
    del selector
    return plugin_class

if __name__ == '__main__':
    import sys
    import inspect
    from openalea.vpltk.qt import QtGui
    from openalea.core.plugin import iter_groups

    instance = QtGui.QApplication.instance()
    if instance is None:
        qapp = QtGui.QApplication(sys.argv)
    else:
        qapp = instance

    class TestPluginSelector(QtGui.QWidget):

        def __init__(self):
            QtGui.QWidget.__init__(self)
            layout = QtGui.QVBoxLayout(self)

            self.pb_select = QtGui.QPushButton('select')
            self.cb_category = QtGui.QComboBox()
            self.e_size = QtGui.QLineEdit("400x400")

            for category in ['oalab.lab', 'oalab.applet']:
                self.cb_category.addItem(category)

            self.pb_select.clicked.connect(self.select)

            layout.addWidget(self.cb_category)
            layout.addWidget(self.e_size)
            layout.addWidget(self.pb_select)

        def select(self):
            x, y = self.e_size.text().split('x')
            x = int(x)
            y = int(y)
            print select_plugin(category=str(self.cb_category.currentText()), size=(x, y))

    widget = TestPluginSelector()
    widget.show()

    if instance is None:
        qapp.exec_()
