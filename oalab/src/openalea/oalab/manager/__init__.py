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
            style = WelcomePage.STYLE_LARGE
        WelcomePage.__init__(self, parent=parent, style=style)

        self._actions = {}
        self._sorted_actions = []
        for item in self.manager.items(group):
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


def main():
    from openalea.core.service.project import default_project_manager
    from openalea.core.service.plugin import default_plugin_manager

    import sys

    def item_selected(item):
        print 'item selected: %s (%s)' % (item.label, item.name)

    plm = default_plugin_manager()
    pm = default_project_manager()

    app = QtGui.QApplication(sys.argv)
    widgets = []
    for manager, group in [
        (plm, 'oalab.applet'),
        (plm, 'oalab.lab'),
    ]:
        widget = ManagerItemSelector(manager, group)
        widget.item_selected.connect(item_selected)
        widget.show()
        widgets.append(widget)
    app.exec_()


if __name__ == "__main__":
    main()
