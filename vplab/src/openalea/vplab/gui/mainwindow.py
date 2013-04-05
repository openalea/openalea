#---------------------------------------------
# Main Window class
# 
# VPlantsLab GUI is create here
#---------------------------------------------
""" Main Window """


import sys
import os
from openalea.vpltk.qt import qt
from path import path

from openalea.core import settings
from openalea.vplab.scene.view3d import view3D
from openalea.vplab.history.history import History
from openalea.vplab.applets.mapping import map_language
# from openalea.core.logger import get_logger
from openalea.visualea.splitterui import SplittableUI
from openalea.vplab.editor.text_editor import PythonCodeEditor as Editor
from openalea.vplab.editor.text_editor import LPyCodeEditor as LPyEditor
from openalea.vplab.applets.mapping import SelectEditor
from openalea.vpltk.shell.shell import get_shell_class
from openalea.vpltk.shell.shell import get_interpreter_class
from openalea.vpltk.project.project import ProjectManager


# sn_logger = get_logger(__name__)


class MainWindow(qt.QtGui.QMainWindow):
    """
    Main Window Class
    
    .. warning:: In Progress
    """
    def __init__(self, parent=None):
        super(qt.QtGui.QMainWindow, self).__init__(parent)
        
        # -- show the splash screen --
        self.splash = show_splash_screen()   
        
        self.showEditors = False
        
        # self.logger = sn_logger
        
        # window title and icon
        self.setWindowTitle("Virtual Plants Laboratory")
        self.setWindowIcon(qt.QtGui.QIcon("./resources/openalea_icon2.png"))
        
        self.setAttribute(qt.QtCore.Qt.WA_DeleteOnClose)
        self.showMaximized()

        # list of central widgets
        self.widList = []
        self.current_mode = None
        
        # project
        # list of opened projects
        self.projects = {}
        self.projectManager = ProjectManager()
        
        # editor
        self.set_text_editor_container()
        # self.hide_editors()
        
        # Central widgets
        # self.splittable = SplittableUI(parent=self, content=self.VW)
        # Virtual World
        self.set_virtual_world()
        
        # self.splittable.splitPane(content=self.widList[1], paneId=0, direction=qt.QtCore.Qt.Horizontal, amount=0.8)
        self.set_central_widget(1,1)
        # self.setCentralWidget(self.splittable)
        
        # Other widgets
        # Ressources
        self.set_world_manager()
        # Packages
        # self.set_package_manager()
        
        # control panel
        self.set_control_panel()
        # observation panel
##        self.set_observation_panel()
        # tabify control and observation panels
##        self.tabifyDockWidget(self.controlDockWidget, self.obsDockWidget)
        
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
        # Menu Bar
        self.set_permanent_menu_bar()
        # Actions bars and buttons
        self.set_buttons_level_one()
        
        self.set_model_actions()
        self.set_model_buttons()
        # self.set_model_2_actions()
        # self.set_model_2_buttons()

        

##        self.openProj(name='demo_lpy_noise_branche')        

        self.splash.finish(self)
    #----------------------------------------
    # Setup Central Widget
    #----------------------------------------        
    def set_central_widget(self, row, column):
        # pass
        # self.__centralStack.addWidget(wid)
        
        layout = qt.QtGui.QGridLayout()
        self.central = qt.QtGui.QWidget()
        self.central.setMinimumSize(200, 200)
        
        l = len(self.widList)
        
        # Fill central Widget in a layout
        i=0
        for x in range(row):
            for y in range(column):
                if i < l:
                    wid = self.widList[i]
                # if they are more panels than widgets in widgList
                else:
                    wid = qt.QtGui.QWidget()
                
                try:
                    wid.setMinimumSize(100,100) 
                except:
                    pass
  
                layout.addWidget(wid, x, y)
                i += 1
        
        # If they are too many widgets, they are add (in new lines)
        if l > i:
            for w in self.widList[i:]:
                layout.addWidget(w)

        
        self.central.setLayout(layout)

        self.setCentralWidget(self.central)  
        

        
 
    #----------------------------------------
    # Setup Virtual World
    #----------------------------------------
    def set_virtual_world(self):
        self.history = History()
    
        view = view3D(parent=self)
        view.setObjectName("view3D")
        
        view.start()    
        
        self.VW = view
        # self.VW.setMinimumSize(500, 500)
        
        self.widList.append(self.VW)
        
        # Connect the scene3D (self.VW) to the history list (self.history)
        self.actionHistoryList = qt.QtGui.QAction(self)
        qt.QtCore.QObject.connect(self.history.obj, qt.QtCore.SIGNAL('HistoryChanged'),self.VW.setScene)
        qt.QtCore.QObject.connect(self.history.obj, qt.QtCore.SIGNAL('HistoryChanged'),self.update_ressources_manager)
        
    def add_virtual_world_viewer(self):
        print "This action doens't work for the moment('new virtual world viewer')."
        pass
        # view = view3D(scene=self.VW.getScene(),parent=self,shareWidget=self.VW)
        # view.start()
        # self.widList.append(view)
        # self.splittable.splitPane(content=self.widList[2], paneId=0, direction=qt.QtCore.Qt.Vertical, amount=0.8)
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
    def set_world_manager(self):
        # Ressources
        self.ressManaWid = qt.QtGui.QTableWidget(0,2)       
        self.ressManaWid.setMinimumSize(100, 100)

        self.ressManaDockWidget = qt.QtGui.QDockWidget("Virtual World", self)
        self.ressManaDockWidget.setObjectName("RessMana")
        self.ressManaDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea)
        self.ressManaDockWidget.setWidget(self.ressManaWid)
        self.addDockWidget(qt.QtCore.Qt.RightDockWidgetArea, self.ressManaDockWidget) 
        
        hist = self.history.getHistory()
        self.update_ressources_manager(hist)
        
    def reset_world_manager(self):
        self.ressManaWid.clear()
        headerName1 = qt.QtGui.QTableWidgetItem("name")
        headerName2 = qt.QtGui.QTableWidgetItem("value")
        self.ressManaWid.setHorizontalHeaderItem(0,headerName1)
        self.ressManaWid.setHorizontalHeaderItem(1,headerName2)
        
    def update_ressources_manager(self, scene):
        self.reset_world_manager()
        row = 0
        for h in scene:
            itemName = qt.QtGui.QTableWidgetItem(str(h))
            itemObj = qt.QtGui.QTableWidgetItem(str(scene[h]))
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
        self.packManaWid = qt.QtGui.QWidget()
        self.packManaWid.setMinimumSize(100, 100)
        # self.packManaWid.setMaximumSize(400, 400)

        self.packManaDockWidget = qt.QtGui.QDockWidget("Package Manager", self)
        self.packManaDockWidget.setObjectName("RessMana")
        self.packManaDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea)
        self.packManaDockWidget.setWidget(self.packManaWid)
        self.addDockWidget(qt.QtCore.Qt.LeftDockWidgetArea, self.packManaDockWidget)     
        
    
    #----------------------------------------
    # Setup Help Dock Widget
    #----------------------------------------
    def set_help(self):
    
        # Help
        self.helpWid = qt.QtGui.QWidget()
        self.helpWid.setMinimumSize(150, 150)
        # self.helpWid.setMaximumSize(400, 400)

        self.helpDockWidget = qt.QtGui.QDockWidget("Help", self)
        self.helpDockWidget.setObjectName("Help")
        self.helpDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea)
        self.helpDockWidget.setWidget(self.helpWid)
        self.addDockWidget(qt.QtCore.Qt.BottomDockWidgetArea, self.helpDockWidget)         
    
    
    
    #----------------------------------------
    # Setup Control Panel Dock Widget
    #----------------------------------------
    def set_control_panel(self):
        """ Set the control panel
        Only once by project!
        """        
        # Create widget control panel
        self.controlWid = qt.QtGui.QTableWidget(0,3)
        self.reset_control_panel()
        self.controlWid.setMinimumSize(50, 50) 
        self.controlDockWidget = qt.QtGui.QDockWidget("Control Panel", self)
        self.controlDockWidget.setObjectName("ControlPanel")
        self.controlDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea | qt.QtCore.Qt.BottomDockWidgetArea)
        self.controlDockWidget.setWidget(self.controlWid)
        self.addDockWidget(qt.QtCore.Qt.BottomDockWidgetArea, self.controlDockWidget)   

        qt.QtCore.QObject.connect(self.controlWid, qt.QtCore.SIGNAL('itemChanged(QTableWidgetItem *)'),self.edit_control)   

    def edit_control(self, item):
        row = item.row()
        column = item.column()
        
        try:
            name = self.controlWid.item(row,0).text()
            value = self.controlWid.item(row,1).text()
            filename = self.controlWid.item(row,2).text()
            
            if column == 0:
                # TODO
                # Delete old control "name"
                self.current_project.controls[filename][name] = eval(value)
            elif column == 1:
                self.current_project.controls[filename][name] = eval(value)
            elif column == 2:
                # TODO
                # Delete old control "filename"
                self.current_project.controls[filename][name] = eval(value)        

            ctrl = self.current_project.controls[filename]
            self.interpreter.user_ns.update(ctrl)
        
        except:
            pass
        
    def add_control(self, controle_filename, controle_name, controle_value):
        """
        Add one Control in the widget control panel.
        
        :param controle_filename: file name where the control is saved
        :param controle_name: name of the control
        :param controle_value: value of the control
        """
        row = self.controlWid.rowCount()
        self.controlWid.insertRow(row)
        self.controlWid.setItem(row,0,qt.QtGui.QTableWidgetItem(str(controle_name)))
        self.controlWid.setItem(row,1,qt.QtGui.QTableWidgetItem(str(controle_value)))
        self.controlWid.setItem(row,2,qt.QtGui.QTableWidgetItem(str(controle_filename)))
        
    def set_controls(self, controls):
        """
        Set Control from the applet in the control manager and the widget control panel.
        
        :param controls: dict of the controls to set
        """
        self.reset_control_panel()
        # Add new controls in control manager
        for filename in controls:
            for name in eval(str(controls[filename])):
                new_control = eval(str(controls[filename]))[name] 
                self.add_control(filename,name,new_control) 

    def reset_control_panel(self):
        """Clear the control panel and set the headers.
        """
        self.controlWid.clear()
        headerName0 = qt.QtGui.QTableWidgetItem("object")
        headerName1 = qt.QtGui.QTableWidgetItem("value")
        headerName2 = qt.QtGui.QTableWidgetItem("file name")
        self.controlWid.setHorizontalHeaderItem(0,headerName0)
        self.controlWid.setHorizontalHeaderItem(1,headerName1)
        self.controlWid.setHorizontalHeaderItem(2,headerName2)
    
    #----------------------------------------
    # Setup Observation Panel Dock Widget
    #----------------------------------------
    def set_observation_panel(self):
    
        # Help
        self.obsWid = qt.QtGui.QLabel("number of leafs : 42000")
        self.obsWid.setMinimumSize(50, 50)

        self.obsDockWidget = qt.QtGui.QDockWidget("Observation Panel", self)
        self.obsDockWidget.setObjectName("ObservationPanel")
        self.obsDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea | qt.QtCore.Qt.BottomDockWidgetArea)
        self.obsDockWidget.setWidget(self.obsWid)
        self.addDockWidget(qt.QtCore.Qt.BottomDockWidgetArea, self.obsDockWidget) 

        
    #----------------------------------------
    # Setup Editor Container Dock Widget
    #----------------------------------------
    def set_text_editor_container(self):
        # Editor
        self.textEditorContainer = qt.QtGui.QTabWidget()
        self.textEditorContainer.max_ID = 0
        self.textEditorContainer.current_file_name = [None]
        self.textEditorContainer.current_extension = [None]
        self.textEditorContainer.current_path_and_fname = [None]
        self.textEditorContainer.current_path = [None]
        self.textEditorContainer.setTabsClosable(True)
        self.textEditorContainer.setMinimumSize(200, 200)
        self.textEditorContainer.setMaximumSize(1000, 1000)
        
        self.editDockWidget = qt.QtGui.QDockWidget("Editor", self)
        self.editDockWidget.setObjectName("Editor")
        self.editDockWidget.setAllowedAreas(qt.QtCore.Qt.LeftDockWidgetArea | qt.QtCore.Qt.RightDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea | qt.QtCore.Qt.BottomDockWidgetArea)
        self.editDockWidget.setWidget(self.textEditorContainer)
        
        # self.widList.append(self.textEditorContainer)
        self.new()
        
        # Bar of Editor: instanciate self.CodeBar
        self.set_editor_actions()
        self.set_permanent_editor_buttons()
        
        # Add Dock Widget
        self.addDockWidget(qt.QtCore.Qt.LeftDockWidgetArea, self.editDockWidget)
        self.editDockWidget.setTitleBarWidget( self.CodeBar )
            
    def update_text_editor(self):
        """
        Clear the text editor container and set in tab
        script from current project.
        """        
        self.textEditorContainer.clear()
        for script in self.current_project.scripts:
            language = str(script).split('.')[-1]
            Editor = map_language(language)
            edit = Editor()
            edit.set_text(self.current_project.scripts[script])
            self.textEditorContainer.addTab(edit, str(script))
            self.setup_new_tab()            

            
            
    def new_text_editor(self, name="NewFile", type="python"):
        if(self.textEditorContainer.tabText(self.textEditorContainer.currentIndex())=="Select your editor type"):
            self.textEditorContainer.removeTab(self.textEditorContainer.currentIndex())
        
        widget = map_language(language=type)  
        
        self.editorWidget = widget(parent=self)
        self.textEditorContainer.addTab(self.editorWidget, name)
        self.textEditorContainer.setCurrentWidget(self.editorWidget)
        self.setup_new_tab()

##        applet, widget = map_language(language=type)  
##        
##        self.editorWidget = widget(parent=self)
##        try: appl = applet(parent=self)
##        except: appl = applet()
##        self.editorWidget.appl = appl
##        
##        self.textEditorContainer.addTab(self.editorWidget, name)
##        self.textEditorContainer.setCurrentWidget(self.editorWidget)
##        self.setup_new_tab()
##
##        try: appl.controls()
##        except: print("can\'t get controls from %s" %appl) 
##        
##        try: self.set_controls(appl.controls())
##        except: print("can\'t set controls from %s in application" %appl)
    
    def show_select_editor(self, name="Select your editor type"):
        """
        Display a widget for select the editor type
        
        :param name: string that you want to display as widget title
        """
        self.selectEditor = SelectEditor(parent=self)
        self.textEditorContainer.addTab(self.selectEditor, name)
        self.textEditorContainer.setCurrentWidget(self.selectEditor)
        # self.add_widget(self.selectEditor)
    
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
    def set_button_change_project(self):
        menu = CustomMenu(self.projects, self)  
        self.current_project_button.setMenu(menu)
    
    def set_buttons_level_one(self):
        # Create actions

        self.actionFile = qt.QtGui.QAction(self)
        self.actionEdit = qt.QtGui.QAction(self)
        self.actionView = qt.QtGui.QAction(self)
        self.actionHelp = qt.QtGui.QAction(self)
        self.actionInit = qt.QtGui.QAction(self)
        self.actionSimu = qt.QtGui.QAction(self)
        self.actionExp = qt.QtGui.QAction(self)

        self.current_project_button = qt.QtGui.QPushButton(self)
        
        self.current_project_label = qt.QtGui.QLabel(self)

        # Set title of buttons       
        self.actionFile.setText(qt.QtGui.QApplication.translate("MainWindow", "File", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(qt.QtGui.QApplication.translate("MainWindow", "Edit", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionView.setText(qt.QtGui.QApplication.translate("MainWindow", "View", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(qt.QtGui.QApplication.translate("MainWindow", "Help", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionInit.setText(qt.QtGui.QApplication.translate("MainWindow", "Initialisation", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSimu.setText(qt.QtGui.QApplication.translate("MainWindow", "Simulation", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionExp.setText(qt.QtGui.QApplication.translate("MainWindow", "Exporation", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.current_project_button.setText(qt.QtGui.QApplication.translate("MainWindow", "Select Project", None, qt.QtGui.QApplication.UnicodeUTF8))
    
        self.LevelOneBar = qt.QtGui.QToolBar(self)
        self.LevelOneBar.setToolButtonStyle(qt.QtCore.Qt.ToolButtonTextUnderIcon)
        size = qt.QtCore.QSize(30, 30)
        self.LevelOneBar.setIconSize(size)
        self.addToolBar(qt.QtCore.Qt.TopToolBarArea, self.LevelOneBar) 
##        self.addToolBarBreak()
        
        icon0 = qt.QtGui.QIcon()
        icon0.addPixmap(qt.QtGui.QPixmap("./resources/new/axiom2.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionInit.setIcon(icon0)
        icon1 = qt.QtGui.QIcon()
        icon1.addPixmap(qt.QtGui.QPixmap("./resources/new/growth2.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionSimu.setIcon(icon1)
        icon2 = qt.QtGui.QIcon()
        icon2.addPixmap(qt.QtGui.QPixmap("./resources/new/analysis.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionExp.setIcon(icon2)

        # connect actions to buttons
        # qt.QtCore.QObject.connect(self.actionInit, qt.QtCore.SIGNAL('triggered(bool)'),self.set_central_widget11)
        # qt.QtCore.QObject.connect(self.actionSimu, qt.QtCore.SIGNAL('triggered(bool)'),self.set_central_widget12)
        # qt.QtCore.QObject.connect(self.actionExp, qt.QtCore.SIGNAL('triggered(bool)'),self.add_virtual_world_viewer) 
        
        # self.LevelOneBar.addAction(self.actionFile)
        # self.LevelOneBar.addAction(self.actionEdit)
        # self.LevelOneBar.addAction(self.actionView)
        # self.LevelOneBar.addAction(self.actionHelp)
        # self.LevelOneBar.addSeparator()
        self.LevelOneBar.addAction(self.actionInit)
        self.LevelOneBar.addSeparator()
        self.LevelOneBar.addAction(self.actionSimu)   
        self.LevelOneBar.addSeparator()        
        self.LevelOneBar.addAction(self.actionExp)
        self.LevelOneBar.addSeparator()
        self.LevelOneBar.addWidget(self.current_project_label)
        self.LevelOneBar.addSeparator()
        self.LevelOneBar.addWidget(self.current_project_button)
        self.LevelOneBar.addSeparator()
    
    def update_current_project_label(self):
        text = 'current project:\n\n"%s"' %self.current_project.name
        self.current_project_label.setText(text)
    
    def change_current_mode(self, mode=None):
        self.current_mode = mode
    
    def set_buttons_level_two(self):
        self.delete_buttons_level_two()
        if self.current_mode == "init":
            self.set_buttons_init()
        elif self.current_mode == "simu":
            self.set_buttons_simu()
        elif self.current_mode == "expl":
            self.set_buttons_expl()
        else:
            pass
            
    
    def delete_buttons_level_two(self):
        pass
    
        self.LevelTwoBar.clear()
        
    # def set_buttons_level_three(self):
        # pass
    
    # def delete_buttons_level_three(self):
        # pass    
    
    def set_model_actions(self):
        # Create actions
        self.actionAddPlant = qt.QtGui.QAction(self)
        self.actionPlantGrowing = qt.QtGui.QAction(self)
        
        self.actionSoil = qt.QtGui.QAction(self)
        self.actionSky = qt.QtGui.QAction(self)
        self.actionGreenhouse = qt.QtGui.QAction(self)
        
        self.actionPlay= qt.QtGui.QAction(self)
        
        self.actionGlobalWorkflow= qt.QtGui.QAction(self)
                
        # Set title of buttons       
        self.actionAddPlant.setText(qt.QtGui.QApplication.translate("MainWindow", "Plant", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionPlantGrowing.setText(qt.QtGui.QApplication.translate("MainWindow", "Plant Growth", None, qt.QtGui.QApplication.UnicodeUTF8))
        
        self.actionSoil.setText(qt.QtGui.QApplication.translate("MainWindow", "Soil", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSky.setText(qt.QtGui.QApplication.translate("MainWindow", "Weather", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionGreenhouse.setText(qt.QtGui.QApplication.translate("MainWindow", "Greenhouse", None, qt.QtGui.QApplication.UnicodeUTF8))
            
        self.actionPlay.setText(qt.QtGui.QApplication.translate("MainWindow", "Run", None, qt.QtGui.QApplication.UnicodeUTF8))
        
        self.actionGlobalWorkflow.setText(qt.QtGui.QApplication.translate("MainWindow", "Global Workflow", None, qt.QtGui.QApplication.UnicodeUTF8))

    def set_model_2_actions(self):
        # Create actions
        self.actionBDD = qt.QtGui.QAction(self)
        self.actionPy = qt.QtGui.QAction(self)
        self.actionLPy = qt.QtGui.QAction(self)
        self.actionWF = qt.QtGui.QAction(self)

                
        # Set title of buttons       
        self.actionBDD.setText(qt.QtGui.QApplication.translate("MainWindow", "From DataBase", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionPy.setText(qt.QtGui.QApplication.translate("MainWindow", "From Python", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionLPy.setText(qt.QtGui.QApplication.translate("MainWindow", "From LPy", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionWF.setText(qt.QtGui.QApplication.translate("MainWindow", "From Workflow", None, qt.QtGui.QApplication.UnicodeUTF8))

    
        
    def set_editor_actions(self):
        # Create actions
        self.actionNew = qt.QtGui.QAction(self)
        self.actionOpen = qt.QtGui.QAction(self)
        self.actionSave = qt.QtGui.QAction(self)
        self.actionSaveAll = qt.QtGui.QAction(self)
        self.actionSaveAs = qt.QtGui.QAction(self)
        self.actionClose = qt.QtGui.QAction(self)

        # Set title of buttons
        self.actionNew.setText(qt.QtGui.QApplication.translate("MainWindow", "New", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(qt.QtGui.QApplication.translate("MainWindow", "Open", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(qt.QtGui.QApplication.translate("MainWindow", "Save", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAll.setText(qt.QtGui.QApplication.translate("MainWindow", "Save All", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(qt.QtGui.QApplication.translate("MainWindow", "Save As", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(qt.QtGui.QApplication.translate("MainWindow", "Close", None, qt.QtGui.QApplication.UnicodeUTF8))

    def set_model_buttons(self):
        self.ModelBar = qt.QtGui.QToolBar(self)
        self.ModelBar.setToolButtonStyle(qt.QtCore.Qt.ToolButtonTextUnderIcon)
        size = qt.QtCore.QSize(30, 30)
        self.ModelBar.setIconSize(size)
        self.addToolBar(qt.QtCore.Qt.TopToolBarArea, self.ModelBar)
        self.addToolBarBreak()        
        
        icon2_2 = qt.QtGui.QIcon()
        icon2_2.addPixmap(qt.QtGui.QPixmap("./resources/new/plant.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionAddPlant.setIcon(icon2_2)
        icon2_3 = qt.QtGui.QIcon()
        icon2_3.addPixmap(qt.QtGui.QPixmap("./resources/new/grow.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionPlantGrowing.setIcon(icon2_3)
        icon5 = qt.QtGui.QIcon()
        icon5.addPixmap(qt.QtGui.QPixmap("./resources/new/soil.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionSoil.setIcon(icon5)
        icon6 = qt.QtGui.QIcon()
        icon6.addPixmap(qt.QtGui.QPixmap("./resources/new/sky.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionSky.setIcon(icon6)
        icon7 = qt.QtGui.QIcon()
        icon7.addPixmap(qt.QtGui.QPixmap("./resources/new/greenhouse.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionGreenhouse.setIcon(icon7)       
        icon2_4 = qt.QtGui.QIcon()
        icon2_4.addPixmap(qt.QtGui.QPixmap("./resources/new/play.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionPlay.setIcon(icon2_4)
        icon1 = qt.QtGui.QIcon()
        icon1.addPixmap(qt.QtGui.QPixmap("./resources/new/workflow.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionGlobalWorkflow.setIcon(icon1)
        
        # connect actions to buttons
        # qt.QtCore.QObject.connect(self.actionAddPlant, qt.QtCore.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QtCore.QObject.connect(self.actionPlantGrowing, qt.QtCore.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QtCore.QObject.connect(self.actionSoil, qt.QtCore.SIGNAL('triggered(bool)'),self.set_text_editor_container) 
        # qt.QtCore.QObject.connect(self.actionSky, qt.QtCore.SIGNAL('triggered(bool)'),self.set_text_editor_container)
        # qt.QtCore.QObject.connect(self.actionGreenhouse, qt.QtCore.SIGNAL('triggered(bool)'),self.set_text_editor_container)         
        # qt.QtCore.QObject.connect(self.actionPlay, qt.QtCore.SIGNAL('triggered(bool)'),self.play) 
        # qt.QtCore.QObject.connect(self.actionGlobalWorkflow, qt.QtCore.SIGNAL('triggered(bool)'),self.globalWorkflow) 
        
        qt.QtCore.QObject.connect(self.actionSoil, qt.QtCore.SIGNAL('triggered(bool)'),self.add_soil)
        qt.QtCore.QObject.connect(self.actionAddPlant, qt.QtCore.SIGNAL('triggered(bool)'),self.add_plant)
        qt.QtCore.QObject.connect(self.actionSky, qt.QtCore.SIGNAL('triggered(bool)'),self.add_sun)
        
        self.ModelBar.addAction(self.actionAddPlant)
        # self.ModelBar.addAction(self.actionPlantGrowing)
        # self.ModelBar.addSeparator()
        self.ModelBar.addAction(self.actionSoil)
        self.ModelBar.addAction(self.actionSky)
        self.ModelBar.addAction(self.actionGreenhouse)
        # self.ModelBar.addSeparator()
        # self.ModelBar.addAction(self.actionPlay)
        # self.ModelBar.addSeparator()
        # self.ModelBar.addAction(self.actionGlobalWorkflow)
    
    set_buttons_init = set_model_buttons
    
    def set_buttons_simu(self):
        pass
        
    def set_buttons_expl(self):
        pass
    
    def set_model_2_buttons(self):
        self.ModelBar2 = qt.QtGui.QToolBar(self)
        self.ModelBar2.setToolButtonStyle(qt.QtCore.Qt.ToolButtonTextOnly)
        size = qt.QtCore.QSize(30, 30)
        self.ModelBar2.setIconSize(size)
        self.addToolBar(qt.QtCore.Qt.TopToolBarArea, self.ModelBar2)    
        
        self.ModelBar2.addAction(self.actionBDD)
        self.ModelBar2.addAction(self.actionPy)
        self.ModelBar2.addAction(self.actionLPy)
        self.ModelBar2.addAction(self.actionWF)
        
        
    
    def set_permanent_editor_buttons(self):
        # set top buttons
        self.CodeBar = qt.QtGui.QToolBar(self)
        self.CodeBar.setToolButtonStyle(qt.QtCore.Qt.ToolButtonTextUnderIcon)
        size = qt.QtCore.QSize(30, 30)
        self.CodeBar.setIconSize(size)
        self.addToolBar(qt.QtCore.Qt.TopToolBarArea, self.CodeBar)
        self.addToolBarBreak()

        # Shortcuts
        self.actionNew.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(qt.QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, qt.QtGui.QApplication.UnicodeUTF8))
        icon0 = qt.QtGui.QIcon()
        icon0.addPixmap(qt.QtGui.QPixmap("./resources/new/new.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionNew.setIcon(icon0)
        icon1 = qt.QtGui.QIcon()
        icon1.addPixmap(qt.QtGui.QPixmap("./resources/new/open.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        icon2 = qt.QtGui.QIcon()
        icon2.addPixmap(qt.QtGui.QPixmap("./resources/new/save.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSaveAs.setIcon(icon2)
        icon2_1 = qt.QtGui.QIcon()
        icon2_1.addPixmap(qt.QtGui.QPixmap("./resources/filesaveall.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionSaveAll.setIcon(icon2_1)
        icon4 = qt.QtGui.QIcon()
        icon4.addPixmap(qt.QtGui.QPixmap("./resources/fileclose.png"), qt.QtGui.QIcon.Normal, qt.QtGui.QIcon.Off)
        self.actionClose.setIcon(icon4)
        

        # connect actions to buttons
        qt.QtCore.QObject.connect(self.actionNew, qt.QtCore.SIGNAL('triggered(bool)'),self.new)
        qt.QtCore.QObject.connect(self.actionOpen, qt.QtCore.SIGNAL('triggered(bool)'),self.open)
        qt.QtCore.QObject.connect(self.actionSave, qt.QtCore.SIGNAL('triggered(bool)'),self.save) 
        qt.QtCore.QObject.connect(self.actionSaveAll, qt.QtCore.SIGNAL('triggered(bool)'),self.saveall)
        qt.QtCore.QObject.connect(self.actionSaveAs, qt.QtCore.SIGNAL('triggered(bool)'),self.saveas)         
        qt.QtCore.QObject.connect(self.actionClose, qt.QtCore.SIGNAL('triggered(bool)'),self.close) 
        qt.QtCore.QObject.connect(self.textEditorContainer, qt.QtCore.SIGNAL('tabCloseRequested(int)'),self.autoclose)# Auto-close (red cross)

        self.CodeBar.addAction(self.actionNew)
        self.CodeBar.addAction(self.actionOpen)
        self.CodeBar.addAction(self.actionSave)
        self.CodeBar.addAction(self.actionSaveAll)
        self.CodeBar.addAction(self.actionClose)  
            
    def set_permanent_menu_bar(self):
        self.menubar = qt.QtGui.QMenuBar(self)
        self.menubar.setGeometry(qt.QtCore.QRect(0, 0, 1024, 20))
        self.menubar.setObjectName("menubar")
        
        self.menuProj = qt.QtGui.QMenu(self.menubar)
        self.menuProj.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Project", None, qt.QtGui.QApplication.UnicodeUTF8))  
        self.menuProj.setObjectName("menuProj")
        
        self.menuFile = qt.QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(qt.QtGui.QApplication.translate("MainWindow", "File", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName("menuFile")
        
        self.menuRecents = qt.QtGui.QMenu(self.menuFile)
        self.menuRecents.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Recents", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuRecents.setObjectName("menuRecents")
        
        self.menuImport = qt.QtGui.QMenu(self.menuFile)
        self.menuImport.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Import", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuImport.setObjectName("menuImport")
        
        self.menuEdit = qt.QtGui.QMenu(self.menubar)
        self.menuEdit.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Edit", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setObjectName("menuEdit")
        
        self.menuHelp = qt.QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(qt.QtGui.QApplication.translate("MainWindow", "Help", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName("menuHelp")
        
        self.menuView = qt.QtGui.QMenu(self.menubar)
        self.menuView.setTitle(qt.QtGui.QApplication.translate("MainWindow", "View", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.menuView.setObjectName("menuView")
        
        self.setMenuBar(self.menubar)       
        
        self.actionNewProj = qt.QtGui.QAction(self)
        self.actionOpenProj = qt.QtGui.QAction(self)
        self.actionSaveProj = qt.QtGui.QAction(self)
        self.actionSaveAllProj = qt.QtGui.QAction(self)
        self.actionCloseProj = qt.QtGui.QAction(self)
        self.actionChangeActiveProj = qt.QtGui.QAction(self)
        
        self.actionNewProj.setText(qt.QtGui.QApplication.translate("MainWindow", "New Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj.setText(qt.QtGui.QApplication.translate("MainWindow", "Open Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj.setText(qt.QtGui.QApplication.translate("MainWindow", "Save Current Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj.setText(qt.QtGui.QApplication.translate("MainWindow", "Close Current Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAllProj.setText(qt.QtGui.QApplication.translate("MainWindow", "Save All Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.actionChangeActiveProj.setText(qt.QtGui.QApplication.translate("MainWindow", "Change Current Project", None, qt.QtGui.QApplication.UnicodeUTF8))
        
        qt.QtCore.QObject.connect(self.actionNewProj, qt.QtCore.SIGNAL('triggered(bool)'),self.newProj)
        qt.QtCore.QObject.connect(self.actionOpenProj, qt.QtCore.SIGNAL('triggered(bool)'),self.openProj)
        qt.QtCore.QObject.connect(self.actionSaveProj, qt.QtCore.SIGNAL('triggered(bool)'),self.saveProj)
        qt.QtCore.QObject.connect(self.actionSaveAllProj, qt.QtCore.SIGNAL('triggered(bool)'),self.saveAllProj)
        qt.QtCore.QObject.connect(self.actionCloseProj, qt.QtCore.SIGNAL('triggered(bool)'),self.closeProj)
        qt.QtCore.QObject.connect(self.actionChangeActiveProj, qt.QtCore.SIGNAL('triggered(bool)'),self.changeActiveProj)
        
        self.menuProj.addAction(self.actionNewProj)
        self.menuProj.addAction(self.actionOpenProj)
        self.menuProj.addAction(self.actionSaveProj)
        self.menuProj.addAction(self.actionSaveAllProj)
        self.menuProj.addAction(self.actionCloseProj)
        self.menuProj.addAction(self.actionChangeActiveProj)  

        # self.menuFile.addAction(self.actionNew)
        # self.menuFile.addAction(self.actionOpen)
        # self.menuFile.addAction(self.actionSave)
        # self.menuFile.addAction(self.actionSaveAs)
        # self.menuFile.addAction(self.actionSaveAll)
        # self.menuFile.addAction(self.actionClose)
       
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProj.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
       
    def set_status_bar(self):   
        # status bar
        self.sizeLabel = qt.QtGui.QLabel()     
        self.sizeLabel.setFrameStyle(qt.QtGui.QFrame.StyledPanel|qt.QtGui.QFrame.Sunken)
        status = self.statusBar()     
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)     
        self.edit_status_bar(message="VPLab is ready!", time=10000)   

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
        pass
##        try:
##            self.remove_local_menu_bar()
##        except:
##            pass
##        try:    
##            menu_local = self.textEditorContainer.currentWidget().set_menu(self.menubar, self.local_actions)
##            self.menubar.insertAction(self.menuEdit.menuAction(), menu_local)
##        except:
##            pass    
        
    def remove_local_menu_bar(self):
        actions= self.menubar.actions()
        if actions[1] != self.menuEdit.menuAction():
            self.menubar.removeAction(actions[1])
    
    #----------------------------------------
    # Interpreter
    #----------------------------------------
    def set_shell(self):

        # dock widget => Shell IPython
        InterpreterClass = get_interpreter_class()
        self.interpreter = InterpreterClass()# interpreter
        self.interpreter.locals['world'] = self.history.getHistory()
        self.interpreter.locals['projects'] = self.projects
        # self.interpreter.runcode("print('yep')")

        self.shellDockWidget = qt.QtGui.QDockWidget("Python Shell", self)     
            
        self.shellDockWidget.setObjectName("Shell")
        self.shellDockWidget.setAllowedAreas(qt.QtCore.Qt.BottomDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.QtCore.Qt.BottomDockWidgetArea, self.shellDockWidget)
        
        
        ShellClass = get_shell_class()
        self.shellwdgt = ShellClass(self.interpreter)
        self.shellwdgt.setMinimumSize(700,150)
        self.shellDockWidget.setWidget(self.shellwdgt)

##    def run(self):
##        self.textEditorContainer.currentWidget().appl.run()
        # 123456
        # code = self.textEditorContainer.currentWidget().get_text()
        # interp = self.get_interpreter()
        # interp.runsource(code)
        # self.edit_status_bar("Code runned.")
 
    def get_interpreter(self):
        return self.interpreter
        
        
    #----------------------------------------
    # Log
    #----------------------------------------
    def set_log(self):

        # dock widget => Log
        self.logDockWidget = qt.QtGui.QDockWidget("Log", self)
        self.logDockWidget.setObjectName("Shell")
        self.logDockWidget.setAllowedAreas(qt.QtCore.Qt.BottomDockWidgetArea | qt.QtCore.Qt.TopDockWidgetArea)
        self.addDockWidget(qt.QtCore.Qt.BottomDockWidgetArea, self.logDockWidget)

        self.logDockWidget.setMinimumSize(150,150)

    #----------------------------------------
    # Actions on project
    #----------------------------------------
    def newProj(self):
        proj = self.projectManager.create('unamed_project')
        self.projects[proj.name] = proj
        self.project_change(proj.name)
       
    def openProj(self, name=False):
        if name is False:
            name = self.showOpenFileDialog()
        if name is not u'':
            proj_name = name.split('/')[-1]
            proj = self.projectManager[proj_name]
            self.projects[proj.name] = proj
            self.project_change(proj.name)
            
    def saveProj(self):
        self.saveall()#text editor
        self.current_project.save()
        self.project_changed() 

    def saveAllProj(self):
        # todo
        for proj in self.projects:
            self.projects[proj].save()
        self.project_changed()

    def closeProj(self):
        name = self.current_project.name
        del self.projects[name]
        for pname in self.projects:
            self.current_project = self.projects[pname]
        self.project_changed()
        
    def changeActiveProj(self):
        pass
    
    def project_change(self, name):
        if hasattr(self, 'current_project'):
            if name is not self.current_project.name:
                # Get project
                self.current_project = self.projects[name]
                # Get the world
                self.history.reset()
##                for w in self.current_project.world:
##                    self.history.add(w,world[w])
                # Get controls
                controls = self.current_project.controls
                self.set_controls(controls)
                
                self.interpreter.user_ns = self.current_project.ns

                self.project_changed()
        else:
            # If this is the first project
            self.current_project = self.projects[name]
            self.history.reset()
##            for w in self.current_project.world:
##                self.history.add(w,self.current_project.world[w])

            controls = self.current_project.controls

            self.set_controls(controls)
            
            self.interpreter.user_ns = self.current_project.ns
            
            self.project_changed()
        
    def project_changed(self):    
        self.set_button_change_project()
        self.update_text_editor()
        self.update_current_project_label()
        
    #----------------------------------------
    # Dialog
    #----------------------------------------        
    def showOpenFileDialog(self):
        my_path = path(settings.get_project_dir())
        fname = qt.QtGui.QFileDialog.getExistingDirectory(self, 'Select Project Directory', 
                my_path)
        return fname
        
    #----------------------------------------
    # Actions on files
    #----------------------------------------
    def new(self):
        self.show_select_editor()
    
    def open(self, fname=None):
        pass
##        self.textEditorContainer.currentWidget().appl.open(fname)
        # 123456
        '''
        self.show_editors()
        try:
            try:
                old_id = self.textEditorContainer.currentWidget().ID
                fname = qt.QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.textEditorContainer.current_path[old_id], "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
            except:
                fname = qt.QtGui.QFileDialog.getOpenFileName(self, 'Open file', "/home", "Python or L-Py File (*.py *.lpy);;Any file(*.*)")
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
        '''
    
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
                fname = self.textEditorContainer.tabText(self.textEditorContainer.currentIndex())
                # Encode in utf8
                # /!\ 
                # encode("iso-8859-1","ignore") don't know what to do with "\n" and so ignore it
                # encode("utf8","ignore") works well but the read function need decode("utf8")
##                code_enc = code.encode("utf8","ignore") #utf8 or iso-8859-1, ignore or replace
                
                # Write text in the file
                code = self.textEditorContainer.currentWidget().get_text()
                
                self.current_project.scripts[fname] = code
            
                fname_without_ext = self.textEditorContainer.current_file_name[id]
                self.edit_status_bar(("File '%s' saved.") %fname_without_ext )
                self.textEditorContainer.setTabText(self.textEditorContainer.currentIndex(), fname_without_ext)
            except:
                self.edit_status_bar("File not saved...") 
                
            self.current_project.save()        
    
    def saveas(self):
        try:
            id = self.textEditorContainer.currentWidget().ID
            fname = qt.QtGui.QFileDialog.getSaveFileName(self, 'Save file', self.current_project.path/self.current_project.name/'scripts', "Python File(*.py)")
            code = self.textEditorContainer.currentWidget().get_text()
            
            self.current_project.scripts[fname] = code
            self.current_project.save()

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
        self.current_project.save()     

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
    
    
class CustomMenu(qt.QtGui.QMenu):
    def __init__(self, projects, parent):
        qt.QtGui.QMenu.__init__(self)
        for proj in projects:
            action = CustomAction(str(proj),self, parent)
            self.addAction(action)   
    
class CustomAction(qt.QtGui.QAction):
    def __init__(self, name, wid, parent):
        qt.QtGui.QAction.__init__(self, name, wid)
        self.name = name
        self.parent = parent
        qt.QtCore.QObject.connect(self, qt.QtCore.SIGNAL('triggered(bool)'), self.on_click)
    def on_click(self):
        self.parent.project_change(self.name)   



def show_splash_screen():
    """Show a small splash screen to make people wait for OpenAleaLab to startup"""
    # import metainfo
    pix = qt.QtGui.QPixmap("./resources/splash.png")
    splash = qt.QtGui.QSplashScreen(pix, qt.QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    # message = "" + metainfo.get_copyright() +\
              # "Version : %s\n"%(metainfo.get_version(),) +\
              # "Loading modules..."
    message = "Loading..."
    splash.showMessage(message, qt.QtCore.Qt.AlignCenter|qt.QtCore.Qt.AlignBottom)
    # -- make sure qt really display the message before importing the modules.--
    qt.QtGui.QApplication.processEvents()
    return splash

    
def main():
    app = qt.QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    MainW = MainWindow()
    MainW.show()
    app.exec_()

    
if( __name__ == "__main__"):
    main()

