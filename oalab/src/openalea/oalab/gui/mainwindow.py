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

import types

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import logger
from openalea.core.path import path
from openalea.core.settings import get_openalea_home_dir

from openalea.oalab.config.main import MainConfig
from openalea.oalab.config.template import config_file_default, config_file_mini, config_file_3d, config_file_tissue, config_file_plant

class MainWindow(QtGui.QMainWindow):
    """
    Main Window Class
    """
    def __init__(self, session, args=None):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session
        
        self._dockwidgets = {}

        if "-e" in args or "--extension" in args:
            self.session.extension = args[-1]
        self.changeExtension(extension=self.session.extension)
            
        # Central Widget
        self.setCentralWidget(session.applet_container)

        self.readSettings()     
        self.setSettingsInMenu()
        self.setShowDockInMenu()
        self.setSelectLabInMenu()
        
    def changeExtension(self, extension=None):
        """
        Change to a new extension.
        
        :param extension: can be "mini", "3d", "tissue", "plant"
        """
        self.removeDocksWidgets()
        
        conf = path(get_openalea_home_dir()) / 'oalab.cfg'
        if extension in ["mini", "3d", "tissue", "plant"]:
            conf = path(get_openalea_home_dir()) / ('oalab_' + extension + '.cfg')
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
        self.session.load_config_file(conf)
        
        self.setWidgets(self.session)
                
                
    def closeEvent(self, event):
        self.writeSettings()
        super(QtGui.QMainWindow, self).closeEvent(event)

    ####################################################################
    ### Settings
    ####################################################################
    def writeSettings(self):
        """
        Register current settings (geometry and window state)
        in a setting file
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("session", self.session.project)
        
    def readSettings(self):
        """
        Read a setting file and restore 
        registered settings (geometry and window state)
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")

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
                actionDefault = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_blue.png"),"Load Default",self.mainwindow)
                actionRestorePref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_green.png"),"Load Prefered",self.mainwindow)
                actionSetPref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_red.png"),"Save Prefered",self.mainwindow)

                QtCore.QObject.connect(actionDefault, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.defaultSettings)
                QtCore.QObject.connect(actionRestorePref, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.preferedSettings)
                QtCore.QObject.connect(actionSetPref, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.registerPreferedSettings)
                
                _actions = [["Help","Window Layout",actionDefault,1],
                            ["Help","Window Layout",actionRestorePref,1],
                            ["Help","Window Layout",actionSetPref,1]]
                return _actions
                
        settings = FakeWidget(parent=self)
        self.session.connect_actions(settings)       
        
    def setShowDockInMenu(self):
        """
        Use it to add show/hide dockwidget in menu
        """
        children = self.findChildren(QtGui.QDockWidget)
        
        for child in children:
            name = child.windowTitle()
            actionShow = QtGui.QAction(QtGui.QIcon(":/images/resources/show.png"),name,self)
            actionHide = QtGui.QAction(QtGui.QIcon(":/images/resources/hide.png"),name,self)
            
            QtCore.QObject.connect(actionShow, QtCore.SIGNAL('triggered(bool)'),child.show)
            QtCore.QObject.connect(actionHide, QtCore.SIGNAL('triggered(bool)'),child.hide)
            
            child._actions = [["View","Show",actionShow,1],
                             ["View","Hide",actionHide,1]]
            def actions(self):
                return self._actions
            
            child.actions = types.MethodType( actions, child)
            self.session.connect_actions(child) 
            
    def setSelectLabInMenu(self):
        class FakeWidget(object):
            def __init__(self, parent):
                """
                Use it to add features like setting widgets layout
                """
                super(FakeWidget, self).__init__()
                self.mainwindow = parent
            def actions(self):
                minilab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"MiniLab", self.mainwindow)
                lab3d = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"3DLab", self.mainwindow)
                plantlab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"PlantLab", self.mainwindow)
                tissuelab = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"TissueLab", self.mainwindow)

                QtCore.QObject.connect(minilab, QtCore.SIGNAL('triggered(bool)'),self.mainwindow._mini)
                QtCore.QObject.connect(lab3d, QtCore.SIGNAL('triggered(bool)'),self.mainwindow._lab3d)
                QtCore.QObject.connect(plantlab, QtCore.SIGNAL('triggered(bool)'),self.mainwindow._plant)
                QtCore.QObject.connect(tissuelab, QtCore.SIGNAL('triggered(bool)'),self.mainwindow._tissue)
                
                _actions = [["Extension","Select an Extension",minilab,0],
                            ["Extension","Select an Extension",lab3d,0],
                            ["Extension","Select an Extension",plantlab,0],
                            ["Extension","Select an Extension",tissuelab,0]]
                return _actions
                
        settings = FakeWidget(parent=self)
        self.session.connect_actions(settings)  
    
    def defaultSettings(self):
        """
        Restore default settings (geometry and window state)
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        self.restoreGeometry(settings.value("defaultGeometry"))
        self.restoreState(settings.value("defaultWindowState"))
        
    def preferedSettings(self):
        """
        Get prefered settings and restore them
        """
        try:
            settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
            self.restoreGeometry(settings.value("preferedGeometry"))
            self.restoreState(settings.value("preferedWindowState"))
        except:
            logger.warning("Can t restore prefered session")
        
    def registerPreferedSettings(self):
        """
        Register current settings as preferd settings
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        settings.setValue("preferedGeometry", self.saveGeometry())
        settings.setValue("preferedWindowState", self.saveState())
    
    ####################################################################
    ### Widgets
    ####################################################################
    
    def _dockWidget(self, identifier, widget, name=None, allowed_area=None, position=None):
        if name is None :
            name = identifier.capitalize()
        if allowed_area is None:
            allowed_area = QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea
        if position is None:
            position = QtCore.Qt.LeftDockWidgetArea
    
        dock_widget = QtGui.QDockWidget(name, self)
        dock_widget.setObjectName("%sPanel" % identifier)
        dock_widget.setAllowedAreas(allowed_area)
        dock_widget.setWidget(widget)
        self.addDockWidget(position, dock_widget)
        self._dockwidgets[identifier] = dock_widget
        
        display = self.session.config.MainWindowConfig.get(identifier.lower(), False)
        dock_widget.setVisible(display)
        
        return dock_widget
    
    def setWidgets(self, session):
        # Menu
        dock_menu = self._dockWidget("Menu", session.menu, allowed_area=QtCore.Qt.TopDockWidgetArea, position=QtCore.Qt.TopDockWidgetArea)
        # Hide title bar
        dock_menu.setTitleBarWidget( QtGui.QWidget() ) 
        dock_menu.setMinimumSize(10,10)

        # Docks
        self._dockWidget("Project", session.applets["Project"]) # Project Manager
        self._dockWidget("Packages", session.applets["Packages"])
        self._dockWidget("PackageCategories", session.applets["PackageCategories"], name="Package Categories")
        self._dockWidget("PackageSearch", session.applets["PackageSearch"], name="Package Search")
        self._dockWidget("ControlPanel", session.applets["ControlPanel"], name="Control Panel", position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Viewer3D", session.applets["Viewer3D"], name="3D Viewer", position=QtCore.Qt.RightDockWidgetArea)
        self._dockWidget("Help", session.applets["Help"], position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Logger", session.applets["Logger"], position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Store", session.applets["Store"], name="OpenAlea Store", position=QtCore.Qt.RightDockWidgetArea)
        self._dockWidget("Shell", session.shell, name="IPython Shell", position=QtCore.Qt.BottomDockWidgetArea)

        session.applets['ControlPanel'].geometry_editor.setStatusBar(self.statusBar())
        self._dockwidgets['Store'].hide()

        # Status bar
        status = self.statusBar()     
        status.setSizeGripEnabled(False)  
        session.statusBar = status
        self.statusBar().showMessage("OALab is ready!", 10000)   
        
        # Tabify docks
        self.tabifyDockWidget(self._dockwidgets['PackageSearch'], self._dockwidgets['PackageCategories'])
        self.tabifyDockWidget(self._dockwidgets['PackageCategories'], self._dockwidgets['Packages'])
        self.tabifyDockWidget(self._dockwidgets['Viewer3D'], self._dockwidgets['Store'])
        self.tabifyDockWidget(self._dockwidgets['Logger'], self._dockwidgets['Shell'])
        
        self._dockwidgets['Store'].setTitleBarWidget(QtGui.QWidget())
        
    def removeDocksWidgets(self):
        children = self.findChildren(QtGui.QDockWidget)
        
        for child in children:
            self.removeDockWidget(child)
        
    def changeMenuTab(self, old, new):
        """
        Set tab of 'new' current in the menu
        
        :param old: old current widget. Not used.
        :param new: current widget to check if we have to change menu
        """
        try:
            # Get Tab Name
            name = new.mainMenu()
            # Get Menu
            menu = self._dockwidgets['Menu'].widget()
            # Find tab named 'name'
            for index in range(menu.count()):
                if menu.tabText(index) == name:
                    # Set Current
                    menu.setCurrentIndex(index)
        except:
            pass
            
    def _mini(self):
        self.changeExtension("mini")      
          
    def _lab3d(self):
        self.changeExtension("3d")     
                  
    def _plant(self):
        self.changeExtension("plant")   
        
    def _tissue(self):
        self.changeExtension("tissue")           
