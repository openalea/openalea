

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.splittablewindow import TestMainWin, obj_icon


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


class TestAppletPlugin(object):
    name = 'TestApplet'
    alias = 'Test Applet'

    def __call__(self):
        return TestApplet


from openalea.core.plugin.manager import PluginManager
pm = PluginManager()
pm.discover('oalab.applet')
pm.add_plugin('oalab.applet', TestAppletPlugin)

if __name__ == '__main__':

    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    tissuelab_conf = {
        'children': {0: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 7: [11, 12], 8: [9, 10]},
        'parents': {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 8, 10: 8, 11: 7, 12: 7},
        'properties': {
            0: {'amount': 0.04774535809018567, 'splitDirection': 2},
            1: {'widget':
                {'applets': [
                    {'name': u'ContextualMenu'}],
                 'properties': {'position': 0}
                 }},
            2: {'amount': 0.1609375, 'splitDirection': 1},
            3: {'amount': 0.4850467289719626, 'splitDirection': 2},
            4: {'amount': 0.6540136901057871, 'splitDirection': 1},
            5: {'widget':
                {'applets': [
                    {'name': u'ProjectManager'}],
                 'properties': {'position': 0, 'title': '<b>Project</b>'}
                 }},
            6: {'widget':
                {'applets': [
                    {'name': u'ControlManager'},
                    {'name': u'World', 'properties': {'toolbar': True}},
                    {'name': u'PkgManagerWidget'}],
                 'properties': {'position': 0}
                 }},
            7: {'amount': 0.7252336448598131, 'splitDirection': 2},
            8: {'amount': 0.4803738317757009, 'splitDirection': 2},
            9: {'widget':
                {'applets': [
                    {'name': u'LineageViewer'},
                    {'name': u'FigureWidget'},
                    {'name': u'FigureWidget'}],
                 'properties': {'position': 2, 'title': '<b>2D</b> Viewers'}
                 }},
            10: {'widget':
                 {'applets': [
                     {'name': u'Viewer3D'},
                     {'name': u'VtkViewer'}],
                  'properties': {'position': 2, 'title': '<b>3D</b> Viewers'}}},
            11: {'widget':
                 {'applets': [
                     {'name': u'EditorManager'}],
                  'properties': {'position': 0}}},
            12: {'widget':
                 {'applets': [
                     {'name': u'ShellWidget'},
                     {'name': u'HistoryWidget'},
                     {'name': u'HelpWidget'},
                     {'name': u'Logger'}],
                  'properties': {'position': 2}
                  }}
        }}

    def hello_world():
        print 'Hello OpenAleaLab world'

    from openalea.core.service.plugin import PIM
    PIM.debug = True
    TestMainWin.DEFAULT_LAYOUT = tissuelab_conf
    mw = TestMainWin(tests=[hello_world])

    mw.resize(1024, 768)
    mw.showMaximized()
    mw.show()
    mw.set_edit_mode(False)

    mw.initialize()

    if instance is None:
        app.exec_()
