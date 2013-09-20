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
#from openalea.lpy.gui.objectpanel import LpyObjectPanelDock
from openalea.core import logger

class MainWindow(QtGui.QMainWindow):
    """
    Main Window Class
    """
    def __init__(self, session):
        super(QtGui.QMainWindow, self).__init__()
        self.session = session
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
        
    def readSettings(self):
        """
        Read a setting file and restore 
        registered settings (geometry and window state)
        """
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        try:
            self.restoreGeometry(settings.value("geometry"))
            self.restoreState(settings.value("windowState"))
        except:
            # if you launch application for the first time,
            # it will save the default state
            settings.setValue("defaultGeometry", self.saveGeometry())
            settings.setValue("defaultWindowState", self.saveState())
            logger.warning("Can t restore session")
            
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
    def setWidgets(self, session):
        # Menu
        self.menuDockWidget = QtGui.QDockWidget("Menu", self)
        # Hide title bar
        self.menuDockWidget.setTitleBarWidget( QtGui.QWidget() ) 
        self.menuDockWidget.setObjectName("Menu")
        self.menuDockWidget.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.menuDockWidget.setWidget(session.menu)
        self.menuDockWidget.setMinimumSize(10,10)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.menuDockWidget)

        # Docks
        # Project Manager
        self.projectManagerDockWidget = QtGui.QDockWidget("Project", self)
        self.projectManagerDockWidget.setObjectName("ProjectPanel")
        self.projectManagerDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.projectManagerDockWidget.setWidget(session.project_layout_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.projectManagerDockWidget)   
        
        # Package Manager
        self.packageManagerDockWidget = QtGui.QDockWidget("Packages", self)
        self.packageManagerDockWidget.setObjectName("PackagePanel")
        self.packageManagerDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.packageManagerDockWidget.setWidget(session.package_manager_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.packageManagerDockWidget)   
        
        # Package Manager Categorie
        self.packageManagerCatDockWidget = QtGui.QDockWidget("Pkg Categories", self)
        self.packageManagerCatDockWidget.setObjectName("PackagePanel")
        self.packageManagerCatDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.packageManagerCatDockWidget.setWidget(session.package_manager_categorie_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.packageManagerCatDockWidget)  
        
        # Package Manager Search
        self.packageManagerSearchDockWidget = QtGui.QDockWidget("Search Pkg", self)
        self.packageManagerSearchDockWidget.setObjectName("PackagePanel")
        self.packageManagerSearchDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.packageManagerSearchDockWidget.setWidget(session.package_manager_search_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.packageManagerSearchDockWidget)  

        ## Scene_Widget
        #self.sceneMngDockWidget = QtGui.QDockWidget("Scene Components", self)     
        #self.sceneMngDockWidget.setObjectName("SceneManager")
        #self.sceneMngDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        #self.sceneMngDockWidget.setWidget(session.scene_widget)
        #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.sceneMngDockWidget)          
        
        ## Control_Panel
        #self.controlDockWidget = LpyObjectPanelDock(parent=self,name="Control Panel", panelmanager=session.control_panel_manager)
        #self.controlDockWidget.setStatusBar(self.statusBar())
        #session.control_panel_manager.panels.append(self.controlDockWidget)
        ##self.controlDockWidget = QtGui.QDockWidget("Control Panel", self)     
        ##self.controlDockWidget.setObjectName("ControlPanel")
        ##self.controlDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        ##self.controlDockWidget.setWidget(session.control_panel)
        #self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.controlDockWidget)         
        
        ## Observer_Panel
        #self.obsDockWidget = QtGui.QDockWidget("Observer Panel", self)     
        #self.obsDockWidget.setObjectName("ObserverPanel")
        #self.obsDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        #self.obsDockWidget.setWidget(session.observer_panel)
        #self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.obsDockWidget)  
        
        # Viewer
        self.viewerDockWidget = QtGui.QDockWidget("3D Viewer", self)
        self.viewerDockWidget.setObjectName("Viewer")
        self.viewerDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.viewerDockWidget.setWidget(session.viewer)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.viewerDockWidget)
        
        # Help
        self.helpDockWidget = QtGui.QDockWidget("Help", self)     
        self.helpDockWidget.setObjectName("Help")
        self.helpDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.helpDockWidget.setWidget(session.help)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.helpDockWidget)         

        # Logger
        self.loggerDockWidget = QtGui.QDockWidget("Logger", self)     
        self.loggerDockWidget.setObjectName("Logger")
        self.loggerDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.loggerDockWidget.setWidget(session.logger)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.loggerDockWidget)  
        
        # Shell
        self.shellDockWidget = QtGui.QDockWidget("IPython Shell", self)     
        self.shellDockWidget.setObjectName("Shell")
        self.shellDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.shellDockWidget.setWidget(session.shell)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.shellDockWidget)          
        
        # Store
        self.storeDockWidget = QtGui.QDockWidget("OpenAlea Store", self)     
        self.storeDockWidget.setObjectName("Store")
        self.storeDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.storeDockWidget.setWidget(session.store)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.storeDockWidget)  
        self.storeDockWidget.hide()
        session.storeDockWidget = self.storeDockWidget

        # Central Widget
        self.setCentralWidget(session.applet_container)

        # Status bar
        status = self.statusBar()     
        status.setSizeGripEnabled(False)  
        session.statusBar = status
        self.statusBar().showMessage("OALab is ready!", 10000)   
        
        # Tabify docks
        self.tabifyDockWidget(self.packageManagerSearchDockWidget, self.packageManagerCatDockWidget)
        self.tabifyDockWidget(self.packageManagerCatDockWidget, self.packageManagerDockWidget)
        #self.tabifyDockWidget(self.packageManagerDockWidget, self.projectManagerDockWidget)
        
        #self.tabifyDockWidget(self.obsDockWidget, self.controlDockWidget)
        #self.tabifyDockWidget(self.sceneMngDockWidget, self.viewerDockWidget)
        self.tabifyDockWidget(self.viewerDockWidget, self.storeDockWidget)
        #self.tabifyDockWidget(self.helpDockWidget, self.loggerDockWidget)
        #self.tabifyDockWidget(self.helpDockWidget, self.loggerDockWidget)
        self.tabifyDockWidget(self.loggerDockWidget, self.shellDockWidget)
        
    def changeMenuTab(self, old, new):
        """
        Set tab of 'new' current in the menu
        """
        try:
            # Get Tab Name
            name = new.mainMenu()
            # Get Menu
            menu = self.menuDockWidget.widget()
            # Find tab named 'name'
            for index in range(menu.count()):
                if menu.tabText(index) == name:
                    # Set Current
                    menu.setCurrentIndex(index)
        except:
            pass
            
