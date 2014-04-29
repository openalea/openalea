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

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.shell.shell import get_shell_class

class MainWindow(QtGui.QMainWindow):
    """
    MainWindow provides:
      - a PanedMenu menu (MainWindow.menu)
      - a shell widget

    """
    def __init__(self, session, parent=None, args=None):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session

        self.areas = {}
        for area in ('inputs', 'outputs', 'shell'):
            self.areas[area] = QtGui.QTabWidget()

        self.dockWidget("Inputs", self.areas['inputs'], name="Inputs",
                         position=QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget("Outputs", self.areas['outputs'], name="Outputs",
                         position=QtCore.Qt.RightDockWidgetArea)
        self.dockWidget("Shell", self.areas['shell'], name="Shell, log and history",
                         position=QtCore.Qt.BottomDockWidgetArea)

        self.split = QtGui.QSplitter()
        self.setCentralWidget(self.split)

        # PanedMenu
        self.menu = PanedMenu()
        dock_menu = self.dockWidget("Menu", self.menu, position=QtCore.Qt.TopDockWidgetArea)
        dock_menu.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        dock_menu.setContentsMargins(0, 0, 0, 0)
        widget = QtGui.QLabel('Menu')
        dock_menu.setTitleBarWidget(widget)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        dock_menu.setSizePolicy(size_policy)

        # Shell
        self.shell = get_shell_class()(self.session.interpreter)
        self.add_applet(self.shell, 'Shell', area='shell')

        self.applets = self._plugins = {}

    def add_applet(self, applet, name, area=None):
        if area in self.areas:
            self.areas[area].addTab(applet, name)
        elif area == 'central':
            self.split.addWidget(applet)
        else:
            self.dockWidget(name, applet)

    def add_plugin(self, plugin):
        plugin(self)
        self._plugins[plugin.name] = plugin

    def dockWidget(self, identifier, widget, name=None,
                    allowed_area=None, position=None, alias=None):
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

        return dock_widget

    def update_namespace(self):
        """ Stub method from allwidgets. CPL: TODO

        Definition: Update namespace
        """
        self.session.interpreter.locals['project'] = self.session.project
        self.session.interpreter.locals['scene'] = self.session.scene

    def get_project_manager(self):
        if 'ProjectManager' in self._plugins:
            return self._plugins['ProjectManager'].instance()

    def get_applet_container(self):
        if 'EditorManager' in self._plugins:
            return self._plugins['EditorManager'].instance()

    applet_container = property(fget=get_applet_container)
    project_manager = property(fget=get_project_manager)
