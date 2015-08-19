

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.utils import obj_icon
from openalea.oalab.testing.applet import test_applet


class TestApplet(QtGui.QLineEdit):

    def __init__(self):
        QtGui.QLineEdit.__init__(self, "I am a test applet")
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        icon = obj_icon(None)
        self.action_1 = QtGui.QAction(icon, 'A1 [widget.actions]', self)
        self.addAction(self.action_1)

        self.action_global_1 = QtGui.QAction(icon, 'Big 1 [widget.global_tb_actions]', self)
        self.action_global_2 = QtGui.QAction(icon, 'Small 1 [widget.global_tb_actions]', self)
        self.action_global_3 = QtGui.QAction(icon, 'Small 2 [widget.global_tb_actions]', self)

        self.action_context_1 = QtGui.QAction(icon, 'Big A [widget.tb_actions]', self)
        self.action_context_2 = QtGui.QAction(icon, 'Small A [widget.tb_actions]', self)
        self.action_context_3 = QtGui.QAction(icon, 'Small B [widget.tb_actions]', self)

        self.menu_tb = QtGui.QMenu("Toolbutton", self)
        self.menu_tb.addActions([self.action_context_1, self.action_context_2])

        self.action_search = QtGui.QAction(icon, 'search', self)

        self.menu_edit = QtGui.QMenu("Edit", self)
        self.menu_edit.addAction(self.action_search)

        self.action_menu_1 = QtGui.QAction(icon, 'A1 [widget.menu_actions]', self)

        self.toolbar_1 = QtGui.QToolBar("Toolbar 1")
        self.toolbar_1.addAction(self.action_context_1)
        self.toolbar_2 = QtGui.QToolBar("Toolbar 2")
        self.toolbar_2.addAction(self.action_context_2)

    def toolbars(self):
        """
        Optional: return a list of QToolBar
        """
        return [self.toolbar_1, self.toolbar_2]

    def global_toolbar_actions(self):
        return [
            dict(action=self.action_global_1),
            dict(action=self.action_global_2, style=1),
            dict(action=self.action_global_3, style=1)
        ]

    def toolbar_actions(self):
        return [
            dict(action=self.action_context_1),
            dict(action=self.action_context_2, style=1),
            dict(action=self.action_context_3, style=1),
            self.menu_tb
        ]

    def menus(self):
        return [self.menu_edit]

    def menu_actions(self):
        return [self.menu_edit, self.action_menu_1]

    def initialize(self):
        print "initialize", self


class TestAppletPlugin(object):
    name = 'TestApplet'
    label = 'Test Applet'

    def __call__(self):
        return TestApplet


from openalea.core.service.plugin import register_plugin, plugins
from openalea.core.util import camel_case_to_lower
register_plugin('oalab.applet', TestAppletPlugin)

if __name__ == '__main__':
    SAMPLE_WIDGET = 'FileBrowser'
    sample_widget = camel_case_to_lower(SAMPLE_WIDGET)

    def hello_world():
        print 'Hello OpenAleaLab world'

    def change_applet(applet_name='TestApplet'):
        widget = ns[sample_widget]
        widget.parent_tab.set_applet(applet_name)

    test_applet(SAMPLE_WIDGET, tests=[hello_world, change_applet])
