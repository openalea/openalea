# -*- coding: utf-8 -*-
# -*- python -*-
#
#       Main Window class
#       VPlantsLab GUI is created here
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = ""

from openalea.core.settings import Settings
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.menu import PanedMenu
from openalea.oalab.shell import get_shell_class
from openalea.oalab.service.applet import get_applets, register_applet
from openalea.core.service.ipython import interpreter

from openalea.core.service.plugin import plugin_class, plugin_instance, debug_plugin


class MainWindow(QtGui.QMainWindow):

    """
    This class is based on QMainWindow and provide widgets common to all openalea labs.
    Some are inherited from QMainWindow:
      - a status bar
      - a menu bar
      - a central widget
    Other are specific to openalea's labs:
      - a PanedMenu menu (MainWindow.menu)
      - an IPython shell widget

    MainWindow is a passive widget that host plugin widgets.
    Nevertheless, it provides some method to ease widget integration
    like adding menu and actions

    MainWindow is composed of three distinct areas (shelves) reachable via areas dict.
    Available keys are
        - inputs
        - outputs
        - shell
    """

    def __init__(self, session, parent=None, args=None):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session
        interp = interpreter()
        interp.locals['mainwindow'] = self

        self.areas = {}
        for area_name in ('inputs', 'outputs', 'shell'):
            self.areas[area_name] = QtGui.QTabWidget()

        self.dockWidget("Inputs", self.areas['inputs'], name="Inputs",
                        position=QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget("Outputs", self.areas['outputs'], name="Outputs",
                        position=QtCore.Qt.RightDockWidgetArea)
        self.dockWidget("Shell", self.areas['shell'], name="Shell, log and history",
                        position=QtCore.Qt.BottomDockWidgetArea)

        self.split = QtGui.QSplitter()
        self.setCentralWidget(self.split)

        menu_names = ('Project', 'Edit', 'Viewer', 'Help')

        # Classic menu
        self.menu_classic = {}
        menubar = QtGui.QMenuBar()

        for menu_name in menu_names:
            self.menu_classic[menu_name] = menubar.addMenu(menu_name)

        self.setMenuBar(menubar)

        # PanedMenu
        self.menu_paned = {}
        self.menu = PanedMenu()

        # Organize order of tabs
        for menu_name in menu_names:
            self.menu_paned[menu_name] = self.menu.addSpecialTab(menu_name)

        dock_menu = self.dockWidget("Menu", self.menu, position=QtCore.Qt.TopDockWidgetArea)
        dock_menu.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        dock_menu.setContentsMargins(0, 0, 0, 0)
        widget = QtGui.QLabel()
        dock_menu.setTitleBarWidget(widget)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        dock_menu.setSizePolicy(size_policy)

        # Shell
        self.shell = get_shell_class()(interp)
        interp.locals['shell'] = self.shell
        self.add_applet(self.shell, 'Shell', area='shell')

        self.applets = self._plugins = {}
        # self.resize(QtGui.qApp.desktop().size())

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

        """
        ### This part is used if you want to set menu and submenus

        # warning: if a submenu and a menu have the same name, it will not work
        # todo: find another way that just "findchildren" to get the menus
        children = menubar.findChildren(QtGui.QMenu)
        for child in children:
            if child.title() == sub_menu_name:
                submenu = child
                break
        if not submenu:
            submenu = menu.addMenu(sub_menu_name)
        submenu.addAction(action)"""

        self.setMenuBar(menubar)

    def add_applet(self, applet, name, area=None):
        if area in self.areas:
            self.areas[area].addTab(applet, name)
        elif area == 'central':
            self.split.addWidget(applet)
        else:
            self.dockWidget(name, applet)

    def add_plugin(self, plugin=None, name=None):
        if name and plugin is None:
            _plugin_class = plugin_class('oalab.applet', name)
            plugin = _plugin_class()

        def plug():
            applet = plugin_instance('oalab.applet', plugin.name)
            plugin.graft(applet=applet, oa_mainwin=self)
            self.session.applet['plugin_%s' % plugin.name] = plugin
            self.session.applet[applet.__class__.__name__] = applet

        # Use plugin manager call to handle debug mode automatically
        debug_plugin('oalab.applet', func=plug)

    def initialize(self):
        for applet in get_applets():
            if hasattr(applet, 'initialize'):
                applet.initialize()
            else:
                pass

    def dockWidget(self, identifier, widget, name=None,
                   allowed_area=None, position=None, alias=None):
        if name is None:
            name = identifier.capitalize()

        if allowed_area is None:
            allowed_area = QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea
        if position is None:
            position = QtCore.Qt.LeftDockWidgetArea

        if alias:
            dock_widget = QtGui.QDockWidget(alias, self)
        else:
            dock_widget = QtGui.QDockWidget(name, self)

        dock_widget.setObjectName("%sPanel" % identifier)
        dock_widget.setAllowedAreas(allowed_area)
        dock_widget.setWidget(widget)

        # Remove title bar
        dock_widget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title_bar = QtGui.QLabel()
        dock_widget.setTitleBarWidget(title_bar)

        self.addDockWidget(position, dock_widget)

        return dock_widget

    def closeEvent(self, event):
        self.writeSettings()
        super(QtGui.QMainWindow, self).closeEvent(event)

    ####################################################################
    # Settings
    ####################################################################
    def writeSettings(self):
        """
        Register current settings (geometry and window state)
        in a setting file
        """
        if self.session.project:
            last_proj = self.session.project.name
            config = Settings()

            config.set("ProjectManager", "Last Project", last_proj)
            config.write()
