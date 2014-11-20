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

import weakref
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.service.applet import new_applet
from openalea.oalab.gui.splitterui import SplittableUI, BinaryTree
from openalea.core.service.plugin import (new_plugin_instance, plugin_instances, plugin_class,
                                          plugins, plugin_instance, plugin_instance_exists)
from openalea.oalab.gui.utils import qicon
from openalea.core.plugin.manager import PluginManager
import openalea.core


def obj_icon(obj):
    if hasattr(obj, 'icon'):
        return qicon(obj.icon)
    else:
        return qicon('Crystal_Clear_action_edit_add.png')


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
            self._cb_applets.addItem(obj_icon(plugin_class), plugin_class.alias)

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
    appletSet = QtCore.Signal(object, object)

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
        idx = self.currentIndex()
        old = self._name.get(idx, None)
        for applet in self._applets.get(idx, {}).values():
            applet.hide()

        if not name:
            return

        if name in self._name.get(idx, {}):
            applet = self._applets[idx][name]
            applet.show()
        else:
            # If applet is not yet instantiated, we instantiate it as the main instance (ie reachable thanks to plugin_instance)
            # else, just create a new one.
            if plugin_instance_exists('oalab.applet', name):
                applet = new_plugin_instance('oalab.applet', name)
            else:
                applet = plugin_instance('oalab.applet', name)
            if applet is None:
                return
            tab = self.currentWidget()
            tab.layout().addWidget(applet)
            self._applets.setdefault(idx, {})[name] = applet
            self._name[idx] = name

        _plugin_class = plugin_class('oalab.applet', name)

        #self.setTabText(idx, _plugin_class.alias)
        self.setTabIcon(idx, obj_icon(_plugin_class))
        self.setTabToolTip(idx, _plugin_class.alias)
        self.appletSet.emit(old, name)

    def currentApplet(self):
        try:
            return self._name[self.currentIndex()]
        except KeyError:
            return None

    def toString(self):
        layout = dict(applet=self._name.values(), position=self.tabPosition())
        return layout


class AppletContainer(QtGui.QWidget):
    appletSet = QtCore.Signal(object, object)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, None)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self._applets = []
        self._edit_mode = True

        self._tabwidget = AppletTabWidget()
        self._tabwidget.appletSet.connect(self.appletSet.emit)
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

    def emit_applet_set(self):
        for applet in self._applets:
            self.appletSet.emit(None, applet)

    def add_applets(self, applets, **kwds):
        position = kwds.pop('position', 0)
        for i, name in enumerate(applets):
            if i:
                self._tabwidget.new_tab()
            self._tabwidget.set_applet(name)
        self._tabwidget.setCurrentIndex(0)
        self._tabwidget.setTabPosition(position)
        self._applets = applets

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
            container.add_applets(applets, position=position)
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
            widget.emit_applet_set()
            return False, False

        direction = self.g.get_property(vid, "splitDirection")
        amount = self.g.get_property(vid, "amount")
        self.wid._split_parent(vid, direction, amount)

        return False, False


class OALabSplittableUi(SplittableUI):

    reprProps = ["amount", "splitDirection", "widget"]
    appletSet = QtCore.Signal(object, object)

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

        self._containers = {}

        self.set_edit_mode()

    def _connect_container(self, container):
        if isinstance(container, AppletContainer):
            if container not in self._containers:
                container.appletSet.connect(self.appletSet.emit)
                self._containers[container] = container

    def getPlaceHolder(self):
        container = AppletContainer()
        self._connect_container(container)
        return container

    def setContentAt(self, paneId, wid, **kwargs):
        self._connect_container(wid)
        return SplittableUI.setContentAt(self, paneId, wid, **kwargs)

    def _install_child(self, paneId, widget, **kwargs):
        g = self._g
        self._connect_container(widget)

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
    def FromString(cls, rep, parent=None):
        g, tup = OABinaryTree.fromString(rep)

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

    def fromString(self, rep, parent=None):
        g, tup = OABinaryTree.fromString(rep)

        w0 = self._uninstall_child(0)
        if w0:
            w0.setParent(None)
            w0.close()

        self._g = g
        visitor = InitContainerVisitor(g, self)
        g.visit_i_breadth_first(visitor)
        self._geomCache[0] = self.contentsRect()
        self.computeGeoms(0)

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
    appletSet = QtCore.Signal(object, object)
    DEFAULT_MENU_NAMES = ('Project', 'Edit', 'Viewer', 'Help')

    def __init__(self, layout=None):
        QtGui.QMainWindow.__init__(self)

        # Classic menu
        self.menu_classic = {}
        self._registered_applets = []
        menubar = QtGui.QMenuBar()

        for menu_name in self.DEFAULT_MENU_NAMES:
            self.menu_classic[menu_name] = menubar.addMenu(menu_name)

        self.setMenuBar(menubar)

        self.splittable = OALabSplittableUi(parent=self)
        self.splittable.appletSet.connect(self.appletSet.emit)
        self.appletSet.connect(self._on_applet_set)

        if layout is None:
            container = AppletContainer()
            self.splittable.setContentAt(0, container)
        else:
            self.splittable.fromString(str(layout))

        self.setCentralWidget(self.splittable)

        QtGui.QApplication.instance().focusChanged.connect(self._on_focus_changed)

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

    def _actions(self, obj):
        actions = None
        if hasattr(obj, 'toolbar_actions'):
            if isinstance(obj.toolbar_actions, list):
                actions = obj.toolbar_actions
            else:
                actions = obj.toolbar_actions()

        if actions is None:
            return []
        else:
            return actions

    def _on_focus_changed(self, old, new):
        if new is None:
            self.clear_toolbar()
            return

        # Generally focus is on "leaf" widget on widget hierarchy.
        # We try to browse all tree to get widget defining actions
        # For example, if an editor is defined as MyEditor -> Container -> Editor -> QTextEdit
        # Widget with focus is QTextEdit but widget that define actions is MyEditor
        # Search stops if widget has no more parents or if widget is AppletContainer
        parent = new
        actions = self._actions(parent)
        while parent is not None:
            try:
                parent = parent.parent()
            except TypeError:
                break
            else:
                if isinstance(parent, AppletContainer):
                    break
                actions += self._actions(parent)

        if actions:
            self.fill_toolbar(actions)
        else:
            self.clear_toolbar()

    def fill_toolbar(self, actions):
        menus = plugin_instances('oalab.applet', 'ContextualMenu')
        for menu in menus:
            menu.clear()
            for action in actions:
                menu.addBtnByAction(*action)

    def clear_toolbar(self):
        menus = plugin_instances('oalab.applet', 'ContextualMenu')
        for menu in menus:
            menu.clear()

    def _on_applet_set(self, old, new):
        if new in self._registered_applets:
            return

        self._registered_applets.append(new)
        applet = plugin_instance('oalab.applet', new)

        if applet and hasattr(applet, 'global_menu_actions'):
            actions = applet.global_menu_actions()
            if actions is None:
                return
            for menu_name, submenu_name, action, style in actions:
                if menu_name in self.menu_classic:
                    menu = self.menu_classic[menu_name]
                else:
                    menu = QtGui.QMenu(menu_name)
                if isinstance(action, QtGui.QAction):
                    menu.addAction(action)
                elif isinstance(action, QtGui.QMenu):
                    menu.addMenu(action)
                elif action == '-':
                    menu.addSeparator()

    def layout(self):
        return eval(self.splittable.toString())

from openalea.core.path import path as Path
from openalea.core.service.ipython import interpreter


class TestMainWin(OALabMainWin):
    DEFAULT_LAYOUT = ({}, {0: None}, {0: {'widget': {'position': 0, 'applet': [u'ShellWidget']}}})

    def __init__(self, layout=None, **kwds):
        """
        tests: list of function runnable in shell (name changed to run_<funcname>)
        layout_file
        """
        layout_file = kwds.pop('layout_file', 'layout.oaui')
        default_layout = kwds.pop('default_layout', self.DEFAULT_LAYOUT)

        self.layout_filepath = Path(layout_file).abspath()
        if layout is None:
            if self.layout_filepath.exists():
                with open(self.layout_filepath) as layout_file:
                    layout = eval(layout_file.read())

        if layout is None:
            layout = default_layout

        OALabMainWin.__init__(self, layout=layout)

        self.interp = interpreter()
        self.interp.user_ns['mainwin'] = self
        self.interp.user_ns['debug'] = self.debug

        for f in kwds.pop('tests', []):
            self.interp.user_ns['run_%s' % f.__name__] = f

        self.set_edit_mode()

    def closeEvent(self, event):
        with open(self.layout_filepath, 'w') as layout_file:
            layout_file.write(str(self.layout()))

    def debug(self):
        from openalea.oalab.session.session import Session
        session = Session()
        self.interp.user_ns['session'] = session
        session.debug = True
