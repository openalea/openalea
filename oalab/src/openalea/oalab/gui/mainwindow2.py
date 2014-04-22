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
from openalea.core import logger
from openalea.core.path import path
from openalea.core.settings import get_openalea_home_dir

from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.plugin import discover

class MainWindow(QtGui.QMainWindow):
    """
    Main Window Class
    """
    def __init__(self, session, parent=None, args=None):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session

        self.menu = PanedMenu()

        self._dockwidgets = {}
        self._setWidgets()

        # Must be done outside MainWindow
        for plugin_factory in discover('oalab.widgets').itervalues():
            widget_factory = plugin_factory.load()()
            widget_factory(self)

    def _setWidgets(self):
        dock_menu = self.dockWidget("Menu", self.menu, position=QtCore.Qt.TopDockWidgetArea)
        dock_menu.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        dock_menu.setContentsMargins(0, 0, 0, 0)
        widget = QtGui.QLabel('Menu')
        dock_menu.setTitleBarWidget(widget)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        dock_menu.setSizePolicy(size_policy)

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
        self._dockwidgets[identifier] = dock_widget
#         display = self.session.config.get('MainWindowConfig').get(identifier.lower(), False)
#         dock_widget.setVisible(display)

        return dock_widget
