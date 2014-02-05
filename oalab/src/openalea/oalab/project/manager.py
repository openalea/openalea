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
from openalea.vpltk.project.script import Scripts
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.oalab.control.picklable_curves import geometry_2_piklable_geometry
            
class ProjectManager(QtGui.QWidget):
    """
    Object which permit to manage projects.
    """
    def __init__(self, parent):
        super(ProjectManager, self).__init__()

        self.session = parent
        self.parent = self.session
        self.setAccessibleName("Project Manager")

        self.projectManager = PM()
        self.scriptManager = Scripts()
        
        for proj in self.projectManager.projects:
            self.session.project = proj
               
        self.actionNewPython = QtGui.QAction(QtGui.QIcon(":/images/resources/Python-logo.png"),"Python", self)
        self.actionNewR = QtGui.QAction(QtGui.QIcon(":/images/resources/RLogo.png"),"R", self)
        self.actionNewLPy = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/logo.png"),"L-System", self)
        self.actionNewWorkflow = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"Workflow", self)
        
        self.actionImportFile = QtGui.QAction(QtGui.QIcon(":/images/resources/import.png"),"Add file", self)
        
        self.actionNewProj = QtGui.QAction(QtGui.QIcon(":/images/resources/new.png"),"New", self)
        self.actionNewProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(QtGui.QIcon(":/images/resources/open.png"),"Open", self)
        self.actionOpenProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        #self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(QtGui.QIcon(":/images/resources/closeButton.png"),"Close All", self)
        
        QtCore.QObject.connect(self.actionNewProj, QtCore.SIGNAL('triggered(bool)'),self.new)
        QtCore.QObject.connect(self.actionOpenProj, QtCore.SIGNAL('triggered(bool)'),self.open)
        QtCore.QObject.connect(self.actionSaveProj, QtCore.SIGNAL('triggered(bool)'),self.saveCurrent)
        QtCore.QObject.connect(self.actionCloseProj, QtCore.SIGNAL('triggered(bool)'),self.closeCurrent)
        
        QtCore.QObject.connect(self.actionNewPython, QtCore.SIGNAL('triggered(bool)'),self.newPython)
        QtCore.QObject.connect(self.actionNewR, QtCore.SIGNAL('triggered(bool)'),self.newR)
        QtCore.QObject.connect(self.actionNewLPy, QtCore.SIGNAL('triggered(bool)'),self.newLpy)
        QtCore.QObject.connect(self.actionNewWorkflow, QtCore.SIGNAL('triggered(bool)'),self.newVisualea)
        
        QtCore.QObject.connect(self.actionImportFile, QtCore.SIGNAL('triggered(bool)'),self.importFile)
        
        self._actions = [["Project","Manage Project",self.actionNewProj,0],
                         ["Project","Manage Project",self.actionOpenProj,0],
                         ["Project","Manage Project",self.actionSaveProj,0],
                         ["Project","Manage Project",self.actionCloseProj,0],
                         ["Model","New Model",self.actionNewPython,0],
                         ["Model","New Model",self.actionNewR,0],
                         ["Model","New Model",self.actionNewLPy,0],
                         ["Model","New Model",self.actionNewWorkflow,0],
                         ["Model","New Model",self.actionImportFile,0]]

        self._project_changed()

           
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
        
    def showOpenFileDialog(self, extension="*.py *.lpy *.r *.wpy", where=None):
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
                    self.projectManager.close(self.session.project.name)
            
            self.session._project = self.projectManager.load(proj_name,proj_path)
            self.session._is_script = False
            self.session._is_proj = True
            self._project_changed()
            self._load_control()
            
            logger.debug("Project opened: " + str(self.session._project))

    def importFile(self, filename=None, extension="*.py *.lpy *.r *.wpy"):
        """
        Import a file and add it in the project
        """
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
                    self.session.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add_script(tab_name, txt)
                    self.session._update_locals()
                    self._script_change()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " +ext+ " not recognised"
                    logger.warning("Can't import file named %s in current project. Unknow extension."%filename)
        else:
            self.session._is_script = True
            self.session._is_proj = False
            where_ = None
            if self.session.project is not None:
                if len(self.session.project) != 0:
                    i = self.session.applet_container.currentIndex()
                    tab_text = self.session.applet_container.tabText(i)
                    where_ = self.session.project.get_name_by_ez_name(tab_text)
            if not filename:
                filename = self.showOpenFileDialog(extension=extension, where=where_)
            if filename:
                f = open(filename, "r")
                txt = f.read() 
                f.close()
                
                self.scriptManager.add_script(filename, txt) 
                self.session._project = self.scriptManager
                
                tab_name = self.session.project.get_ez_name_by_name(filename)
                ext = str(path(filename).splitext()[-1])
                ext = ext.split(".")[-1]

                
                self.session.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                try:
                    self.session._update_locals()
                    #self._script_change()
                    self._tree_view_change()
                    logger.debug("Import file named %s outside project"%tab_name)
                except:
                    print "File extension " +ext+ " not recognised"
                    logger.warning("Can't import file named %s outside project. Unknow extension: %s ."%(tab_name,ext))
        
    def new(self, name=None):
        """
        Create an empty project with a default name.
        """
        if not name:
            date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            name = self.showNewProjectDialog('project_%s' %date)
        if not name:
            date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            name = 'project_%s' %date
        if self.session.current_is_project():
            if self.session.project is not None:
            	self.projectManager.close(self.session.project.name)
        self.session._project = self.projectManager.create(name)
        self.session._is_script = False
        self.session._is_proj = True

        self._project_changed()
        self._load_control()
        
        self.session.applet_container.addCreateFileTab()
        
    def newPython(self):       
        if self.session.current_is_project():
            tab_name = "script.py"
            self.session.applet_container.newTab(applet_type="python", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  

            self.session._update_locals()
            self._script_change()
            self._tree_view_change() 
        else:
            self.session._is_script = True
            self.session._is_proj = False
            tab_name = "script.py"
            self.scriptManager.add_script(tab_name, "") 
            self.session._project = self.scriptManager
            self.session.applet_container.newTab(applet_type="python", tab_name=tab_name)
            self.session._update_locals()
            #self._script_change()
            self._tree_view_change()
        
    def newR(self):    
        if self.session.current_is_project():
            tab_name = "script.r"
            self.session.applet_container.newTab(applet_type="r", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.session._update_locals()
            self._script_change()
            self._tree_view_change()
        else:
            self.session._is_script = True
            self.session._is_proj = False
            tab_name = "script.r"
            self.scriptManager.add_script(tab_name, "") 
            self.session._project = self.scriptManager
            self.session.applet_container.newTab(applet_type="r", tab_name=tab_name)
            self.session._update_locals()
            #self._script_change()
            self._tree_view_change()
        
    def newLpy(self):
        if self.session.current_is_project():
            tab_name = "script.lpy"
            self.session.applet_container.newTab(applet_type="lpy", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.session._update_locals()
            self._script_change()
            self._tree_view_change()
        else:
            self.session._is_script = True
            self.session._is_proj = False
            tab_name = "script.lpy"
            self.scriptManager.add_script(tab_name, "") 
            self.session._project = self.scriptManager
            self.session.applet_container.newTab(applet_type="lpy", tab_name=tab_name)
            self.session._update_locals()
            #self._script_change()
            self._tree_view_change()
                    
    def newVisualea(self):
        if self.session.current_is_project():
            tab_name = "workflow.wpy"
            self.session.applet_container.newTab(applet_type="visualea",tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.session._update_locals()
            self._script_change()
            self._tree_view_change()
        else:
            self.session._is_script = True
            self.session._is_proj = False
            tab_name = "workflow.wpy"
            self.scriptManager.add_script(tab_name, "") 
            self.session._project = self.scriptManager
            self.session.applet_container.newTab(applet_type="visualea", tab_name=tab_name)
            self.session._update_locals()
            #self._script_change()
            self._tree_view_change()
                    
    def removeModel(self, model_name):
        """
        :param model_name: Name of the model to remove in the current project
        
        TODO
        """
        pass    
        
    def openModel(self, fname=None):
        """"
        Open a (script-type) file
        
        TODO
        """
        self.session._is_script = True
        self.session._is_proj = False
        self.importFile(filename=fname, extension="*")
    
    def openPython(self, fname=None):
        """
        Open a python script named "fname".
        If "fname"==None, display a dialog
        
        TODO
        """
        self.session._is_script = True
        self.session._is_proj = False
        self.importFile(filename=fname, extension="*.py")
        
    def renameCurrent(self, name):
        """
        Rename current project.
        
        TODO
        """
        pass
    
    def saveCurrent(self):
        """
        Save current project.
        """
        if self.session.current_is_project():
            current = self.session.project
            current.controls = dict()
            container = self.session.applet_container
        
            for i in range(container.count()):
                container.setCurrentIndex(i)
                name = container.tabText(i)
                container.widget(i).save(name)
                
            colors = self.session.applets['ControlPanel'].colormap_editor.getTurtle().getColorList()
            current.controls["color map"] = colors
            
            geoms = self.session.applets['ControlPanel'].geometry_editor.getObjects()
            

            for (manager, geom) in geoms:
                if geom != list():
                    new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
                    current.controls[new_name] = new_obj
            
            scalars = self.session.applets['ControlPanel'].scalars_editor.getScalars()
            for scalar in scalars:
                current.controls[scalar.name] = scalar

            current.save()
            
        elif self.session.current_is_script():
            ## TODO : Warning! Save all not just current
            #current = self.session.project
            #container = 
            self.session.applet_container.save_all()
            self._tree_view_change()
        
            #for i in range(container.count()):
                #container.setCurrentIndex(i)
                #name = container.tabText(i)
                #container.save_all()
                #container.setTabText(i, container.widget(i).applet.name)
                
    def closeCurrent(self):
        """
        Close current project or scripts.
        """
        if self.session.current_is_project():
            self.projectManager.close(self.session.project.name)
            self._clear_control()
            logger.debug("Close Project")
        elif self.session.current_is_script():
            logger.debug("Close Scripts")
            
        self.session._project = None
        self.session._is_script = False
        self.session._is_proj = False
        
        self._scene_change()
        #self._control_change()
        self._script_change()
        self._tree_view_change()
            
    def displayCurrentName(self):
        """
        Display name of the current project
        """
        if self.session.current_is_project():
            print self.session.project.name
        else:
            print ""
        
    def displayProjectTreeOnDisk(self):
        """
        Display a QTreeView of the current project on the disk.
        Permit to open files in click on his name.
        
        TODO
        """  
        print self.session.project
        
    def _project_changed(self):
        """
        Update what is needed when the current project is changed
        """
        logger.debug("Project changed")
        self.session._update_locals()
        if self.session.current_is_project():
            self._scene_change()
            #self._control_change()
            self._script_change()
            self._tree_view_change()
        elif self.session.current_is_script():
            self._tree_view_change()
            #self._script_change()
        else:
            pass
            
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
            self.session.applets['ControlPanel'].colormap_editor.getTurtle().setMaterial(i, color)
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
            self.session.applets['ControlPanel'].geometry_editor.setObjects(geom)
        if scalars is not list():
            logger.debug("Load Controls Scalars: %s "%str(scalars))
            self.session.applets['ControlPanel'].scalars_editor.setScalars(scalars)
        
    def _update_control(self):
        """
        Get controls from widget and put them into project
        """
        logger.debug("Update Controls")
        #self.session.project.controls = dict()
        
        self.session.project.controls["color map"] = PglTurtle().getColorList()
        
        objects = self.session.applets['ControlPanel'].geometry_editor.getObjects()
        for (manager,obj) in objects:
            if obj != list():
                obj, name = geometry_2_piklable_geometry(manager,obj)
                self.session.project.controls[unicode(name)] = obj
                
        scalars = self.session.applets['ControlPanel'].scalars_editor.getScalars()
        for scalar in scalars:
            self.session.project.controls[unicode(scalar.name)] = scalar
                
    def _clear_control(self):
            self.session.applets['ControlPanel'].geometry_editor.clear()
            n = len(self.session.applets['ControlPanel'].scalars_editor.getScalars())
            for scalar in range(n):
            	    self.session.applets['ControlPanel'].scalars_editor.deleteScalars()
            
    def _control_change(self):
        pass           
        
    def _tree_view_change(self):
        logger.debug("Tree View changed")
        self.session.applets['Project'].update()
        
    def _script_change(self):
        logger.debug("Script changed")
        if self.session.current_is_project():
            # If project
            project = self.session.project
            self.session.applet_container.reset()
            for script in project.scripts:
                language = str(script).split('.')[-1]
                self.session.applet_container.openTab(language, script, project.scripts[script])
            
        elif self.session.current_is_script():
            # If script
            self.session.applet_container.reset()
            scripts = self.session.project
            
            for script_name in scripts:
                language = str(script_name).split('.')[-1]
                txt = scripts[script_name]
                self.session.applet_container.openTab(language, script_name, txt)
        else:
            # If nothing opened
            #self.session.applet_container.reset()
            self.session.applet_container.closeAll()
            
    def _scene_change(self):
        logger.debug("Scene changed")
        self.session.scene.reset()
        if self.session.current_is_project():
            project = self.session.project
            for w in project.scene:
                self.session.scene.add(name=w,obj=project.scene[w])
