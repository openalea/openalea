#---------------------------------------------
# Main Window class
# 
# VPlantsLab GUI is create here
#---------------------------------------------

import sys
import os

import qt

from openalea.oalab.scene.view3d import view3D
from openalea.oalab.history.history import History
from openalea.oalab.control.controlmanager import ControlManager

# from openalea.core.logger import get_logger
from openalea.visualea.splitterui import SplittableUI

from openalea.oalab.editor.text_editor import PythonCodeEditor as Editor
from openalea.oalab.editor.text_editor import LPyCodeEditor as LPyEditor
from openalea.oalab.editor.text_editor import SelectEditor
from openalea.oalab.shell.shell import ShellWidget
from openalea.oalab.shell.interpreter import Interpreter
from openalea.oalab.project.project import ProjectManager


# sn_logger = get_logger(__name__)


class MainWindow(qt.QMainWindow):
    def __init__(self, parent=None):
        super(qt.QMainWindow, self).__init__(parent)
        
        # -- show the splash screen --
        self.splash = show_splash_screen()   
        
        self.showEditors = False
        
        # self.logger = sn_logger
        
        # window title and icon
        self.setWindowTitle("Virtual Plants Laboratory")
        self.setWindowIcon(qt.QIcon("./resources/openalea_icon2.png"))
        
        self.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.showMaximized()
        # project
        self.projectManager = ProjectManager()
        self.projectManager.new_project()
        
        # list of central widgets
        self.widList = []
        
        # Central widgets
        # Virtual World
        self.set_virtual_world()
        self.splittable = SplittableUI(parent=self, content=self.VW)
        # editor
        self.set_text_editor_container()
        self.hide_editors()
        
        # self.splittable.splitPane(content=self.widList[1], paneId=0, direction=qt.Qt.Horizontal, amount=0.8)
        
        self.setCentralWidget(self.splittable)
        
        # Other widgets
        # Ressources
        self.set_ressources_manager()
        # Packages
        # self.set_package_manager()
        
        # control panel
        self.set_control_panel()
        # observation panel
        self.set_observation_panel()
        # tabify control and observation panels
        self.tabifyDockWidget(self.controlDockWidget, self.obsDockWidget)
        
        # shell
        self.set_shell()
        # log
        self.set_log()
        # tabify control and observation panels
        self.tabifyDockWidget(self.shellDockWidget, self.logDockWidget)

        # help
        self.set_help()

        
        
        # Status Bar
        self.set_status_bar()
        # Actions bars and buttons
        self.set_editor_actions()
        self.set_model_actions()
        self.set_model_buttons()
        self.set_permanent_editor_buttons()
        # self.set_model_2_actions()
        # self.set_model_2_buttons()
        self.set_view_actions()
        self.set_view_buttons()
        
        self.splash.finish(self)
    
    #----------------------------------------
    # Setup Central Widget
    #----------------------------------------
    
    def add_widget(self, wid):
        # self.__centralStack.addWidget(wid)
        # self.__centralStack.setCurrentWidget(wid)
        pass
        
    def set_central_widget(self, row, column):
        pass
        # self.__centralStack.addWidget(wid)
        """
        layout = qt.QGridLayout()
        self.central = qt.QWidget()
        self.central.setMinimumSize(600, 500)
        
        l = len(self.widList)
        
        # Fill central Widget in a layout
        i=0
        for x in range(row):
            for y in range(column):
                if i < l:
                    wid = self.widList[i]
                # if they are more panels than widgets in widgList
                else:
                    wid = qt.QWidget()
                
                try:
                    wid.setMinimumSize(100,100) 
                except:
                    pass
  
                layout.addWidget(wid ,x ,y)
                i += 1
        
        # If they are too many widgets, they are add (in new lines)
        if l > i:
            for w in self.widList[i:]:
                layout.addWidget(w)

        
        self.central.setLayout(layout)

        self.setCentralWidget(self.central)  
        """

        
    def set_central_widget11(self):    
        if self.showEditors == True:
            self.hide_editors()
    def set_central_widget12(self):    
        if self.showEditors == False:
            self.show_editors()
    def set_central_widget13(self):    
        self.set_central_widget(1,3)
    def set_central_widget21(self):    
        self.set_central_widget(2,1)
    def set_central_widget22(self):    
        self.set_central_widget(2,2)
    def set_central_widget23(self):    
        self.set_central_widget(2,3)   

    #----------------------------------------
    # Show / Hide editors
    #----------------------------------------
    def show_hide_editors(self):    
        if self.showEditors == False:
            self.show_editors()
        else:
            self.hide_editors()
            
    def show_editors(self):
        if self.showEditors == False:
            self.splittable.splitPane(content=self.widList[1], paneId=0, direction=qt.Qt.Horizontal, amount=0.8)
            self.showEditors = True
            
    def hide_editors(self):
        if self.showEditors == True:
            self.splittable.collapsePane(paneId=0)
            self.showEditors = False
            
    #----------------------------------------
    # Setup Virtual World
    #----------------------------------------
    def set_virtual_world(self):
        self.history = History()
    
        view = view3D(parent=self)
        view.setObjectName("view3D")
        
        view.start()    
        
        self.VW = view
        self.VW.setMinimumSize(300, 300)
        
        self.widList.append(self.VW)
        
        self.add_widget(self.VW)
        
        # Connect the scene3D (self.VW) to the history list (self.history)
        self.actionHistoryList = qt.QAction(self)
        qt.QObject.connect(self.history.obj, qt.SIGNAL('HistoryChanged'),self.VW.setScene)
        qt.QObject.connect(self.history.obj, qt.SIGNAL('HistoryChanged'),self.update_ressources_manager)
    
    def add_virtual_world_viewer(self):
        print "This action doens't work for the moment('new virtual world viewer')."
        pass
        # view = view3D(scene=self.VW.getScene(),parent=self,shareWidget=self.VW)
        # view.start()
        # self.widList.append(view)
        # self.splittable.splitPane(content=self.widList[2], paneId=0, direction=qt.Qt.Vertical, amount=0.8)
        # self.show_editors()
        
    def add_soil(self):
        import openalea.plantgl.all as pgl
        from random import randint, random
        box = pgl.Translated((0.5,0.5,-0.5),pgl.Scaled((0.9,0.9,0.9),pgl.Box()))
        material = lambda : pgl.Material(ambient=(randint(0,255), randint(0,255), randint(0,255)), transparency=float(randint(100,255)))
        scene = [ pgl.Shape(pgl.Translated((x,y,z),box), material()) for x in range(-5,5) for y in range(-5,5) for z in range(0,-5,-1)]
        soil = pgl.Scene(scene)
        self.history.add(name="soil",obj=soil)
        # for x in range(-5,5):
            # for y in range(-5,5):
                # for z in range(0,-5,-1):
                    # s = Soil(pgl.Translated((x,y,z),box), material())
                    # self.history.add("soil",s)
        # self.VW.addToScene(sphere)
  
    def add_plant(self):
        '''
        from math import pi
        from openalea.plantgl.all import Polyline2D, Material, Translated, Swung, Shape
        def line_prof():
            """ create a list of profiles with polyline """
            return [Polyline2D([(0,0),(1.5,0.1),(0.75,2),(1.1,2.2),(0.55,3),(0.8,3.1),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.2,0.1),(0.7,2),(1.0,2.3),(0.5,3.1),(0.8,3.1),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.4,0.1),(0.8,2),(1.1,2.1),(0.6,3),(0.85,3.0),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.6,0.1),(0.8,2),(1.2,2.2),(0.4,3),(0.7,3.2),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.5,0.1),(0.75,2),(1.1,2.2),(0.55,3),(0.8,3.1),(0,4),(0,4)])]

        
        #the angles to associate to profiles
        angles = [0,pi/2.,pi,3.*pi/2.,2.*pi]
        col = Material((0,100,50))
        
        class Plant(Shape):pass
        
        # a swung interpolating the profiles associated to the angles
        tree = Plant(Translated(1,1,0,Swung(line_prof(),angles)),col)
        '''
        import random
        from vplants.weberpenn import tree_client
        from vplants.weberpenn import tree_server
        from vplants.weberpenn import tree_geom
        import openalea.plantgl.all as pgl


        p= [(0.5,0), ( 0,0.5), (-0.5,0),(0,-0.5),(0.5,0)]
        section= pgl.Polyline2D(p)

        param = tree_client.Quaking_Aspen()
        param.order-= 2
        param.scale = (7,2)
        def f( param, section=section, position= (0,0,0), scene=None ):
            param.leaves= 0
            client= tree_client.Weber_Laws(param)
            server= tree_server.TreeServer(client)
            server.run()
            geom= tree_geom.GeomEngine(server,section,position)
            scene= geom.scene('axis', scene)
            return scene
        scene = f(param) 

        self.history.add(name="tree",obj=scene)
    
    def add_sun(self):
        import openalea.plantgl.all as pgl
        sun = pgl.Shape(pgl.Translated((3,3,7),pgl.Sphere()), pgl.Material(ambient=(255, 255, 0)))      
        self.history.add(name="sun",obj=sun)
        
    #----------------------------------------
    # Setup Ressources Manager / History Viewer Dock Widget
    #----------------------------------------
    def set_ressources_manager(self):
        # Ressources
        self.ressManaWid = qt.QTableWidget(0,2)       
        self.ressManaWid.setMinimumSize(100, 100)

        self.ressManaDockWidget = qt.QDockWidget("Virtual World", self)
        self.ressManaDockWidget.setObjectName("RessMana")
        self.ressManaDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.ressManaDockWidget.setWidget(self.ressManaWid)
        self.addDockWidget(qt.Qt.LeftDockWidgetArea, self.ressManaDockWidget) 
        
        hist = self.history.getHistory()
        self.update_ressources_manager(hist)
        
    def reset_ressources_manager(self):
        self.ressManaWid.clear()
        headerName1 = qt.QTableWidgetItem("name")
        headerName2 = qt.QTableWidgetItem("value")
        self.ressManaWid.setHorizontalHeaderItem(0,headerName1)
        self.ressManaWid.setHorizontalHeaderItem(1,headerName2)
        
    def update_ressources_manager(self, scene):
        self.reset_ressources_manager()
        row = 0
        for h in scene:
            itemName = qt.QTableWidgetItem(str(h))
            itemObj = qt.QTableWidgetItem(str(scene[h]))
            if self.ressManaWid.rowCount()<=row:
                self.ressManaWid.insertRow(row)
            self.ressManaWid.setItem(row,0,itemName)
            self.ressManaWid.setItem(row,1,itemObj)
            row += 1
    
    
    #----------------------------------------
    # Setup Package Manager Dock Widget
    #----------------------------------------
    def set_package_manager(self):
        # Ressources
        self.packManaWid = qt.QWidget()
        self.packManaWid.setMinimumSize(100, 100)
        self.packManaWid.setMaximumSize(400, 400)

        self.packManaDockWidget = qt.QDockWidget("Package Manager", self)
        self.packManaDockWidget.setObjectName("RessMana")
        self.packManaDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.packManaDockWidget.setWidget(self.packManaWid)
        self.addDockWidget(qt.Qt.LeftDockWidgetArea, self.packManaDockWidget)     
        
    
    #----------------------------------------
    # Setup Help Dock Widget
    #----------------------------------------
    def set_help(self):
    
        # Help
        self.helpWid = qt.QWidget()
        self.helpWid.setMinimumSize(150, 150)
        self.helpWid.setMaximumSize(400, 400)

        self.helpDockWidget = qt.QDockWidget("Help", self)
        self.helpDockWidget.setObjectName("Help")
        self.helpDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.helpDockWidget.setWidget(self.helpWid)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.helpDockWidget)         
    
    
    
    #----------------------------------------
    # Setup Control Panel Dock Widget
    #----------------------------------------
    def set_control_panel(self):
        """ Set the control panel
        Only once by project!
        """
        
        # Set THE control manager
        self.controlManager = ControlManager()
        
        # Create widget control panel
        self.controlWid = qt.QTableWidget(0,2)
        self.reset_control_panel()
        self.controlWid.setMinimumSize(50, 50) 
        self.controlDockWidget = qt.QDockWidget("Control Panel", self)
        self.controlDockWidget.setObjectName("ControlPanel")
        self.controlDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea | qt.Qt.BottomDockWidgetArea)
        self.controlDockWidget.setWidget(self.controlWid)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.controlDockWidget)   

        # qt.QObject.connect(self.controlWid, qt.SIGNAL('cellClicked(int,int)'),self.printTest) 
        qt.QObject.connect(self.controlWid, qt.SIGNAL('cellDoubleClicked(int,int)'),self.edit_control)        
            
    def edit_control(self, row, column):
        cont = self.controlWid.item(row,column)
        print(cont)

    
    def set_controls_from_editor(self, editor):
        """ Set Control from editor 'editor' in the control manager and the widget control panel.
        """
        self.reset_control_panel()
        
        # Get new controls which come from editor
        new_controls = editor.get_widgets_controls()
        # Add new controls in control manager
        for name in new_controls:
            self.controlManager.add_control(name,new_controls[name]) 
        row = 0
        # Get all controls
        all_controls = self.controlManager.get_controls()
        
        # Display all controls
        for n in all_controls:
            itemName = qt.QTableWidgetItem(str(n))
            itemObj = qt.QTableWidgetItem(str(all_controls[n]))
            # Add row if necessary
            if self.controlWid.rowCount()<=row:
                self.controlWid.insertRow(row)
            self.controlWid.setItem(row,0,itemName)
            self.controlWid.setItem(row,1,itemObj)
            row += 1
            
            
    def reset_control_panel(self):
        """Clear the control panel and set the headers.
        """
        self.controlWid.clear()
        headerName1 = qt.QTableWidgetItem("name")
        headerName2 = qt.QTableWidgetItem("value")
        self.controlWid.setHorizontalHeaderItem(0,headerName1)
        self.controlWid.setHorizontalHeaderItem(1,headerName2)

    
    #----------------------------------------
    # Setup Observation Panel Dock Widget
    #----------------------------------------
    def set_observation_panel(self):
    
        # Help
        self.obsWid = qt.QLabel("number of leafs : 42000")
        self.obsWid.setMinimumSize(50, 50)
        # self.obsWid.setMinimumSize(400, 400)

        self.obsDockWidget = qt.QDockWidget("Observation Panel", self)
        self.obsDockWidget.setObjectName("ObservationPanel")
        self.obsDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea | qt.Qt.BottomDockWidgetArea)
        self.obsDockWidget.setWidget(self.obsWid)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.obsDockWidget) 

        
    #----------------------------------------
    # Setup Editor Container Dock Widget
    #----------------------------------------
    def set_text_editor_container(self):
    
        # Editor
        self.textEditorContainer = qt.QTabWidget()
        self.textEditorContainer.max_ID = 0
        self.textEditorContainer.current_file_name = [None]
        self.textEditorContainer.current_extension = [None]
        self.textEditorContainer.current_path_and_fname = [None]
        self.textEditorContainer.current_path = [None]
        self.textEditorContainer.setTabsClosable(True)
        self.textEditorContainer.setMinimumSize(250, 250)
        
        # editorsDockWidget = qt.QDockWidget("Editors", self)
        # editorsDockWidget.setObjectName("Editors")
        # editorsDockWidget.setAllowedAreas(qt.Qt.LeftDockWidgetArea | qt.Qt.RightDockWidgetArea | qt.Qt.TopDockWidgetArea)
        # editorsDockWidget.setWidget(self.textEditorContainer)
        # self.addDockWidget(qt.Qt.RightDockWidgetArea, editorsDockWidget)
        
        self.widList.append(self.textEditorContainer)
        self.new()
               
    def new_text_editor(self, name="NewFile", type="py"):
        # central widget => Editor
        if(self.textEditorContainer.tabText(self.textEditorContainer.currentIndex())=="Select your editor type"):
            self.textEditorContainer.removeTab(self.textEditorContainer.currentIndex())
        if type=='py':
            self.editorWidget = Editor(parent=self)
            self.textEditorContainer.addTab(self.editorWidget, name)
            self.textEditorContainer.setCurrentWidget(self.editorWidget)
            self.setup_new_tab()
        elif type=='lpy':
            self.editorWidget = LPyEditor()
            self.textEditorContainer.addTab(self.editorWidget, name)
            self.textEditorContainer.setCurrentWidget(self.editorWidget)
            self.setup_new_tab()
            self.set_controls_from_editor(self.editorWidget)
        elif type=='wf':
            self.editorWidget = Editor(parent=self)
            self.textEditorContainer.addTab(self.editorWidget, name)
            self.textEditorContainer.setCurrentWidget(self.editorWidget)
            self.setup_new_tab()    
            self.set_controls_from_editor(LPyEditor())

    
    def show_select_editor(self, name="Select your editor type"):
        self.selectEditor = SelectEditor(parent=self)
        self.textEditorContainer.addTab(self.selectEditor, name)
        self.textEditorContainer.setCurrentWidget(self.selectEditor)
        self.add_widget(self.selectEditor)
    
    def setup_new_tab(self):
        self.textEditorContainer.max_ID += 1
        max_ID = self.textEditorContainer.max_ID
        self.textEditorContainer.current_file_name.append(None)
        self.textEditorContainer.current_extension.append(None)
        self.textEditorContainer.current_path_and_fname.append(None)
        self.textEditorContainer.current_path.append(None)
        self.textEditorContainer.currentWidget().ID = max_ID
        self.textEditorContainer.currentWidget().setup()
        
        self.set_local_actions()
        self.set_local_top_buttons()
        self.set_local_menu_bar()
    
    #----------------------------------------
    # Setup Windows, bars, buttons
    #----------------------------------------
    def set_model_actions(self):
        # Create actions
        self.actionAddPlant = qt.QAction(self)
        self.actionPlantGrowing = qt.QAction(self)
        
        self.actionSoil = qt.QAction(self)
        self.actionSky = qt.QAction(self)
        self.actionGreenhouse = qt.QAction(self)
        
        self.actionPlay= qt.QAction(self)
        
        self.actionGlobalWorkflow= qt.QAction(self)
                
        # Set title of buttons       
        self.actionAddPlant.setText(qt.QApplication.translate("MainWindow", "New Plant", None, qt.QApplication.UnicodeUTF8))
        self.actionPlantGrowing.setText(qt.QApplication.translate("MainWindow", "Plant Growth", None, qt.QApplication.UnicodeUTF8))
        
        self.actionSoil.setText(qt.QApplication.translate("MainWindow", "Soil", None, qt.QApplication.UnicodeUTF8))
        self.actionSky.setText(qt.QApplication.translate("MainWindow", "Weather", None, qt.QApplication.UnicodeUTF8))
        self.actionGreenhouse.setText(qt.QApplication.translate("MainWindow", "Greenhouse", None, qt.QApplication.UnicodeUTF8))
            
        self.actionPlay.setText(qt.QApplication.translate("MainWindow", "Run", None, qt.QApplication.UnicodeUTF8))
        
        self.actionGlobalWorkflow.setText(qt.QApplication.translate("MainWindow", "Global Workflow", None, qt.QApplication.UnicodeUTF8))

    def set_model_2_actions(self):
        # Create actions
        self.actionBDD = qt.QAction(self)
        self.actionPy = qt.QAction(self)
        self.actionLPy = qt.QAction(self)
        self.actionWF = qt.QAction(self)

                
        # Set title of buttons       
        self.actionBDD.setText(qt.QApplication.translate("MainWindow", "From DataBase", None, qt.QApplication.UnicodeUTF8))
        self.actionPy.setText(qt.QApplication.translate("MainWindow", "From Python", None, qt.QApplication.UnicodeUTF8))
        self.actionLPy.setText(qt.QApplication.translate("MainWindow", "From LPy", None, qt.QApplication.UnicodeUTF8))
        self.actionWF.setText(qt.QApplication.translate("MainWindow", "From Workflow", None, qt.QApplication.UnicodeUTF8))

    
        
    def set_editor_actions(self):
        # Create actions
        self.actionNew = qt.QAction(self)
        self.actionOpen = qt.QAction(self)
        self.actionSave = qt.QAction(self)
        self.actionSaveAll = qt.QAction(self)
        self.actionSaveAs = qt.QAction(self)
        self.actionClose = qt.QAction(self)

        # Set title of buttons
        self.actionNew.setText(qt.QApplication.translate("MainWindow", "New", None, qt.QApplication.UnicodeUTF8))
        self.actionOpen.setText(qt.QApplication.translate("MainWindow", "Open", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setText(qt.QApplication.translate("MainWindow", "Save", None, qt.QApplication.UnicodeUTF8))
        self.actionSaveAll.setText(qt.QApplication.translate("MainWindow", "Save All", None, qt.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(qt.QApplication.translate("MainWindow", "Save As", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setText(qt.QApplication.translate("MainWindow", "Close", None, qt.QApplication.UnicodeUTF8))
    
    
    def set_view_actions(self):
        # Create actions
        self.action11 = qt.QAction(self)
        self.action12 = qt.QAction(self)
        self.action13 = qt.QAction(self)
        self.action21 = qt.QAction(self)
        self.action22 = qt.QAction(self)
        self.action23 = qt.QAction(self)
        self.actionEditors = qt.QAction(self)
        
        # Set title of buttons
        self.action11.setText(qt.QApplication.translate("MainWindow", "1 block", None, qt.QApplication.UnicodeUTF8))
        self.action12.setText(qt.QApplication.translate("MainWindow", "grid 1x2", None, qt.QApplication.UnicodeUTF8))
        self.action13.setText(qt.QApplication.translate("MainWindow", "grid 1x3", None, qt.QApplication.UnicodeUTF8))
        self.action21.setText(qt.QApplication.translate("MainWindow", "grid 2x1", None, qt.QApplication.UnicodeUTF8))
        self.action22.setText(qt.QApplication.translate("MainWindow", "grid 2x2", None, qt.QApplication.UnicodeUTF8))
        self.action23.setText(qt.QApplication.translate("MainWindow", "grid 2x3", None, qt.QApplication.UnicodeUTF8))
        self.actionEditors.setText(qt.QApplication.translate("MainWindow", "show/hide editors", None, qt.QApplication.UnicodeUTF8))
    
    def set_view_buttons(self):
        self.ViewBar = qt.QToolBar(self)
        self.ViewBar.setToolButtonStyle(qt.Qt.ToolButtonIconOnly)
        size = qt.QSize(20, 20)
        self.ViewBar.setIconSize(size)
        self.addToolBar(qt.Qt.LeftToolBarArea, self.ViewBar)    
        
        icon2_2 = qt.QIcon()
        icon2_2.addPixmap(qt.QPixmap("./resources/new/square11.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action11.setIcon(icon2_2)
        icon2_3 = qt.QIcon()
        icon2_3.addPixmap(qt.QPixmap("./resources/new/square12.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action12.setIcon(icon2_3)
        icon5 = qt.QIcon()
        icon5.addPixmap(qt.QPixmap("./resources/new/square13.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action13.setIcon(icon5)
        icon6 = qt.QIcon()
        icon6.addPixmap(qt.QPixmap("./resources/new/square21.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action21.setIcon(icon6)
        icon7 = qt.QIcon()
        icon7.addPixmap(qt.QPixmap("./resources/new/square22.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action22.setIcon(icon7)
        icon8 = qt.QIcon()
        icon8.addPixmap(qt.QPixmap("./resources/new/square23.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.action23.setIcon(icon8)
        icon9 = qt.QIcon()
        icon9.addPixmap(qt.QPixmap("./resources/book.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionEditors.setIcon(icon9)
        

        # connect actions to buttons
        qt.QObject.connect(self.action11, qt.SIGNAL('triggered(bool)'),self.set_central_widget11)
        qt.QObject.connect(self.action12, qt.SIGNAL('triggered(bool)'),self.set_central_widget12)
        qt.QObject.connect(self.action13, qt.SIGNAL('triggered(bool)'),self.add_virtual_world_viewer) 
        qt.QObject.connect(self.action21, qt.SIGNAL('triggered(bool)'),self.set_central_widget21)
        qt.QObject.connect(self.action22, qt.SIGNAL('triggered(bool)'),self.set_central_widget22)         
        qt.QObject.connect(self.action23, qt.SIGNAL('triggered(bool)'),self.set_central_widget23)         
        qt.QObject.connect(self.actionEditors, qt.SIGNAL('triggered(bool)'),self.show_hide_editors)    
        
        self.ViewBar.addAction(self.action11)
        self.ViewBar.addSeparator()
        self.ViewBar.addAction(self.action12)
        self.ViewBar.addSeparator()
        self.ViewBar.addAction(self.action13)
        # self.ViewBar.addAction(self.action22)
        # self.ViewBar.addAction(self.action23)
        self.ViewBar.addSeparator()
        self.ViewBar.addAction(self.actionEditors)
    
    def set_model_buttons(self):
        self.ModelBar = qt.QToolBar(self)
        self.ModelBar.setToolButtonStyle(qt.Qt.ToolButtonTextUnderIcon)
        size = qt.QSize(40, 40)
        self.ModelBar.setIconSize(size)
        self.addToolBar(qt.Qt.TopToolBarArea, self.ModelBar)
        self.addToolBarBreak()        
        
        icon2_2 = qt.QIcon()
        icon2_2.addPixmap(qt.QPixmap("./resources/new/plant.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionAddPlant.setIcon(icon2_2)
        icon2_3 = qt.QIcon()
        icon2_3.addPixmap(qt.QPixmap("./resources/new/grow.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionPlantGrowing.setIcon(icon2_3)
        icon5 = qt.QIcon()
        icon5.addPixmap(qt.QPixmap("./resources/new/soil.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionSoil.setIcon(icon5)
        icon6 = qt.QIcon()
        icon6.addPixmap(qt.QPixmap("./resources/new/sky.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionSky.setIcon(icon6)
        icon7 = qt.QIcon()
        icon7.addPixmap(qt.QPixmap("./resources/new/greenhouse.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionGreenhouse.setIcon(icon7)       
        icon2_4 = qt.QIcon()
        icon2_4.addPixmap(qt.QPixmap("./resources/new/play.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionPlay.setIcon(icon2_4)
        icon1 = qt.QIcon()
        icon1.addPixmap(qt.QPixmap("./resources/new/workflow.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionGlobalWorkflow.setIcon(icon1)
        
        # connect actions to buttons
        # qt.QObject.connect(self.actionAddPlant, qt.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QObject.connect(self.actionPlantGrowing, qt.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QObject.connect(self.actionSoil, qt.SIGNAL('triggered(bool)'),self.set_text_editor_container) 
        # qt.QObject.connect(self.actionSky, qt.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QObject.connect(self.actionGreenhouse, qt.SIGNAL('triggered(bool)'),self.set_text_editor_container)         
        # qt.QObject.connect(self.actionPlay, qt.SIGNAL('triggered(bool)'),self.play) 
        # qt.QObject.connect(self.actionGlobalWorkflow, qt.SIGNAL('triggered(bool)'),self.globalWorkflow) 
        
        qt.QObject.connect(self.actionSoil, qt.SIGNAL('triggered(bool)'),self.add_soil)
        qt.QObject.connect(self.actionAddPlant, qt.SIGNAL('triggered(bool)'),self.add_plant)
        qt.QObject.connect(self.actionSky, qt.SIGNAL('triggered(bool)'),self.add_sun)
        
        self.ModelBar.addAction(self.actionAddPlant)
        self.ModelBar.addAction(self.actionPlantGrowing)
        self.ModelBar.addSeparator()
        self.ModelBar.addAction(self.actionSoil)
        self.ModelBar.addAction(self.actionSky)
        self.ModelBar.addAction(self.actionGreenhouse)
        self.ModelBar.addSeparator()
        self.ModelBar.addAction(self.actionPlay)
        self.ModelBar.addSeparator()
        self.ModelBar.addAction(self.actionGlobalWorkflow)
    
    
    def set_model_2_buttons(self):
        self.ModelBar2 = qt.QToolBar(self)
        self.ModelBar2.setToolButtonStyle(qt.Qt.ToolButtonTextOnly)
        size = qt.QSize(30, 30)
        self.ModelBar2.setIconSize(size)
        self.addToolBar(qt.Qt.TopToolBarArea, self.ModelBar2)    
        
        self.ModelBar2.addAction(self.actionBDD)
        self.ModelBar2.addAction(self.actionPy)
        self.ModelBar2.addAction(self.actionLPy)
        self.ModelBar2.addAction(self.actionWF)
        
        
    
    def set_permanent_editor_buttons(self):
        # set top buttons
        self.CodeBar = qt.QToolBar(self)
        self.CodeBar.setToolButtonStyle(qt.Qt.ToolButtonTextUnderIcon)
        size = qt.QSize(30, 30)
        self.CodeBar.setIconSize(size)
        self.addToolBar(qt.Qt.TopToolBarArea, self.CodeBar)
        self.addToolBarBreak()

        # Shortcuts
        self.actionNew.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+N", None, qt.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+O", None, qt.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+S", None, qt.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(qt.QApplication.translate("MainWindow", "Ctrl+W", None, qt.QApplication.UnicodeUTF8))
        icon0 = qt.QIcon()
        icon0.addPixmap(qt.QPixmap("./resources/new/new.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionNew.setIcon(icon0)
        icon1 = qt.QIcon()
        icon1.addPixmap(qt.QPixmap("./resources/new/open.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        icon2 = qt.QIcon()
        icon2.addPixmap(qt.QPixmap("./resources/new/save.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSaveAs.setIcon(icon2)
        icon2_1 = qt.QIcon()
        icon2_1.addPixmap(qt.QPixmap("./resources/filesaveall.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionSaveAll.setIcon(icon2_1)
        icon4 = qt.QIcon()
        icon4.addPixmap(qt.QPixmap("./resources/fileclose.png"), qt.QIcon.Normal, qt.QIcon.Off)
        self.actionClose.setIcon(icon4)
        

        # connect actions to buttons
        qt.QObject.connect(self.actionNew, qt.SIGNAL('triggered(bool)'),self.new)
        qt.QObject.connect(self.actionOpen, qt.SIGNAL('triggered(bool)'),self.open)
        qt.QObject.connect(self.actionSave, qt.SIGNAL('triggered(bool)'),self.save) 
        qt.QObject.connect(self.actionSaveAll, qt.SIGNAL('triggered(bool)'),self.saveall)
        qt.QObject.connect(self.actionSaveAs, qt.SIGNAL('triggered(bool)'),self.saveas)         
        qt.QObject.connect(self.actionClose, qt.SIGNAL('triggered(bool)'),self.close) 
        qt.QObject.connect(self.textEditorContainer, qt.SIGNAL('tabCloseRequested(int)'),self.autoclose)# Auto-close (red cross)

        self.CodeBar.addAction(self.actionNew)
        self.CodeBar.addAction(self.actionOpen)
        self.CodeBar.addAction(self.actionSave)
        self.CodeBar.addAction(self.actionSaveAll)
        self.CodeBar.addAction(self.actionClose)  
            
    def set_permanent_menu_bar(self):
        self.menubar = qt.QMenuBar()
        self.menubar.setGeometry(qt.QRect(0, 0, 1024, 20))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = qt.QMenu(self.menubar)
        self.menuFile.setTitle(qt.QApplication.translate("MainWindow", "File", None, qt.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName("menuFile")
        
        self.menuRecents = qt.QMenu(self.menuFile)
        self.menuRecents.setTitle(qt.QApplication.translate("MainWindow", "Recents", None, qt.QApplication.UnicodeUTF8))
        self.menuRecents.setObjectName("menuRecents")
        
        self.menuImport = qt.QMenu(self.menuFile)
        self.menuImport.setTitle(qt.QApplication.translate("MainWindow", "Import", None, qt.QApplication.UnicodeUTF8))
        self.menuImport.setObjectName("menuImport")
        
        self.menuEdit = qt.QMenu(self.menubar)
        self.menuEdit.setTitle(qt.QApplication.translate("MainWindow", "Edit", None, qt.QApplication.UnicodeUTF8))
        self.menuEdit.setObjectName("menuEdit")
        
        self.menuHelp = qt.QMenu(self.menubar)
        self.menuHelp.setTitle(qt.QApplication.translate("MainWindow", "Help", None, qt.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName("menuHelp")
        
        self.menuView = qt.QMenu(self.menubar)
        self.menuView.setTitle(qt.QApplication.translate("MainWindow", "View", None, qt.QApplication.UnicodeUTF8))
        self.menuView.setObjectName("menuView")
        
        self.setMenuBar(self.menubar)
        
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionSaveAll)
        self.menuFile.addAction(self.actionClose)
       
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
       
    def set_status_bar(self):   
        # status bar
        self.sizeLabel = qt.QLabel()     
        self.sizeLabel.setFrameStyle(qt.QFrame.StyledPanel|qt.QFrame.Sunken)
        status = self.statusBar()     
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)     
        self.edit_status_bar(message="OALab is ready!", time=10000)   

    def edit_status_bar(self, message, time=10000):   
        self.statusBar().showMessage(message, time)     
        
    def set_local_actions(self):
        try:
            self.local_actions = self.textEditorContainer.currentWidget().set_actions()
        except:
            pass

    def set_local_top_buttons(self):
        try:
            self.remove_local_top_buttons()
        except:
            pass
        try:
            btn_local = self.textEditorContainer.currentWidget().set_buttons(self.local_actions, self)
            self.CodeBar.insertAction(self.actionClose, btn_local)    
        except:
            pass
    
    def remove_local_top_buttons(self):
        actions = self.CodeBar.actions()
        if len(actions)>=5:
            if actions[4] != self.actionClose:
                self.CodeBar.removeAction(actions[4])
        
    def set_local_menu_bar(self):
        try:
            self.remove_local_menu_bar()
        except:
            pass
        try:    
            menu_local = self.textEditorContainer.currentWidget().set_menu(self.menubar, self.local_actions)
            self.menubar.insertAction(self.menuEdit.menuAction(), menu_local)
        except:
            pass    
        
    def remove_local_menu_bar(self):
        actions= self.menubar.actions()
        if actions[1] != self.menuEdit.menuAction():
            self.menubar.removeAction(actions[1])
    
    #----------------------------------------
    # Interpreter
    #----------------------------------------
    def set_shell(self):

        # dock widget => Shell IPython
        self.interpreter = Interpreter()# interpreter
        self.interpreter.locals['history'] = self.history.getHistory()
        self.shellDockWidget = qt.QDockWidget("IPython Shell", self)
        self.shellDockWidget.setObjectName("Shell")
        self.shellDockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.shellDockWidget)
        
        self.shellwdgt = ShellWidget(self.interpreter)
        self.shellwdgt.setMinimumSize(700,150)
        self.shellDockWidget.setWidget(self.shellwdgt)

    def run(self):
        code = self.textEditorContainer.currentWidget().get_text()
        interp = self.get_interpreter()
        interp.runsource(code)
        self.edit_status_bar("Code runned.")
 
    def get_interpreter(self):
        return self.interpreter
        
        
    #----------------------------------------
    # Log
    #----------------------------------------
    def set_log(self):

        # dock widget => Log
        self.logDockWidget = qt.QDockWidget("Log", self)
        self.logDockWidget.setObjectName("Shell")
        self.logDockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea | qt.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.logDockWidget)

        self.logDockWidget.setMinimumSize(150,150)

        
    #----------------------------------------
    # Actions on files
    #----------------------------------------
    def new(self):
        self.show_editors()
        self.show_select_editor()
    
    def open(self, fname=None):
        self.show_editors()
        try:
            try:
                old_id = self.textEditorContainer.currentWidget().ID
                fname = qt.QFileDialog.getOpenFileName(self, 'Open file', self.textEditorContainer.current_path[old_id], "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
            except:
                fname = qt.QFileDialog.getOpenFileName(self, 'Open file', "/home", "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
            f = open(fname, 'r')
            data = f.read()
            # TODO
            fnamesplit = os.path.split(fname)
            fnamesplitext = os.path.splitext(fname)
            f.close()
            self.new_text_editor(name=fnamesplit[1], type=fnamesplitext[1][1:])
            id = self.textEditorContainer.currentWidget().ID
            self.textEditorContainer.current_file_name[id] = fnamesplit[1]
            self.textEditorContainer.current_path_and_fname[id] = fname
            self.textEditorContainer.current_path[id] = fnamesplit[0]
            self.textEditorContainer.current_extension[id] = fnamesplitext[1][1:]
            try:
                self.textEditorContainer.currentWidget().set_text(data.decode("utf8"))#.decode("utf8")#ISO-8859-1
            except:
                self.textEditorContainer.currentWidget().set_text(data)
            self.edit_status_bar(("File '%s' opened.") %self.textEditorContainer.current_file_name[id])
            
            self.textEditorContainer.currentWidget().set_language(self.textEditorContainer.current_extension[id])
        except:
            self.edit_status_bar("No file opened...")

    
    def saveall(self):
        try:
            for _i in range(self.textEditorContainer.count()):
                self.textEditorContainer.setCurrentIndex(_i)
                self.save()
            self.edit_status_bar("All files saved")
        except:
            self.edit_status_bar("All files not saved...")
    
    def save(self):
        if(self.textEditorContainer.tabText(self.textEditorContainer.currentIndex())=="NewFile"):
            self.edit_status_bar("Save as...")
            self.saveas()
        else:
            try:
                code = self.textEditorContainer.currentWidget().get_text() # type(code) = unicode
                id = self.textEditorContainer.currentWidget().ID
                fname = self.textEditorContainer.current_path_and_fname[id]
                # Encode in utf8
                # /!\ 
                # encode("iso-8859-1","ignore") don't know what to do with "\n" and so ignore it
                # encode("utf8","ignore") works well but the read function need decode("utf8")
                code_enc = code.encode("utf8","ignore") #utf8 or iso-8859-1, ignore or replace
                
                # Write text in the file
                f = open(fname, "w")
                f.writelines(code_enc)
                f.close()
                
                fname_without_ext = self.textEditorContainer.current_file_name[id]
                self.edit_status_bar(("File '%s' saved.") %fname_without_ext )
                self.textEditorContainer.setTabText(self.textEditorContainer.currentIndex(), fname_without_ext)
            except:
                self.edit_status_bar("File not saved...") 
    
    def saveas(self):
        try:
            id = self.textEditorContainer.currentWidget().ID
            fname = qt.QFileDialog.getSaveFileName(self, 'Save file', self.textEditorContainer.current_path[id], "Python File(*.py)")
            code = self.textEditorContainer.currentWidget().get_text()
            code_enc = code.encode("utf8","ignore") 
            
            f = open(fname, "w")
            f.writelines(code_enc)
            f.close()
            
            fnamesplit = os.path.split(fname)
            fnamesplitext = os.path.splitext(fname)
            self.textEditorContainer.current_file_name[id] = fnamesplit[1]
            self.textEditorContainer.current_path_and_fname[id] = fname
            self.textEditorContainer.current_path[id] = fnamesplit[0]
            self.textEditorContainer.current_extension[id] = fnamesplitext[1][1:]
            
            fname_without_ext = self.textEditorContainer.current_file_name[id]
            self.edit_status_bar(("File '%s' saved.") % fname_without_ext)
            self.textEditorContainer.setTabText(self.textEditorContainer.currentIndex(), fname_without_ext)
        except:
            self.edit_status_bar("File not saved...")  

    def close(self):       
        try:
            id = self.textEditorContainer.currentWidget().ID
            self.textEditorContainer.removeTab(self.textEditorContainer.currentIndex())
            self.edit_status_bar(("File '%s' closed.") % self.textEditorContainer.current_file_name[id])
        except:
            try:
                self.textEditorContainer.removeTab(self.textEditorContainer.currentIndex())
                self.edit_status_bar("Selector closed.")
            except:    
                self.edit_status_bar("No file closed...")
                
        self.set_local_actions()
        self.set_local_top_buttons()
        self.set_local_menu_bar()

    def autoclose(self, n_tab):
        self.textEditorContainer.setCurrentIndex(n_tab)
        self.close()    
    
def show_splash_screen():
    """Show a small splash screen to make people wait for OpenAleaLab to startup"""
    # import metainfo
    pix = qt.QPixmap("./resources/splash.png")
    splash = qt.QSplashScreen(pix, qt.Qt.WindowStaysOnTopHint)
    splash.show()
    # message = "" + metainfo.get_copyright() +\
              # "Version : %s\n"%(metainfo.get_version(),) +\
              # "Loading modules..."
    message = "Loading..."
    splash.showMessage(message, qt.Qt.AlignCenter|qt.Qt.AlignBottom)
    # -- make sure qt really display the message before importing the modules.--
    qt.QApplication.processEvents()
    return splash

    
def main():
    app = qt.QApplication(sys.argv)
    app.setStyle('plastique')
    MainW = MainWindow()
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()

