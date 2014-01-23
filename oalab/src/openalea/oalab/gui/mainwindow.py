# -*- python -*-
#
#       Main Window class
#       VPlantsLab GUI is create here
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

from openalea.oalab.config.gui import MainConfig

class MainWindow(QtGui.QMainWindow):
    """
    Main Window Class
    """
    def __init__(self, session):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session
        
        self._dockwidgets = {}
        self._config = MainConfig()
        self._config.initialize()

        conf = path(get_openalea_home_dir()) / 'oalab.cfg'
        if conf.exists():
            self._config.load_config_file(conf)
        else :
            with conf.open() as f:
                f.write(self._config.generate_config_file())
        
        self.setWidgets(session)
        self.readSettings()     
        self.setSettingsInMenu()

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
        '''
        try:
            self.restoreGeometry(settings.value("geometry"))
            self.restoreState(settings.value("windowState"))
        except:
            # if you launch application for the first time,
            # it will save the default state
            settings.setValue("defaultGeometry", self.saveGeometry())
            settings.setValue("defaultWindowState", self.saveState())
            logger.warning("Can t restore session")
        '''
            
    def setSettingsInMenu(self):
        
        class FakeWidget(object):
            def __init__(self, parent):
                super(FakeWidget, self).__init__()
                self.mainwindow = parent
            def actions(self):
                actionDefault = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_blue.png"),"Default",self.mainwindow)
                actionRestorePref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_green.png"),"Prefered",self.mainwindow)
                actionSetPref = QtGui.QAction(QtGui.QIcon(":/images/resources/layout_red.png"),"Save pref",self.mainwindow)

                QtCore.QObject.connect(actionDefault, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.defaultSettings)
                QtCore.QObject.connect(actionRestorePref, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.preferedSettings)
                QtCore.QObject.connect(actionSetPref, QtCore.SIGNAL('triggered(bool)'),self.mainwindow.registerPreferedSettings)
                
                _actions = ["Help",[["Window Layout",actionDefault,1],
                                    ["Window Layout",actionRestorePref,1],
                                    ["Window Layout",actionSetPref,1]]]
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
        
        display = self._config.config.MainWindowConfig.get(identifier.lower(), False)
        dock_widget.setVisible(display)
        
        return dock_widget
    
    def setWidgets(self, session):
        # Menu
        dock_menu = self._dockWidget("Menu", session.menu, allowed_area=QtCore.Qt.TopDockWidgetArea, position=QtCore.Qt.TopDockWidgetArea)
        # Hide title bar
        dock_menu.setTitleBarWidget( QtGui.QWidget() ) 
        dock_menu.setMinimumSize(10,10)

        # Docks
        self._dockWidget("Project", session.project_layout_widget) # Project Manager
        self._dockWidget("Packages", session.package_manager_widget)
        self._dockWidget("PkgCategories", session.package_manager_categorie_widget, name="Package Categories")
        self._dockWidget("PackageSearch", session.package_manager_search_widget, name="Package Search")
        self._dockWidget("ControlPanel", session.control_panel, name="Control Panel", position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("3DViewer", session.viewer, name="3D Viewer", position=QtCore.Qt.RightDockWidgetArea)
        self._dockWidget("Help", session.help, position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Logger", session.logger, position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Shell", session.shell, name="IPython Shell", position=QtCore.Qt.BottomDockWidgetArea)
        self._dockWidget("Store", session.store, name="OpenAlea Store", position=QtCore.Qt.RightDockWidgetArea)

        session.control_panel.geometry_editor.setStatusBar(self.statusBar())
        self._dockwidgets['Store'].hide()

        # Central Widget
        self.setCentralWidget(session.applet_container)

        # Status bar
        status = self.statusBar()     
        status.setSizeGripEnabled(False)  
        session.statusBar = status
        self.statusBar().showMessage("OALab is ready!", 10000)   
        
        # Tabify docks
        self.tabifyDockWidget(self._dockwidgets['PackageSearch'], self._dockwidgets['PkgCategories'])
        self.tabifyDockWidget(self._dockwidgets['PkgCategories'], self._dockwidgets['Packages'])
        #self.tabifyDockWidget(self._dockwidgets['3DViewer'], self._dockwidgets['Store'])
        self.tabifyDockWidget(self._dockwidgets['Logger'], self._dockwidgets['Shell'])
        
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
