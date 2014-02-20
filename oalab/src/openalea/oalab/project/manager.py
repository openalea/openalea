# -*- python -*-
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
__revision__ = "$Id: "


from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.path import path
from openalea.core import settings
from openalea.core import logger
from time import gmtime, strftime
from openalea.plantgl.all import PglTurtle
from openalea.vpltk.project.project import ProjectManager as PM   
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.oalab.control.picklable_curves import geometry_2_piklable_geometry
            
class ProjectManager(QtGui.QWidget):
    """
    Object which permit to manage projects.
    """
    def __init__(self, session, controller, parent=None):
        super(ProjectManager, self).__init__()

        self._actions = []
        self.paradigms_actions = []
        self.session = session
        self.controller = controller
        self.setAccessibleName("Project Manager")

        self.projectManager = PM()
        
        for proj in self.projectManager.projects:
            self.session._project = proj
                
        self.actionEditFile = QtGui.QAction(QtGui.QIcon(":/images/resources/edit.png"),"Edit file", self)
        self.actionImportFile = QtGui.QAction(QtGui.QIcon(":/images/resources/import.png"),"Import", self)
        
        self.actionNewProj = QtGui.QAction(QtGui.QIcon(":/images/resources/new.png"),"New", self)
        self.actionNewProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(QtGui.QIcon(":/images/resources/open.png"),"Open", self)
        self.actionOpenProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        self.actionSaveProjAs = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save As", self)
        #self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(QtGui.QIcon(":/images/resources/closeButton.png"),"Close All", self)
        
        QtCore.QObject.connect(self.actionNewProj, QtCore.SIGNAL('triggered(bool)'),self.new)
        QtCore.QObject.connect(self.actionOpenProj, QtCore.SIGNAL('triggered(bool)'),self.open)
        QtCore.QObject.connect(self.actionSaveProjAs, QtCore.SIGNAL('triggered(bool)'),self.saveAs)
        QtCore.QObject.connect(self.actionSaveProj, QtCore.SIGNAL('triggered(bool)'),self.saveCurrent)
        QtCore.QObject.connect(self.actionCloseProj, QtCore.SIGNAL('triggered(bool)'),self.closeCurrent)
        
        QtCore.QObject.connect(self.actionImportFile, QtCore.SIGNAL('triggered(bool)'),self.importFile)
        QtCore.QObject.connect(self.actionEditFile, QtCore.SIGNAL('triggered(bool)'),self.editFile)
        
        self._actions = [["Project","Manage Project",self.actionNewProj,1],
                         ["Project","Manage Project",self.actionOpenProj,0],
                         ["Project","Manage Project",self.actionSaveProj,0],
                         ["Project","Manage Project",self.actionSaveProjAs,1],
                         ["Project","Manage Project",self.actionCloseProj,1],
                         ["Model","New Model",self.actionEditFile,0],
                         ["Model","New Model",self.actionImportFile,0]]
                         
        self.extensions = ""                 
        # Connect actions from applet_container.paradigms to menu (newPython, newLpy,...)       
        for applet in self.controller.applet_container.paradigms.values():
            action = QtGui.QAction(QtGui.QIcon(applet.icon), applet.default_name, self)
            action.triggered.connect(self.newModel)
            self._actions.append(["Model","New Model",action,0],)
            self.paradigms_actions.append(action)
            self.extensions = self.extensions + applet.pattern + " "
        
        self.defaultProj()
        
    def defaultProj(self):
        proj = self.projectManager.load_empty()
        self.session._project = proj
        self.session._is_proj = True

        if not self.session.project.scripts:
            txt = '''# -*- coding: utf-8 -*-
"""
OpenAlea Lab editor

This temporary script is saved in temporary project in 
%s

You can rename/move this project thanks to the button "Save As" in menu.
"""'''%str(self.session.project.path/self.session.project.name)
            self.session.project.add_script(name=".temp.py", script=txt)
            
        self._project_changed()
        self._load_control()
           
    def showNewProjectDialog(self, default_name=None, text=None):
        my_path = path(settings.get_project_dir())
        if default_name:
            my_path = my_path/default_name
        if not text:
            text = 'Select name to create project'
        fname = QtGui.QFileDialog.getSaveFileName(self, text, 
                my_path)
        return fname       
            
    def showOpenProjectDialog(self):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Project Directory', 
                my_path)
        return fname
        
    def showOpenFileDialog(self, extension=None, where=None):
        if extension is None:
            extension = self.extensions
        
        if where is not None: 
            my_path = path(str(where)).abspath().splitpath()[0]
        else:
            my_path = path(settings.get_project_dir())
        logger.debug("Search to open file with extension "+extension+" from "+my_path)
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select File to open', 
                my_path, "All (*);;Scripts Files (%s)"%extension)
        return fname

    def actions(self):
        return self._actions
    
    def open(self, name=False):
        """
        Display a widget to choose project to open.
        Then open project.
        """
        if name is False:
            name = self.showOpenProjectDialog()
        if name:
            proj_path = path(name).abspath()
            proj_name = proj_path.basename()
            proj_path = proj_path.dirname()
            logger.debug("Open Project named " + proj_name)
            if self.session.project is not None:
                if self.session.current_is_project():
                    logger.debug("Close Project named " + self.session.project.name)
                    self.projectManager.close(self.session.project.name)
                    logger.debug("Project named " + self.session.project.name + " closed.")
            
            proj = self.projectManager.load(proj_name,proj_path)
            logger.debug("Project " + str(proj) + " loaded")
            
            if proj == -1 :
                logger.warning("Project was not loaded...")
                return -1
            else:
                self.session._project = proj
                self.session._is_proj = True
                self._project_changed()
                self._load_control()
                
                logger.debug("Project opened: " + str(self.session._project))
                return self.session._project

    def editFile(self, filename=None, extension=None):
        """
        Permit to edit a file wich is outside project.
        And add link to file in project.
        """     
        if extension is None:
            extension = self.extensions
            
        if self.session.current_is_project():
            project = self.session.project     
            if not filename:
                if extension:
                    filename = self.showOpenFileDialog(extension)
                else:
                    filename = self.showOpenFileDialog()
            if filename:
                filename = path(filename).abspath()
                
                f = open(filename, "r")
                txt = f.read() 
                f.close()
                
                tab_name = str(path(filename).splitpath()[-1])
                ext = str(path(filename).splitext()[-1])
                ext = ext.split(".")[-1]
                logger.debug("Try to import file named " + tab_name + " . With applet_type " + ext)

                try:
                    self.controller.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add_script(filename, txt)
                    self.controller._update_locals()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " +ext+ " not recognised"
                    logger.warning("Can't import file named %s in current project. Unknow extension."%filename)
        else:
            print "You are not working inside project. Please create or load one first."


    def importFile(self, filename=None, extension=None):
        """
        Import a file and add it in the project
        """
        if extension is None:
            extension = self.extensions
            
        if self.session.current_is_project():
            project = self.session.project     
            if not filename:
                if extension:
                    filename = self.showOpenFileDialog(extension)
                else:
                    filename = self.showOpenFileDialog()
            if filename:
                f = open(filename, "r")
                txt = f.read() 
                f.close()
                
                tab_name = str(path(filename).splitpath()[-1])
                ext = str(path(filename).splitext()[-1])
                ext = ext.split(".")[-1]
                logger.debug("Try to import file named " + tab_name + " . With applet_type " + ext)

                try:
                    self.controller.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add_script(tab_name, txt)
                    self.controller._update_locals()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " +ext+ " not recognised"
                    logger.warning("Can't import file named %s in current project. Unknow extension."%filename)
        else:
            print "You are not working inside project. Please create or load one first."
        
    def new(self, name=None):
        """
        Create an empty project with a default name.
        """
        if not name:
            date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            name = self.showNewProjectDialog('project_%s' %date)
        if name:
            if self.session.current_is_project():
                if self.session.project is not None:
                    self.projectManager.close(self.session.project.name)
            self.session._project = self.projectManager.create(name)
            self.session._is_proj = True
            self._load_control()
            self._project_changed()
       
    def newModel(self, applet_type=None, tab_name=None, script=""):
        """
        Create a new model of type 'applet_type
        
        :param applet_type: type of applet to add. Can be Workflow, LSystem, Python, R
        """
        if self.session.current_is_project():
            if not applet_type:
                button = self.sender() 
                applet_type = button.text() # can be Workflow, LSystem, Python, R
                #TODO: this approach is not reliable. If a developer change action name, it breaks the system
                # a better approach should be to define a "newModel" method in IApplet and call it directly
                # for instance in __init__ : action.triggered.connect(applet.newModel)        
            Applet = self.controller.applet_container.paradigms[applet_type]
            if not tab_name:
                tab_name = Applet.default_file_name
            self.controller.applet_container.newTab(applet_type=applet_type, tab_name=tab_name, script=script)
            text = self.controller.applet_container.applets[-1].widget().get_text()
            self.session.project.add_script(tab_name, text)  
            self.controller._update_locals()
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def removeModel(self, model_name):
        """
        :param model_name: Name of the model to remove in the current project
        """
        if self.session.current_is_project():
            self.session.project.remove_script(model_name)   
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."
        
    def openModel(self, fname=None, extension="*.*"):
        """"
        Open a (script-type) file named "fname".
        If "fname"==None, display a dialog with filter "extension".
        
        :param fname: filename to open. Default = None
        :param extension: extension of file to open. Default = "*.*"
        """
        if self.session.current_is_project():
            self.importFile(filename=fname, extension=extension)
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."
        
    def renameCurrent(self, new_name=None):
        """
        Rename current project.
        """
        if self.session.current_is_project():
            name = self.session.project.name
            if not new_name:
                new_name = self.showNewProjectDialog(default_name=path(name)/"..", text='Select new name to save project')
            self.session.project.rename(categorie="project", old_name=name, new_name=new_name)
            self._project_changed()
        else:
            print("You are not working inside project, so you can't use 'rename project'. Please create or load one first.")
    
    def saveAs(self):
        """
        Save current project but permit to rename and move it..
        """
        if self.session.current_is_project():
            name = self.showNewProjectDialog(default_name=None, text="Select name to save project")
            if name:
                self.session.project.rename(categorie="project", old_name=self.session.project.name, new_name=name)
                self._tree_view_change()
                self.saveCurrent()
        else:
            print "You are not working inside project. Please create or load one first."
    
    def saveCurrent(self):
        """
        Save current project.
        """
        if self.session.current_is_project():
            current = self.session.project
            current.controls = dict()
            container = self.controller.applet_container
        
            for i in range(container.count()):
                container.setCurrentIndex(i)
                name = container.tabText(i)
                container.widget(i).save(name)
                
            colors = self.controller.applets['ControlPanel'].colormap_editor.getTurtle().getColorList()
            current.controls["color map"] = colors
            
            geoms = self.controller.applets['ControlPanel'].geometry_editor.getObjects()
            

            for (manager, geom) in geoms:
                if geom != list():
                    new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
                    current.controls[new_name] = new_obj
            
            scalars = self.controller.applets['ControlPanel'].scalars_editor.getScalars()
            for scalar in scalars:
                current.controls[scalar.name] = scalar

            current.save()
            self._project_changed()
            
        else:
            print "You are not working inside project. Please create or load one first."
                
    def closeCurrent(self):
        """
        Close current project.
        """
        if self.session.current_is_project():
            logger.debug("Close Project named %s"%self.session.project.name)
            self.projectManager.close(self.session.project.name)
            self.session._project = None
            self.session._is_proj = False
            self._clear_control()
            self.controller.applet_container.closeAll()
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def _project_changed(self):
        """
        Update what is needed when the current project is changed
        """
        logger.debug("Project changed")
        self.controller._update_locals()
        self._scene_change()
        self._control_change() #do nothing
        self._script_change()
        self._tree_view_change()
            
    def update_from_widgets(self):
        self._update_control()
    
    def _load_control(self):
        """
        Get controls from project and put them into widgets
        """
        logger.debug("Load Controls")
        proj = self.session.project
        if not proj.controls.has_key("color map"):    
            proj.controls["color map"] = PglTurtle().getColorList()
        i = 0
        logger.debug("Load Controls color map: %s "%str(proj.controls["color map"]))
        for color in proj.controls["color map"]:
            self.controller.applets['ControlPanel'].colormap_editor.getTurtle().setMaterial(i, color)
            i += 1
            
        managers = get_managers()
        geom = []
        scalars = []   
    
        for control in proj.controls:
            logger.debug(str(proj.controls[control]))
            if hasattr(proj.controls[control], "__module__"):
                if proj.controls[control].__module__ == "openalea.oalab.control.picklable_curves":
                    typename = proj.controls[control].typename
                    proj.controls[control].name = str(control)
                    manager = managers[typename]
                    geom.append((manager,proj.controls[control]))
                elif str(control) != "color map":
                    scalars.append(proj.controls[control])   
            elif str(control) != "color map":
                scalars.append(proj.controls[control])    
        if geom is not list():
            logger.debug("Load Controls Geom: %s "%str(geom))
            self.controller.applets['ControlPanel'].geometry_editor.setObjects(geom)
        if scalars is not list():
            logger.debug("Load Controls Scalars: %s "%str(scalars))
            self.controller.applets['ControlPanel'].scalars_editor.setScalars(scalars)
        
    def _update_control(self):
        """
        Get controls from widget and put them into project
        """
        logger.debug("Update Controls")
        #self.session.project.controls = dict()
        
        self.session.project.controls["color map"] = PglTurtle().getColorList()
        
        objects = self.controller.applets['ControlPanel'].geometry_editor.getObjects()
        for (manager,obj) in objects:
            if obj != list():
                obj, name = geometry_2_piklable_geometry(manager,obj)
                self.session.project.controls[unicode(name)] = obj
                
        scalars = self.controller.applets['ControlPanel'].scalars_editor.getScalars()
        for scalar in scalars:
            self.session.project.controls[unicode(scalar.name)] = scalar
                
    def _clear_control(self):
        self.controller.applets['ControlPanel'].geometry_editor.clear()
        n = len(self.controller.applets['ControlPanel'].scalars_editor.getScalars())
        for scalar in range(n):
                self.controller.applets['ControlPanel'].scalars_editor.deleteScalars()
            
    def _control_change(self):
        pass           
        
    def _tree_view_change(self):
        logger.debug("Tree View changed")
        self.controller.applets['Project'].update()
        
    def _script_change(self):
        logger.debug("Script changed")
        if self.session.current_is_project():
            project = self.session.project
            self.controller.applet_container.reset()
            for script in project.scripts:
                language = str(script).split('.')[-1]
                self.controller.applet_container.openTab(language, script, project.scripts[script])

    def _scene_change(self):
        logger.debug("Scene changed")
        if self.session.current_is_project():
            self.controller.scene.reset()
            project = self.session.project
            for w in project.scene:
                self.controller.scene.add(name=w,obj=project.scene[w])
