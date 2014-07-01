# -*- coding: utf-8 -*-
# -*- python -*-
#
#       Main Window class
#       OALab GUI is created here
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

import types

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import logger
from openalea.core.path import path
from openalea.core.settings import get_openalea_home_dir
from openalea.oalab.config.template import config_file_default, config_file_mini, config_file_3d, config_file_tissue, config_file_plant

class MainWindow(QtGui.QMainWindow):
    """
    Main Window Class
    """
    def __init__(self, session, controller, parent=None, args=None):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session
        self.controller = controller

        self._dockwidgets = {}

        self.changeExtension(extension=self.session.extension)

        # Central Widget
        self.setCentralWidget(self.controller.applet_container)

        self.readSettings()
        self.setSettingsInMenu()
        self.setShowDockInMenu()
        self.setSelectLabInMenu()

        # print self.controller.classical_menu.actions()
        self.setMenuBar(self.controller.classical_menu)

    def changeExtension(self, extension=None):
        """
        Change to a new extension.

        :param extension: can be "mini", "3d", "tissue", "plant"
        """
        self.removeDocksWidgets()

        filename = 'oalab.py'
        conf = path(get_openalea_home_dir()) / filename
        if extension in ["mini", "3d", "tissue", "plant"]:
            filename = ('oalab_' + extension + '.py')
            conf = path(get_openalea_home_dir()) / filename
        if not conf.exists():
            with conf.open('w') as f:
                # TODO : auto generate config file
                # f.write(self._config.generate_config_file())
                if extension == "mini":
                    f.write(config_file_mini)
                elif extension == "3d":
                    f.write(config_file_3d)
                elif extension == "tissue":
                    f.write(config_file_tissue)
                elif extension == "plant":
                    f.write(config_file_plant)
                else:
                    f.write(config_file_default)

        self.session.load_config_file(filename=filename, path=get_openalea_home_dir())
        self.setWidgets(self.controller)


    def closeEvent(self, event):
        self.writeSettings()
        super(QtGui.QMainWindow, self).closeEvent(event)

    ####################################################################
    # ## Settings
    ####################################################################
    def writeSettings(self):
        """
        Register current settings (geometry and window state)
        in a setting file
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("session", self.session.project)

    def readSettings(self):
        """
        Read a setting file and restore
        registered settings (geometry and window state)
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")

        try:
            self.restoreGeometry(settings.value("geometry"))
            # self.restoreState(settings.value("windowState"))
        except:
            # if you launch application for the first time,
            # it will save the default state
            settings.setValue("defaultGeometry", self.saveGeometry())
            # settings.setValue("defaultWindowState", self.saveState())
            logger.warning("Can t restore session")

    def setSettingsInMenu(self):

        class FakeWidget(object):
            def __init__(self, parent):
                """
                Use it to add features like setting widgets layout
                """
                super(FakeWidget, self).__init__()
                self.mainwindow = parent
            def actions(self):
                actionDefault = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_blue.png"), "Load Default", self.mainwindow)
                actionRestorePref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_green.png"), "Load Prefered", self.mainwindow)
                actionSetPref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_red.png"), "Save Prefered", self.mainwindow)

                QtCore.QObject.connect(actionDefault, QtCore.SIGNAL('triggered(bool)'), self.mainwindow.defaultSettings)
                QtCore.QObject.connect(actionRestorePref, QtCore.SIGNAL('triggered(bool)'), self.mainwindow.preferedSettings)
                QtCore.QObject.connect(actionSetPref, QtCore.SIGNAL('triggered(bool)'), self.mainwindow.registerPreferedSettings)

                _actions = [["Help", "Window Layout", actionDefault, 1],
                            ["Help", "Window Layout", actionRestorePref, 1],
                            ["Help", "Window Layout", actionSetPref, 1]]
                return _actions

        settings = FakeWidget(parent=self)
        self.controller.connect_actions(settings)

    def setShowDockInMenu(self):
        """
        Use it to add show/hide dockwidget in menu
        """
        children = self.findChildren(QtGui.QDockWidget)

        for child in children:
            name = child.windowTitle()
            if name.lower() == "menu":
                continue
            btn = QtGui.QCheckBox(name, self)
            btn.setChecked(child.isVisibleTo(self))

            btn.toggled.connect(child.setVisible)
            # child.visibilityChanged.connect(btn.setChecked)

            child._actions = [["View", "Show", btn, "smallwidget"], ]
            def actions(self):
                return self._actions

            child.actions = types.MethodType(actions, child)
            self.controller.connect_actions(child)

    def setSelectLabInMenu(self):
        class FakeWidget(object):
            def __init__(self, parent):
                """
                Use it to add features like setting widgets layout

                Actually not used
                """
                super(FakeWidget, self).__init__()
                self.mainwindow = parent
            def actions(self):
                minilab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"), "MiniLab", self.mainwindow)
                lab3d = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"), "3DLab", self.mainwindow)
                plantlab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"), "PlantLab", self.mainwindow)
                tissuelab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"), "TissueLab", self.mainwindow)

                QtCore.QObject.connect(minilab, QtCore.SIGNAL('triggered(bool)'), self.mainwindow._mini)
                QtCore.QObject.connect(lab3d, QtCore.SIGNAL('triggered(bool)'), self.mainwindow._lab3d)
                QtCore.QObject.connect(plantlab, QtCore.SIGNAL('triggered(bool)'), self.mainwindow._plant)
                QtCore.QObject.connect(tissuelab, QtCore.SIGNAL('triggered(bool)'), self.mainwindow._tissue)

                _actions = [["Extension", "Select an Extension", minilab, 0],
                            ["Extension", "Select an Extension", lab3d, 0],
                            ["Extension", "Select an Extension", plantlab, 0],
                            ["Extension", "Select an Extension", tissuelab, 0]]
                return None

        settings = FakeWidget(parent=self)
        self.controller.connect_actions(settings)

    def defaultSettings(self):
        """
        Restore default settings (geometry and window state)
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")
        self.restoreGeometry(settings.value("defaultGeometry"))
        self.restoreState(settings.value("defaultWindowState"))

    def preferedSettings(self):
        """
        Get prefered settings and restore them
        """
        try:
            settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")
            self.restoreGeometry(settings.value("preferedGeometry"))
            self.restoreState(settings.value("preferedWindowState"))
        except:
            logger.warning("Can t restore prefered session")

    def registerPreferedSettings(self):
        """
        Register current settings as preferd settings
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")
        settings.setValue("preferedGeometry", self.saveGeometry())
        settings.setValue("preferedWindowState", self.saveState())

    ####################################################################
    # ## Widgets
    ####################################################################

    def _dockWidget(self, identifier, widget, name=None, allowed_area=None, position=None, alias=None):
        if name is None :
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
        self.addDockWidget(position, dock_widget)
        self._dockwidgets[identifier] = dock_widget
        display = self.session.config.get('MainWindowConfig').get(identifier.lower(), False)
        dock_widget.setVisible(display)

        return dock_widget

    def setWidgets(self, controller):
        # Menu
        dock_menu = self._dockWidget("Menu", controller.menu,
                                     allowed_area=QtCore.Qt.TopDockWidgetArea,
                                     position=QtCore.Qt.TopDockWidgetArea)
        dock_menu.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        # Docks
        self._dockWidget("Viewer3D", controller.applets["Viewer3D"], name="Viewer", position=QtCore.Qt.RightDockWidgetArea)
        # self._dockWidget("Store", controller.applets["Store"], name="OpenAlea Store", position=QtCore.Qt.RightDockWidgetArea)

        self._dockWidget("HelpWidget", controller.applets["HelpWidget"], position=QtCore.Qt.RightDockWidgetArea, alias="Help")
        self._dockWidget("Project", controller.applets["Project"], position=QtCore.Qt.RightDockWidgetArea)
        # self._dockWidget("ProjectManager", controller.applets["ProjectManager"],position=QtCore.Qt.RightDockWidgetArea) # Project Manager

        self._dockWidget("Shell", controller.shell, name="IPython Shell", position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Logger", controller.applets["Logger"], position=QtCore.Qt.BottomDockWidgetArea)

        self._dockWidget("Packages", controller.applets["Packages"], position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("PackageCategories", controller.applets["PackageCategories"], name="Package Categories", position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("PackageSearch", controller.applets["PackageSearch"], name="Package Search", position=QtCore.Qt.BottomDockWidgetArea)

        if controller.applets.has_key("ControlPanel"):
            self._dockWidget("ControlPanel", controller.applets["ControlPanel"], name="Control Panel", position=QtCore.Qt.BottomDockWidgetArea)
            controller.applets['ControlPanel'].geometry_editor.setStatusBar(self.statusBar())

        # self._dockwidgets['Store'].hide()

        # Status bar
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        controller.statusBar = status
        self.statusBar().showMessage("OpenAleaLab is ready!", 10000)

        # Tabify docks
        self.tabifyDockWidget(self._dockwidgets['Logger'], self._dockwidgets['Shell'])
        self.tabifyDockWidget(self._dockwidgets['PackageSearch'], self._dockwidgets['PackageCategories'])
        self.tabifyDockWidget(self._dockwidgets['PackageCategories'], self._dockwidgets['Packages'])

        if self._dockwidgets.has_key("Packages") and self._dockwidgets.has_key("ControlPanel"):
            self.tabifyDockWidget(self._dockwidgets['Packages'], self._dockwidgets['ControlPanel'])

        self.tabifyDockWidget(self._dockwidgets['Project'], self._dockwidgets['HelpWidget'])
        # self._dockwidgets['Store'].setTitleBarWidget(QtGui.QWidget())

    def removeDocksWidgets(self):
        children = self.findChildren(QtGui.QDockWidget)

        for child in children:
            self.removeDockWidget(child)

    def changeMenuTab(self, old, new):
        """
        Set tab of 'new' current in the menu.
        This class is designed to be connected to focusChanged signal.

        :param old: old widget. Not used.
        :param new: current widget to check if we have to change menu
        """

        if new and hasattr(new, 'mainMenu') :
            # new=None means application has lost focus, so do not change PanedMenu.
            # (for example, click outside application)

            # Get Tab Name
            name = new.mainMenu()
            # Get Menu
            menu = self._dockwidgets['Menu'].widget()
            menu.showPane(name)


    def _mini(self):
        self.changeExtension("mini")

    def _lab3d(self):
        self.changeExtension("3d")

    def _plant(self):
        self.changeExtension("plant")

    def _tissue(self):
        self.changeExtension("tissue")
