
import weakref
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.service.applet import new_applet
from openalea.oalab.gui.splitterui import SplittableUI, BinaryTree
from openalea.core.plugin.manager import PluginManager

class AppletSelector(QtGui.QWidget):

    appletChanged = QtCore.Signal(str)
    addTabClicked = QtCore.Signal()
    removeTabClicked = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout = QtGui.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._cb_applets = QtGui.QComboBox()
        self._applet_plugins = []

        self._cb_applets.addItem('Select applet')
        for plugin_class in plugins('oalab.applet'):
            self._applet_plugins.append(plugin_class)
            self._cb_applets.addItem(plugin_class.alias)

        self._layout.addWidget(self._cb_applets)

        self.setCurrentApplet('')
        self._cb_applets.currentIndexChanged.connect(self._on_current_applet_changed)

    def _on_current_applet_changed(self, idx):
        """
        Called when selected applet changes.
        Emit signal appletChanged(name)
        name = '' if applet not found or "select applet"
        """
        applet_name = self.applet(idx)
        if applet_name:
            self.appletChanged.emit(applet_name)
        else:
            self.appletChanged.emit('')

    def applet(self, idx):
        if 1 <= idx <= len(self._applet_plugins):
            plugin_class = self._applet_plugins[idx - 1]
            return plugin_class.name
        else:
            return None

    def currentApplet(self):
        return self.applet(self._cb_applets.currentIndex())

    def setCurrentApplet(self, name):
        self._cb_applets.setCurrentIndex(0)
        for i, plugin_class in enumerate(self._applet_plugins):
            if plugin_class.name == name:
                self._cb_applets.setCurrentIndex(i + 1)
                break


class AppletTabWidget(QtGui.QTabWidget):

    def __init__(self):
        QtGui.QTabWidget.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.tabCloseRequested.connect(self.remove_tab)
        self.setDocumentMode(True)
        self.setMovable(True)

        self._applets = {}
        self._name = {}
        self._current = None

        self.set_edit_mode()

    def tabInserted(self, index):
        self.tabBar().setVisible(self.count() > 1)

    def tabRemoved(self, index):
        self.tabBar().setVisible(self.count() > 1)

    def set_edit_mode(self, mode=True):
        self._edit_mode = mode
        self.setTabsClosable(mode)

    def new_tab(self):
        widget = QtGui.QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        layout = QtGui.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addTab(widget, '')
        self.setCurrentWidget(widget)

    def remove_tab(self, idx):
        if idx in self._applets:
            for applet in self._applets[idx].values():
                applet.close()
                del applet
            self._applets[idx] = {}
        self.removeTab(idx)

    def set_applet(self, name):
        # clear view
        for applet in self._applets.values():
            applet.hide()

        if name in self._applets:
            applet = self._applets[name]
            applet.show()
            self._name[self.currentIndex()] = name
        else:
            applet = pm.new('oalab.applet', name)
            self._applets[name] = applet
            if applet is None:
                return
            tab = self.currentWidget()
            tab.layout().addWidget(applet)
            self._name[self.currentIndex()] = name

    def currentApplet(self):
        try:
            return self._name[self.currentIndex()]
        except KeyError:
            return None

    def toString(self):
        layout = dict(applet=self._name.values(), position=self.tabPosition())
        return layout


class AppletContainer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, None)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self._edit_mode = True

        self._tabwidget = AppletTabWidget()
        self._tabwidget.currentChanged.connect(self._on_tab_changed)

        self._applet_selector = AppletSelector()
        self._applet_selector.appletChanged.connect(self._tabwidget.set_applet)
        self._applet_selector.addTabClicked.connect(self._tabwidget.new_tab)
        self._applet_selector.removeTabClicked.connect(self._tabwidget.remove_tab)

        self._layout.addWidget(self._tabwidget)
        self._layout.addWidget(self._applet_selector)

        self._tabwidget.new_tab()

        applet_name = self._applet_selector.currentApplet()
        if applet_name:
            self._tabwidget.set_applet(applet_name)

        # Menu if edit mode is OFF
        self.menu_edit_off = QtGui.QMenu(self)
        self.action_unlock = QtGui.QAction(qicon('oxygen_object-unlocked.png'), "Edit layout", self.menu_edit_off)
        self.action_unlock.triggered.connect(self.unlock_layout)
        self.menu_edit_off.addAction(self.action_unlock)

        # Menu if edit mode is ON
        self.menu_edit_on = QtGui.QMenu(self)

        self.action_lock = QtGui.QAction(qicon('oxygen_object-locked.png'), "Lock layout", self.menu_edit_on)
        self.action_lock.triggered.connect(self.lock_layout)

        self.action_add_tab = QtGui.QAction(qicon('Crystal_Clear_action_edit_add.png'), "Add tab", self.menu_edit_on)
        self.action_add_tab.triggered.connect(self._tabwidget.new_tab)

        self.action_remove_tab = QtGui.QAction(
            qicon('Crystal_Clear_action_edit_remove.png'), "Remove tab", self.menu_edit_on)
        self.action_remove_tab.triggered.connect(self._tabwidget.remove_tab)

        self.menu_edit_on.addAction(self.action_lock)
        self.menu_edit_on.addSeparator()
        self.menu_edit_on.addAction(self.action_add_tab)
        self.menu_edit_on.addAction(self.action_remove_tab)
        self.menu_edit_on.addSeparator()

        self._position_actions = {}
        for name, position in [
                ('top', QtGui.QTabWidget.North),
                ('right', QtGui.QTabWidget.East),
                ('bottom', QtGui.QTabWidget.South),
                ('left', QtGui.QTabWidget.West)]:
            action = QtGui.QAction("Move tab to %s" % name, self.menu_edit_on)
            action.triggered.connect(self._on_tab_position_changed)
            self.menu_edit_on.addAction(action)
            self._position_actions[action] = position

        self.set_edit_mode()

    def _on_tab_position_changed(self):
        self._tabwidget.setTabPosition(self._position_actions[self.sender()])

    def _on_tab_changed(self, idx):
        applet_name = self._tabwidget.currentApplet()
        if applet_name:
            self._applet_selector.setCurrentApplet(applet_name)

    def lock_layout(self):
        self.set_edit_mode(False)

    def unlock_layout(self):
        self.set_edit_mode(True)

    def set_edit_mode(self, mode=True):
        if mode:
            self._applet_selector.show()
        else:
            self._applet_selector.hide()
        self._edit_mode = mode
        self._tabwidget.set_edit_mode(mode)

    def contextMenuEvent(self, event):
        if self._edit_mode:
            self.menu_edit_on.exec_(event.globalPos())
        else:
            self.menu_edit_off.exec_(event.globalPos())

    def toString(self):
        return self._tabwidget.toString()


class OABinaryTree(BinaryTree):

    def toString(self, props=[]):
        filteredProps = {}
        for vid, di in self._properties.iteritems():
            filteredProps[vid] = {}
            for k, v in di.iteritems():
                if k in props:
                    if hasattr(v, 'toString'):
                        filteredProps[vid][k] = v.toString()
                    else:
                        filteredProps[vid][k] = v
        return repr(self._toChildren) + ", " + repr(self._toParents) + ", " + repr(filteredProps)


class InitContainerVisitor(object):

    """Visitor that searches which leaf id has pos in geometry"""

    def __init__(self, graph, wid):
        self.g = graph
        self.wid = wid

    def _to_qwidget(self, widget):
        if isinstance(widget, dict):
            position = widget.get('position', 0)
            applets = widget.get('applet', [])
            if applets is None:
                return widget
            container = AppletContainer()
            for i, name in enumerate(applets):
                if i:
                    container._tabwidget.new_tab()
                container._tabwidget.set_applet(name)
            widget = container
        return widget

    def visit(self, vid):
        """
        """
        if self.g.has_property(vid, 'widget'):
            widget = self.g.get_property(vid, "widget")
            widget = self._to_qwidget(widget)
        else:
            widget = None

        if not self.g.has_children(vid):
            self.wid._install_child(vid, widget)
            return False, False

        direction = self.g.get_property(vid, "splitDirection")
        amount = self.g.get_property(vid, "amount")
        self.wid._split_parent(vid, direction, amount)

        return False, False


class OALabSplittableUi(SplittableUI):

    reprProps = ["amount", "splitDirection", "widget"]

    def __init__(self, parent=None, content=None):
        """Contruct a SplittableUI.
        :Parameters:
         - parent (qt.QtGui.QWidget)  - The parent widget
         - content (qt.QtGui.QWidget) - The widget to display in pane at level 0
        """
        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        # -- our backbone: --
        self._g = OABinaryTree()
        # -- contains geometry information (a vid->QRect mapping) --
        self._geomCache = {}
        # -- initialising the pane at level 0 --
        self._geomCache[0] = self.contentsRect()
        self._install_child(0, content)

        self.set_edit_mode()

    def getPlaceHolder(self):
        return AppletContainer()

    def _install_child(self, paneId, widget, **kwargs):
        g = self._g

        # -- get the old content --
        oldWidget = None
        if g.has_property(paneId, "widget"):
            oldWidget = g.get_property(paneId, "widget")
            if isinstance(oldWidget, QtGui.QWidget):
                oldWidget.hide()

        # -- place the new content --
        if widget is not None:
            widget.setParent(self)
            widget.show()
        g.set_property(paneId, "widget", widget)

        if not kwargs.get("noTearOffs", False):
            self._install_tearOffs(paneId)
        return oldWidget

    @classmethod
    def fromString(cls, rep, parent=None):
        g, tup = OABinaryTree.fromString(rep)
        print g

        newWid = cls(parent=parent)
        w0 = newWid._uninstall_child(0)
        if w0:
            w0.setParent(None)
            w0.close()

        newWid._g = g
        visitor = InitContainerVisitor(g, newWid)
        g.visit_i_breadth_first(visitor)
        newWid._geomCache[0] = newWid.contentsRect()
        newWid.computeGeoms(0)
        return newWid

    def _onSplitRequest(self, paneId, orientation, amount):
        if self._edit_mode:
            SplittableUI._onSplitRequest(self, paneId, orientation, amount)
        else:
            return

    def set_edit_mode(self, mode=True):
        self._edit_mode = mode
        for properties in self._g._properties.values():

            # if 'handleWidget' in properties:
            #    properties['handleWidget'].setVisible(mode)

            if 'tearOffWidgets' in properties:
                for widget in properties['tearOffWidgets']:
                    widget.set_edit_mode(mode)

            if 'widget' in properties:
                widget = properties['widget']
                if widget:
                    widget.set_edit_mode(mode)


class OALabMainWin(QtGui.QMainWindow):

    def __init__(self, layout=None):
        QtGui.QMainWindow.__init__(self)

        menu_names = ('Project', 'Edit', 'Viewer', 'Help')

        # Classic menu
        self.menu_classic = {}
        menubar = QtGui.QMenuBar()

        for menu_name in menu_names:
            self.menu_classic[menu_name] = menubar.addMenu(menu_name)

        self.setMenuBar(menubar)

        if layout is None:
            container = AppletContainer()
            self.splittable = OALabSplittableUi(parent=self)
            self.splittable.setContentAt(0, container)
        else:
            self.splittable = OALabSplittableUi.fromString(str(layout))

        self.setCentralWidget(self.splittable)

    def set_edit_mode(self, mode=True):
        for widget in self.splittable.getAllContents():
            if hasattr(widget, 'set_edit_mode'):
                widget.set_edit_mode(mode)
        self.splittable.set_edit_mode(mode)

    def initialize(self):
        self.pm = PluginManager()
        for instance in plugin_instances('oalab.applet'):
            if hasattr(instance, 'initialize'):
                instance.initialize()

        menus = plugin_instances('oalab.applet', 'PanedMenu')
        if menus:
            self.menu = menus[0]
            for plugin_class in self.pm.plugins('oalab.applet'):
                # TODO: support name properly (class name or name attribute)
                for instance in plugin_instances('oalab.applet', plugin_class.name):
                    if hasattr(plugin_class, 'graft'):
                        instance.show()
                        plugin_class().graft(oa_mainwin=self, applet=instance)

    def add_action_to_existing_menu(self, action, menu_name, sub_menu_name):
        """
        Permit to add in a classic menubar the "action" in the menu "menu_name"
        in the sub_menu "sub_menu_name"
        """
        menubar = self.menuBar()
        if menu_name in self.menu_classic:
            menu = self.menu_classic[menu_name]
        else:
            menu = self.menu_classic[menu_name] = menubar.addMenu(menu_name)

        menu.addAction(action)

    def add_applet(self, *args, **kwds):
        pass

    def layout(self):
        return eval(self.splittable.toString())


if __name__ == '__main__':
    from openalea.core.service.ipython import interpreter
    interp = interpreter()

    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    oalab_conf = ({0: [1, 2], 2: [3, 4], 3: [5, 6], 6: [7, 8]},
                  {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 6, 8: 6},
                  {0: {'amount': 0.0645446507515473, 'splitDirection': 2},
                   1: {'widget': {'applet': ['PanedMenu'], 'position': 0}},
                   2: {'amount': 0.75, 'splitDirection': 2},
                   3: {'amount': 0.2, 'splitDirection': 1},
                   4: {'widget': {'applet': ['ShellWidget', u'Logger', u'HistoryWidget'],
                                  'position': 0}},
                   5: {'widget': {'applet': ['ProjectManager',
                                             'PkgManagerWidget',
                                             'ControlManager',
                                             'World'],
                                  'position': 0}},
                   6: {'amount': 0.6, 'splitDirection': 1},
                   7: {'widget': ['EditorManager']},
                   8: {'widget': ['Viewer3D', 'VtkViewer', 'HelpWidget']}})

    mw = OALabMainWin(layout=layout)
    interp.user_ns['mainwin'] = mw

    mw.resize(1024, 768)
    mw.show()

    mw.set_edit_mode(False)
    mw.initialize()

    def save(event):
        if layout_filepath.exists():
            layout_filepath.remove()
        layout_file = open(layout_filepath, 'w')
        layout_file.write(str(mw.layout()))
        layout_file.close()

    mw.closeEvent = save

    if instance is None:
        app.exec_()
