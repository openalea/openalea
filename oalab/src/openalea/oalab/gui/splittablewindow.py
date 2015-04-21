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

import sys
import json
import weakref


from openalea.core.control import Control
from openalea.core.plugin.manager import PluginManager
from openalea.core.service.plugin import (new_plugin_instance, plugin_instances, plugin_class, plugins,
                                          plugin_instance, plugin_instance_exists)

from openalea.oalab.gui.control.qcontainer import QControlContainer
from openalea.oalab.gui.menu import ContextualMenu
from openalea.oalab.gui.splitterui import SplittableUI, BinaryTree
from openalea.oalab.gui.utils import ModalDialog, obj_icon, qicon, Splitter

from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import tabposition_int, tabposition_qt

import openalea.core


def menu_actions(widget):
    actions = []
    if widget is None:
        return actions
    if hasattr(widget, 'menu_actions'):
        actions += widget.menu_actions()
    elif widget.actions():
        actions += widget.actions()
    return actions


def fill_menu(menu, actions):
    for action in actions:
        if isinstance(action, QtGui.QAction):
            menu.addAction(action)
        elif isinstance(action, (list, tuple)):
            menu.addAction(action[2])
        elif isinstance(action, QtGui.QMenu):
            menu.addMenu(action)
        elif action == '-':
            menu.addSeparator()
        else:
            continue


class AppletSelector(QtGui.QWidget):

    """
    Combobox listing all applets available.
    Signals:
      - appletChanged(name): sent when an applet is selected
    """

    appletChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout = QtGui.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._cb_applets = QtGui.QComboBox()
        self._applet_alias = []  # list of alias sorted by name
        self._applet_plugins = {}  # alias -> plugin class

        self._cb_applets.addItem('Select applet')
        for plugin_class in plugins('oalab.applet'):
            self._applet_alias.append(plugin_class.alias)
            self._applet_plugins[plugin_class.alias] = plugin_class
        self._applet_alias.sort()

        for alias in self._applet_alias:
            plugin_class = self._applet_plugins[alias]
            self._cb_applets.addItem(obj_icon(plugin_class), alias)

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
            plugin_class = self._applet_plugins[self._applet_alias[idx - 1]]
            return plugin_class.name
        else:
            return None

    def currentAppletName(self):
        return self.applet(self._cb_applets.currentIndex())

    def setCurrentApplet(self, name):
        self._cb_applets.setCurrentIndex(0)
        for i, alias in enumerate(self._applet_alias):
            plugin_class = self._applet_plugins[alias]
            if plugin_class.name == name:
                self._cb_applets.setCurrentIndex(i + 1)
                break


class LayoutSelector(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        p = QtGui.QSizePolicy

        self._cb_layout = QtGui.QComboBox()
        self._cb_layout.setSizePolicy(p(p.MinimumExpanding, p.Maximum))
        self._stack = QtGui.QStackedWidget()

        self._cb_layout.activated.connect(self._stack.setCurrentIndex)

        self._layout.addWidget(self._cb_layout)
        self._layout.addWidget(self._stack)

        self._cb_layout.hide()

    def add_widget(self, widget, title=None):
        if title is None:
            title = 'Layout %d' % (self._cb_layout.count() + 1)
        self._cb_layout.addItem(title)
        self._stack.addWidget(widget)
        if self._cb_layout.count() > 1:
            self._cb_layout.show()

    def set_widget(self, idx):
        self._cb_layout.setCurrentIndex(idx)

    def widget(self):
        return self._stack.currentWidget()


class AppletFrame(QtGui.QWidget):

    """
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self._show_toolbar = Control('toolbar', interface='IBool', value=False, alias='Show Toolbar')
        self._show_title = Control('title', interface='IBool', value=False, alias='Show Applet Title')

        self._props = QControlContainer()
        self._props.controlValueChanged.connect(self._on_prop_changed)
        self._props.add_control(self._show_toolbar)
        self._props.add_control(self._show_title)

        self._edit_mode = False

        self._applet = None

        self._layout = QtGui.QVBoxLayout(self)

        self._l_title = QtGui.QLabel('No applet selected')
        self._l_title.hide()
        self._menu = ContextualMenu()

        p = QtGui.QSizePolicy
        self._l_title.setSizePolicy(p(p.MinimumExpanding, p.Maximum))
        self._l_title.setAlignment(QtCore.Qt.AlignVCenter)

        self._layout.setAlignment(self._l_title, QtCore.Qt.AlignVCenter)

        self._layout.addWidget(self._l_title)
        self._layout.addWidget(self._menu)

        self._create_actions()
        self.fine_tune()

    def fine_tune(self):
        if sys.platform == 'darwin':
            self._layout.setContentsMargins(0, 5, 0, 0)
            self.setContentsMargins(0, 5, 0, 0)
        else:
            # warning: drawin case above segfault on linux platform with Qt 4.8.6
            # but works with size==2 instead of 5
            # This is maybe due to default handle/splitters size, see splitterui module
            self._layout.setContentsMargins(0, 0, 0, 0)
            self.setContentsMargins(0, 0, 0, 0)

    def _on_prop_changed(self, prop, value):
        if prop is self._show_toolbar:
            self.show_toolbar(value)
        elif prop is self._show_title:
            self.show_title(value)

    def _create_actions(self):
        self._props.create_actions(self)

    def menu_actions(self):
        if self._applet:
            applet = self._applet()
        else:
            applet = None
        if self._edit_mode:
            actions = self._props.actions()
        else:
            actions = menu_actions(applet)
        return actions

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        fill_menu(menu, self.menu_actions())
        menu.exec_(event.globalPos())

    def set_edit_mode(self, edit=True):
        self._edit_mode = edit

    def set_applet(self, applet):
        self._applet = weakref.ref(applet)
        self._layout.insertWidget(1, applet)
        _plugin_class = plugin_class('oalab.applet', applet.name)
        self._l_title.setText(_plugin_class.alias)
        p = QtGui.QSizePolicy
        applet.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

    def remove_applet(self, applet):
        self._layout.removeWidget(applet)

    def show_title(self, show=True):
        self._show_title.value = show
        self._l_title.setVisible(show)

    def show_toolbar(self, show=True):
        self._show_toolbar.value = show
        if show:
            self.fill_toolbar()
        else:
            self.clear_toolbar()

    def fill_toolbar(self):

        if self._show_toolbar.value is False:
            return

        if self._applet is None:
            return

        applet = self._applet()
        if applet is None:
            return

        # Fill toolbar
        self._menu.show()
        self.clear_toolbar()
        try:
            actions = applet.toolbar_actions()
        except AttributeError:
            pass
        else:
            self._menu.set_actions('n', actions)

    def clear_toolbar(self):
        if self._show_toolbar.value:
            self._menu.clear()
        else:
            self._menu.hide()

    def properties(self):
        return self._props.namespace()

    def set_properties(self, properties):
        self._props.update(properties)


class AppletTabWidget(QtGui.QTabWidget):
    appletSet = QtCore.Signal(object, object)

    def __init__(self):
        QtGui.QTabWidget.__init__(self)

        # Tab management
        self.setMovable(True)
        self.tabCloseRequested.connect(self.remove_tab)
        self.tabBar().tabMoved.connect(self._on_tab_moved)

        # Internal dicts
        # dict: idx -> name -> applet.
        # Ex: self._applets[0]['Help'] -> <HelpWidget instance at 0x7fea19a07d88>
        self._applets = {}

        # dict: idx -> name of current applet
        self._name = {}

        # Set in edit mode by default
        self.set_edit_mode()
        self.fine_tune()

    def closeEvent(self, event):
        for idx in self._applets:
            name = self._name[idx]
            applet = self._applets[idx][name]
            if applet.close() is False:
                event.ignore()
                return
        event.accept()

    def fine_tune(self):
        # Display options
        self.setDocumentMode(True)

    def tabInserted(self, index):
        self.tabBar().setVisible(self.count() > 1)

    def tabRemoved(self, index):
        self.tabBar().setVisible(self.count() > 1)

    def setTabPosition(self, position):
        rvalue = QtGui.QTabWidget.setTabPosition(self, tabposition_qt(position))
        for idx in range(self.count()):
            self._redraw_tab(idx)
        return rvalue

    def _on_tab_moved(self, old, new):
        self._name[old], self._name[new] = self._name[new], self._name[old]
        self._applets[old], self._applets[new] = self._applets[new], self._applets[old]
        self._redraw_tab(old)
        self._redraw_tab(new)

    def set_edit_mode(self, mode=True):
        self._edit_mode = mode
        applet_frame = self.currentWidget()
        if applet_frame:
            applet_frame.set_edit_mode(mode)
        self.setTabsClosable(mode)

    def menu_actions(self):
        return menu_actions(self.currentWidget())

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        fill_menu(menu, self.menu_actions())
        menu.exec_(event.globalPos())

    def new_tab(self):
        widget = AppletFrame()
        widget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.addTab(widget, '')
        self.setCurrentWidget(widget)

    def remove_tab(self, idx):
        """
         - Destroy all applets in current tabs (current applet and previous hidden applets)
         - Then, remove tab.
        """
        if idx in self._applets:
            tab = self.currentWidget()
            for applet in self._applets[idx].values():
                tab.remove_applet(applet)
                applet.close()
                del applet
            del self._applets[idx]
            del self._name[idx]
        self.removeTab(idx)

    def set_applet(self, name, properties=None):
        """
        Show applet "name" in current tab.
        """
        # clear view (hide all widgets in current tab)
        idx = self.currentIndex()
        old = self._name.get(idx, None)
        for applet in self._applets.get(idx, {}).values():
            applet.hide()

        if not name:
            return

        # If applet has been instantiated before, just show it
        # Else, instantiate a new one, place it in layout and show it
        if name in self._applets.get(idx, {}):
            applet = self._applets[idx][name]
            applet.show()
        else:
            # If applet has never been instantiated in the whole application,
            # we instantiate it as the "main" instance (ie reachable thanks to plugin_instance)
            # else, just create a new one.
            if plugin_instance_exists('oalab.applet', name):
                applet = new_plugin_instance('oalab.applet', name)
            else:
                applet = plugin_instance('oalab.applet', name)

            if applet is None:
                return

            applet.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            applet.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            if hasattr(applet, 'initialize'):
                applet.initialize()
            applet.name = name
            if properties:
                try:
                    applet.set_properties(properties)
                except AttributeError:
                    pass

            tab = self.currentWidget()
            tab.set_applet(applet)
            self._applets.setdefault(idx, {})[name] = applet

        self._name[idx] = name
        self._redraw_tab(idx)

        self.appletSet.emit(old, name)

    def _redraw_tab(self, idx):
        """
        """
        if idx not in self._name:
            return

        name = self._name[idx]
        _plugin_class = plugin_class('oalab.applet', name)
        applet = self._applets[idx][name]

        # self.setTabText(idx, _plugin_class.alias)
        if tabposition_int(self.tabPosition()) == 3:
            rotation = -90
        elif tabposition_int(self.tabPosition()) == 2:
            rotation = 90
        else:
            rotation = 0

        self.setTabIcon(idx, obj_icon(_plugin_class, applet=applet, rotation=rotation))
        self.setTabToolTip(idx, _plugin_class.alias)
        self.widget(idx).set_edit_mode(self._edit_mode)

    def currentAppletName(self):
        try:
            return self._name[self.currentIndex()]
        except KeyError:
            return None

    def currentApplet(self):
        try:
            name = self.currentAppletName()
            return self._applets[self.currentIndex()][name]
        except KeyError:
            return None

    def properties(self):
        position = tabposition_int(self.tabPosition())
        return dict(position=position)

    def set_properties(self, properties):
        get = properties.get
        self.setTabPosition(get('position', 0))

    def _repr_json_(self):
        applets = []
        for idx in range(self.count()):
            if idx in self._name:
                name = self._name[idx]
                applet_frame = self.widget(idx)
                properties = applet_frame.properties()
                try:
                    properties.update(self._applets[idx][name].properties())
                except AttributeError:
                    pass
                applets.append(dict(name=name, properties=properties, interface='IPluginInstance', ep='oalab.applet'))
        layout = dict(applets=applets, properties=self.properties(), interface='IAppletTabWidget')
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

        self._e_title = QtGui.QLabel('')
        self._e_title.hide()

        self._tabwidget = AppletTabWidget()
        self._tabwidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self._tabwidget.appletSet.connect(self.appletSet.emit)
        self._tabwidget.currentChanged.connect(self._on_tab_changed)
        self.appletSet.connect(self._on_applet_changed)

        self._applet_selector = AppletSelector()
        self._applet_selector.appletChanged.connect(self._tabwidget.set_applet)

        self._layout.addWidget(self._e_title)
        self._layout.addWidget(self._tabwidget)
        self._layout.addWidget(self._applet_selector)

        self._tabwidget.new_tab()

        applet_name = self._applet_selector.currentAppletName()
        if applet_name:
            self._tabwidget.set_applet(applet_name)

        self._create_menus()
        self._create_actions()
        self._fill_menus()

        self.set_edit_mode()
        self.fine_tune()

    def fine_tune(self):
        self.setContentsMargins(0, 5, 0, 0)

    def _create_actions(self):
        self.action_title = QtGui.QAction("Set Title", self)
        self.action_title.triggered.connect(self._on_set_title_triggered)

        self.action_unlock = QtGui.QAction(qicon('oxygen_object-unlocked.png'), "Edit layout", self.menu_edit_off)
        self.action_unlock.triggered.connect(self.unlock_layout)

        self.action_lock = QtGui.QAction(qicon('oxygen_object-locked.png'), "Lock layout", self.menu_edit_on)
        self.action_lock.triggered.connect(self.lock_layout)

        self.action_add_tab = QtGui.QAction(qicon('Crystal_Clear_action_edit_add.png'), "Add tab", self.menu_edit_on)
        self.action_add_tab.triggered.connect(self._tabwidget.new_tab)

        self.action_remove_tab = QtGui.QAction(
            qicon('Crystal_Clear_action_edit_remove.png'), "Remove tab", self.menu_edit_on)
        self.action_remove_tab.triggered.connect(self._tabwidget.remove_tab)

        self.action_push_to_shell = QtGui.QAction("DEBUG push applet to shell", self.menu_edit_on)
        self.action_push_to_shell.triggered.connect(self._push_applet_to_shell)

    def _push_applet_to_shell(self):
        interp = interpreter()
        interp.user_ns['debug_dict'] = dict(
            container=self,
            c_applets=self._applets,
            c_tabwidget=self._tabwidget,
            frame=self._tabwidget.currentWidget(),
            applet_dict=self._tabwidget._applets,
            applet=self._tabwidget._applets[self._tabwidget.currentIndex()]
        )
        for k, v in interp.user_ns['debug_dict'].items():
            interp.user_ns['debug_%s' % k] = v

    def _create_menus(self):
        # Menu if edit mode is OFF
        self.menu_edit_off = QtGui.QMenu(self)
        self.menu_edit_on = QtGui.QMenu(self)

    def _fill_menus(self):
        self.menu_edit_off.addAction(self.action_unlock)
        self.menu_edit_off.addSeparator()

        # Menu if edit mode is ON

        self.menu_edit_on.addAction(self.action_lock)
        self.menu_edit_on.addSeparator()
        self.menu_edit_on.addAction(self.action_add_tab)
        self.menu_edit_on.addAction(self.action_remove_tab)
        self.menu_edit_on.addSeparator()
        self.menu_edit_on.addAction(self.action_title)
        self.menu_edit_on.addSeparator()
        # self.menu_edit_on.addAction(self.action_push_to_shell)

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

    def menu_actions(self):
        if self._edit_mode is True:
            actions = self.menu_edit_on.actions()
            actions += self._tabwidget.menu_actions()
        else:
            actions = self.menu_edit_off.actions()
            actions += self._tabwidget.menu_actions()
        return actions

    def emit_applet_set(self):
        for applet in self._applets:
            self.appletSet.emit(None, applet)

    def closeEvent(self, event):
        if self._tabwidget.close():
            event.accept()
        else:
            event.ignore()

    def add_applets(self, applets, **kwds):
        """
        applets: list of dict defining applets.
        Each dict must define at least a key "name".
        Ex: applets = [{'name':'MyWidget'}]
        """
        names = []
        for i, applet in enumerate(applets):
            name = applet['name']
            names.append(name)
            properties = applet.get('properties', {})
            if i:
                self._tabwidget.new_tab()
            self._tabwidget.set_applet(name, properties=properties)
            self._tabwidget.currentWidget().set_properties(properties)
        self._tabwidget.setCurrentIndex(0)
        self._applets = names

    def _on_tab_position_changed(self):
        self._tabwidget.setTabPosition(self._position_actions[self.sender()])

    def _on_tab_changed(self, idx):
        applet_name = self._tabwidget.currentAppletName()
        if applet_name:
            applet = self._tabwidget.currentApplet()
            self._applet_selector.setCurrentApplet(applet_name)

    def _on_applet_changed(self, old, new):
        pass

    def lock_layout(self):
        self.set_edit_mode(False)

    def unlock_layout(self):
        self.set_edit_mode(True)

    def set_edit_mode(self, mode=True):
        self._applet_selector.setVisible(mode)
        self._edit_mode = mode
        self._tabwidget.set_edit_mode(mode)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        fill_menu(menu, self.menu_actions())
        menu.exec_(event.globalPos())

    def properties(self):
        properties = {}
        properties.update(self._tabwidget.properties())
        title = unicode(self._e_title.text()).strip()
        if title:
            properties['title'] = title
        return properties

    def set_properties(self, properties):
        self._tabwidget.set_properties(properties)
        self.set_title(properties.get('title', None))

    def _on_set_title_triggered(self):
        from openalea.oalab.service.qt_control import qt_dialog
        value = qt_dialog(name='Title', interface='IStr', value=self._e_title.text())
        if value is not None:
            self.set_title(value)

    def set_title(self, title):
        if title:
            self._e_title.show()
            self._e_title.setText(title)
        else:
            self._e_title.hide()
            self._e_title.setText('')

    def _repr_json_(self):
        json = self._tabwidget._repr_json_()
        json.setdefault('properties', {}).update(self.properties())
        json['interface'] = 'IAppletContainer'
        return json


class OABinaryTree(BinaryTree):

    def toString(self, props=[]):
        raise NotImplementedError

    def _repr_json_(self, props=[]):
        filteredProps = {}
        for vid, di in self._properties.iteritems():
            filteredProps[vid] = {}
            for k, v in di.iteritems():
                if k in props:
                    if hasattr(v, '_repr_json_'):
                        filteredProps[vid][k] = v._repr_json_()
                    else:
                        filteredProps[vid][k] = v
        return dict(children=self._toChildren,
                    parents=self._toParents,
                    properties=filteredProps)


class InitContainerVisitor(object):

    """Visitor that searches which leaf id has pos in geometry"""

    def __init__(self, graph, wid):
        self.g = graph
        self.wid = wid

    def _to_qwidget(self, widget):
        if isinstance(widget, dict):
            properties = widget.get('properties', {})
            applets = widget.get('applets', [])
            if applets is None:
                return widget
            container = AppletContainer()
            container.add_applets(applets)
            container.set_properties(properties)
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

    def emit_applet_set(self):
        for container in self._containers:
            container.emit_applet_set()

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
    def FromJSON(cls, layout, parent=None):
        g = OABinaryTree.fromJSON(layout)

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

    def fromJSON(self, layout, parent=None):
        g = OABinaryTree.fromJSON(layout)

        w0 = self._uninstall_child(0)
        if w0:
            w0.setParent(None)
            w0.close()

        self._g = g
        visitor = InitContainerVisitor(g, self)
        g.visit_i_breadth_first(visitor)
        self._geomCache[0] = self.contentsRect()
        self.computeGeoms(0)

    def toString(self):
        raise NotImplementedError

    def _repr_json_(self):
        dic = self._g._repr_json_(self.reprProps)
        dic['interface'] = 'ISplittableUi'
        return dic

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

    def closeEvent(self, event):
        close = True
        for container in self._containers:
            close = container.close()
            if close is False:
                event.ignore()
                return
        event.accept()


class OALabMainWin(QtGui.QMainWindow):
    appletSet = QtCore.Signal(object, object)
    DEFAULT_MENU_NAMES = ('File', 'Edit', 'View', 'Help')

    DEFAULT_LAYOUT = dict(
        name='default',
        alias='Default Layout',
        children={},
        parents={0: None},
        properties={
            0: {
                'widget': {
                    'properties': {'position': 0},
                    'applets': [{'name': 'ShellWidget'}]
                }
            }}
    )
    DEFAULT_LAYOUT_PATH = 'layout.oaui'
    LAB = None

    def __init__(self, layout=None, **kwds):
        QtGui.QMainWindow.__init__(self)
        self._lab = kwds.get('lab', None)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.DEFAULT_MENU_NAMES = list(self.DEFAULT_MENU_NAMES)
        if 'Edit' not in self.DEFAULT_MENU_NAMES:
            self.DEFAULT_MENU_NAMES.insert(0, 'Edit')
        if 'File' not in self.DEFAULT_MENU_NAMES:
            self.DEFAULT_MENU_NAMES.insert(0, 'File')
        if 'Help' not in self.DEFAULT_MENU_NAMES:
            self.DEFAULT_MENU_NAMES.append('Help')

        # Classic menu
        self._registered_applets = []

        self._create_menus()
        self._create_actions()
        self._pre_fill_menus()

        self._splittable_list = []

        self.layout_selector = LayoutSelector(parent=self)
        layout = self._load_layout(layout, **kwds)
        if isinstance(layout, (list, tuple)):
            layouts = layout
        else:
            layouts = [layout]

        for layout in layouts:
            title = layout.get('title', None)
            if 'children' not in layout:
                layout = None
            splittable = OALabSplittableUi(parent=self)
            splittable.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            splittable.appletSet.connect(self.appletSet.emit)
            self.appletSet.connect(self._on_applet_set)
            if layout is None:
                container = AppletContainer()
                splittable.setContentAt(0, container)
            else:
                splittable.fromJSON(layout)
            self._splittable_list.append(splittable)
            self.layout_selector.add_widget(splittable, title=title)

        self.setCentralWidget(self.layout_selector)
        self._post_fill_menus()
        self.set_edit_mode(False)

        QtGui.QApplication.instance().focusChanged.connect(self._on_focus_changed)

    def emit_applet_set(self):
        self.splittable.emit_applet_set()

    @property
    def splittable(self):
        return self.layout_selector.widget()

    def _create_menus(self):
        self.menu_classic = {}
        menubar = QtGui.QMenuBar()
        self.setMenuBar(menubar)
        for menu_name in self.DEFAULT_MENU_NAMES:
            self.menu_classic[menu_name] = menubar.addMenu(menu_name)

    def _create_actions(self):
        self.action_edit = QtGui.QAction("Edit Layout", self.menu_classic['Edit'])
        self.action_edit.setCheckable(True)
        self.action_edit.toggled.connect(self.set_edit_mode)
        self.action_edit.setChecked(False)

        icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_TitleBarCloseButton)
        self.action_quit = QtGui.QAction(icon, "Quit application", self.menu_classic['File'])
        self.action_quit.triggered.connect(self.close)
        self.action_quit.setChecked(False)

    def _pre_fill_menus(self):
        self.menu_classic['Edit'].addAction(self.action_edit)

    def _post_fill_menus(self):
        self.menu_classic['File'].addSeparator()
        self.menu_classic['File'].addAction(self.action_quit)

    def _load_layout(self, layout=None, **kwds):
        layout_file = kwds.pop('layout_file', self.DEFAULT_LAYOUT_PATH)
        default_layout = kwds.pop('default_layout', self.DEFAULT_LAYOUT)

        self.layout_filepath = Path(layout_file).abspath()
        if layout is None:
            if self.layout_filepath.exists():
                with open(self.layout_filepath) as layout_file:
                    content = layout_file.read()
                    try:
                        layout = json.loads(content)
                    except ValueError:
                        l = eval(content)
                        layout = dict(children=l[0], parents=l[1], properties=l[2])

        if layout is None:
            layout = default_layout
        return layout

    def _save_layout(self):
        with open(self.layout_filepath, 'w') as layout_file:
            json.dump(self.layout(), layout_file, sort_keys=True, indent=2)

    def closeEvent(self, event):
        close = True

        # If a lab is used, check if it can be close
        if hasattr(self._lab, 'readytoclose'):
            close = self._lab.readytoclose()

        # If lab is not ready, stop closing
        if close is False:
            event.ignore()
            return

        # If lab is ready to close, or no lab is used, close widget
        if self.splittable.close():
            if hasattr(self._lab, 'finalize'):
                self._lab.finalize()
            self._save_layout()
            if hasattr(self._lab, 'stop'):
                self._lab.stop()
            event.accept()
        else:
            event.ignore()

    def set_edit_mode(self, mode=True):
        for widget in self.splittable.getAllContents():
            if hasattr(widget, 'set_edit_mode'):
                widget.set_edit_mode(mode)
        if mode is True and self.LAB:
            print self.LAB.connections
        self.splittable.set_edit_mode(mode)

    def initialize(self):
        self.pm = PluginManager()
        for instance in plugin_instances('oalab.applet'):
            if hasattr(instance, 'initialize'):
                instance.initialize()

    def _widget_actions(self, obj):
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

    def _widget_name(self, obj):
        if hasattr(obj, 'name'):
            return obj.name

    def _on_focus_changed(self, old, new):
        self.clear_toolbar()
        if old is new:
            return

        # Generally focus is on "leaf" widget on widget hierarchy.
        # We try to browse all tree to get widget defining actions
        # For example, if an editor is defined as MyEditor -> Container -> Editor -> QTextEdit
        # Widget with focus is QTextEdit but widget that define actions is MyEditor
        # Search stops if widget has no more parents or if widget is AppletContainer
        parent = new
        actions = self._widget_actions(parent)
        name = self._widget_name(parent)
        while parent is not None:
            try:
                parent = parent.parent()
            except TypeError:
                break
            else:
                if isinstance(parent, AppletContainer):
                    break
                name = name or self._widget_name(parent)
                actions += self._widget_actions(parent)

        if actions:
            self.fill_toolbar(name, actions)

        # toolbar creation/destruction set focus to toolbar so we reset it to widget
        if isinstance(new, QtGui.QWidget):
            new.setFocus(QtCore.Qt.OtherFocusReason)

    def fill_toolbar(self, name, actions):
        menus = plugin_instances('oalab.applet', 'ContextualMenu')
        for menu in menus:
            menu.set_actions(name, actions)

    def clear_toolbar(self):
        menus = plugin_instances('oalab.applet', 'ContextualMenu')
        for menu in menus:
            menu.clear()

    def _merge_menus(self, menus):
        parent = self
        default_menus = self.menu_classic
        menubar = self.menuBar()

        for _menu in menus:
            menu_name = _menu.title()
            if menu_name in default_menus:
                menu = default_menus[menu_name]
            else:
                menu = QtGui.QMenu(menu_name, parent)
                default_menus[menu_name] = menu
                menubar.addMenu(menu)

        for _menu in menus:
            menu_name = _menu.title()
            menu = default_menus[menu_name]
            for action in _menu.actions():
                if isinstance(action, QtGui.QAction):
                    menu.addAction(action)
                elif isinstance(action, QtGui.QMenu):
                    menu.addMenu(action)
                elif action == '-':
                    menu.addSeparator()

    def _on_applet_set(self, old, new):
        if new in self._registered_applets:
            return

        self._registered_applets.append(new)
        applet = plugin_instance('oalab.applet', new)

        # Add global menus
        if applet and hasattr(applet, 'menus'):
            menus = applet.menus()
            if menus is None:
                return
            self._merge_menus(menus)

        # Add global toolbars
        if applet and hasattr(applet, 'toolbars'):
            toolbars = applet.toolbars()
            if toolbars is None:
                return
            for toolbar in toolbars:
                self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)

    def layout(self):
        return self.splittable._repr_json_()


class SplitterApplet(Splitter):

    ORIENTATION = QtCore.Qt.Vertical

    def __init__(self):
        Splitter.__init__(self)
        self._applets = {}

        self._action_add_applet = QtGui.QAction('Add applet', self)
        self._action_add_applet.triggered.connect(self._on_add_applet_triggered)

    def menu_actions(self):
        actions = Splitter.menu_actions(self)
        actions.append(self._action_add_applet)
        return actions

    def _on_add_applet_triggered(self):
        widget = AppletSelector()
        dialog = ModalDialog(widget)
        if dialog.exec_() == dialog.Accepted:
            self.add_applet(widget.currentAppletName())

    def clear(self):
        for applet in self._applets.itervalues():
            applet.close()
        self._applets.clear()

    def add_applet(self, name):
        applet = new_plugin_instance('oalab.applet', name)
        applet.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._applets[name] = applet
        self.addWidget(applet)

    def set_properties(self, properties):
        applets = properties.get('applets', [])
        for name in applets:
            self.add_applet(name)
        # applet have to be loaded before to restore state
        Splitter.set_properties(self, properties)

    def properties(self):
        dic = Splitter.properties(self)
        dic['applets'] = self._applets.keys()
        return dic

from openalea.core.path import path as Path
from openalea.core.service.ipython import interpreter


class TestMainWin(OALabMainWin):

    def __init__(self, layout=None, **kwds):
        """
        tests: list of function runnable in shell (name changed to run_<funcname>)
        layout_file
        """
        OALabMainWin.__init__(self, layout=layout, **kwds)

        self.interp = interpreter()
        self.interp.user_ns['mainwin'] = self
        self.interp.user_ns['splittable'] = self.splittable
        self.interp.user_ns['debug'] = self.debug
        self.interp.user_ns['QtCore'] = QtCore
        self.interp.user_ns['QtGui'] = QtGui

        from openalea.core.service.plugin import plugin_instance, plugin_instances

        def applet(name):
            return plugin_instance('oalab.applet', name)

        def applets(name):
            return plugin_instances('oalab.applet', name)

        self.interp.user_ns['applet'] = applet
        self.interp.user_ns['applets'] = applets

        for f in kwds.pop('tests', []):
            self.interp.user_ns['run_%s' % f.__name__] = f

    def debug(self):
        from openalea.oalab.session.session import Session
        session = Session()
        self.interp.user_ns['session'] = session
        session.debug = True
