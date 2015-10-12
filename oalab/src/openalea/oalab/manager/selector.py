# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
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

from openalea.oalab.utils import obj_icon, ModalDialog
from openalea.oalab.widget.pages import WelcomePage
from openalea.vpltk.qt import QtGui, QtCore


class ManagerItemSelector(WelcomePage):
    item_selected = QtCore.Signal(object)

    def __init__(self, manager, group='default', parent=None, style=None):
        """
        items: function returning items for a given group
        """
        self.manager = manager
        if style is None:
            style = WelcomePage.STYLE_MEDIUM
        WelcomePage.__init__(self, parent=parent, style=style)

        self._actions = {}
        items = sorted(self.manager.items(group), key=lambda item: item.label)
        self._sorted_actions = []
        for item in items:
            action = QtGui.QAction(obj_icon(item), item.label, self)
            action.triggered.connect(self._on_action_triggered)
            self._actions[action] = item
            self._sorted_actions.append(action)

        self.set_actions(self._sorted_actions)

    def _on_action_triggered(self):
        plugin_class = self._actions[self.sender()]
        self.plugin_class = plugin_class
        self.item_selected.emit(plugin_class)

    def resize(self, *args, **kwargs):
        WelcomePage.resize(self, *args, **kwargs)
        self.set_actions(self._sorted_actions)


def select_manager_item(manager, group, parent=None, **kwargs):
    """
    kwargs:
        - size: tuple (width, height) [default: (640,480)]
        - title: unicode [default: "Select plugin"]
    """
    size = kwargs.pop('size', None)
    style = kwargs.pop('style', None)
    title = kwargs.pop('title', 'Select plugin')
    selector = ManagerItemSelector(manager, group, style=style)
    selector.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    if size:
        selector.resize(*size)
    dialog = ModalDialog(selector, parent=parent, buttons=QtGui.QDialogButtonBox.Cancel)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.setWindowTitle(title)
    selector.item_selected.connect(dialog.accept)
    if dialog.exec_():
        plugin_class = selector.plugin_class
    else:
        plugin_class = None
    del dialog
    del selector
    return plugin_class


if __name__ == '__main__':
    import sys
    from openalea.vpltk.qt import QtGui
    from openalea.core.service.project import default_project_manager
    from openalea.core.service.plugin import default_plugin_manager

    instance = QtGui.QApplication.instance()
    if instance is None:
        qapp = QtGui.QApplication(sys.argv)
    else:
        qapp = instance

    plm = default_plugin_manager()
    pm = default_project_manager()
    managers = [
        (pm, 'local'),
        (plm, 'oalab.applet'),
        (plm, 'oalab.lab'),
        (plm, 'openalea.image'),
    ]

    class TestPluginSelector(QtGui.QWidget):

        def __init__(self):
            QtGui.QWidget.__init__(self)
            layout = QtGui.QVBoxLayout(self)

            self.pb_select = QtGui.QPushButton('select')
            self.cb_category = QtGui.QComboBox()
            self.e_size = QtGui.QLineEdit("400x400")

            for manager, group in managers:
                self.cb_category.addItem(group, manager)

            self.pb_select.clicked.connect(self.select)

            layout.addWidget(self.cb_category)
            layout.addWidget(self.e_size)
            layout.addWidget(self.pb_select)

        def select(self):
            x, y = self.e_size.text().split('x')
            x = int(x)
            y = int(y)
            group = self.cb_category.currentText()
            idx = self.cb_category.currentIndex()
            manager = self.cb_category.itemData(idx)

            print select_manager_item(manager, group, size=(x, y))

    widget = TestPluginSelector()
    widget.show()

    if instance is None:
        qapp.exec_()
