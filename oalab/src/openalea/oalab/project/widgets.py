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
import warnings
from openalea.vpltk.project.project import ProjectManager as PM   

class ProjectWidget(QtGui.QWidget):
    """
    Widget which permit to manage projects.
    """
    'Permit to change current project and display what is inside current_project'

    def __init__(self, parent):
        super(ProjectWidget, self).__init__() 
        self.parent = parent # session
        self.session = parent
        layout = QtGui.QVBoxLayout()
        
        
        self.currentProjBtn = QtGui.QPushButton(self)
        self.currentProjBtn.setText("Select Project")

        self.currentProjWid = QtGui.QToolBar(self)
        self.currentProjWid.setOrientation(QtCore.Qt.Vertical)
        self.currentProjWid.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)

        self.currentProjWid.addWidget(self.currentProjBtn)
       
        layout.addWidget(self.currentProjWid)
        
        self.setLayout(layout)
        self.projectManager = PM()
        
        self.parent.projects = self.projectManager.projects
               
        self.actionNewPython = QtGui.QAction(QtGui.QIcon(":/images/resources/Python-logo.png"),"Python", self)
        self.actionNewR = QtGui.QAction(QtGui.QIcon(":/images/resources/RLogo.png"),"R", self)
        self.actionNewLPy = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/logo.png"),"L-System", self)
        self.actionNewWorkflow = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"Workflow", self)
        
        self.actionImportFile = QtGui.QAction(QtGui.QIcon(":/images/resources/import.png"),"Import", self)
        
        self.actionNewProj = QtGui.QAction(QtGui.QIcon(":/images/resources/new.png"),"New", self)
        self.actionNewProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(QtGui.QIcon(":/images/resources/open.png"),"Open", self)
        self.actionOpenProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(QtGui.QIcon(":/images/resources/closeButton.png"),"Close", self)
        
        QtCore.QObject.connect(self.actionNewProj, QtCore.SIGNAL('triggered(bool)'),self.new)
        QtCore.QObject.connect(self.actionOpenProj, QtCore.SIGNAL('triggered(bool)'),self.open)
        QtCore.QObject.connect(self.actionSaveProj, QtCore.SIGNAL('triggered(bool)'),self.saveCurrent)
        QtCore.QObject.connect(self.actionCloseProj, QtCore.SIGNAL('triggered(bool)'),self.closeCurrent)
        
        QtCore.QObject.connect(self.actionNewPython, QtCore.SIGNAL('triggered(bool)'),self.newPython)
        QtCore.QObject.connect(self.actionNewR, QtCore.SIGNAL('triggered(bool)'),self.newR)
        QtCore.QObject.connect(self.actionNewLPy, QtCore.SIGNAL('triggered(bool)'),self.newLpy)
        QtCore.QObject.connect(self.actionNewWorkflow, QtCore.SIGNAL('triggered(bool)'),self.newVisualea)
        
        QtCore.QObject.connect(self.actionImportFile, QtCore.SIGNAL('triggered(bool)'),self.importFile)
        
        self._actions = ["Project",[["Manage Project",self.actionNewProj,0],
                                    ["Manage Project",self.actionOpenProj,0],
                                    ["Manage Project",self.actionSaveProj,0],
                                    ["Manage Project",self.actionCloseProj,0],
                                    ["New Model",self.actionNewPython,0],
                                    ["New Model",self.actionNewR,0],
                                    ["New Model",self.actionNewLPy,0],
                                    ["New Model",self.actionNewWorkflow,0],
                                    ["New Model",self.actionImportFile,0]]]

        self._project_changed()

            
    def showOpenProjectDialog(self):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Project Directory', 
                my_path)
        return fname
        
    def showOpenFileDialog(self):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select File to import', 
                my_path, "Scripts Files (*.py *.lpy *.r *.wpy)")
        return fname

    def actions(self):
        return self._actions
    
    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Project"  
    
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
            proj = self.projectManager.load(proj_name,proj_path)
            # Send an event rather than setting by code
            self.parent.cprojname = proj.name
            
            self._project_changed()
            logger.debug("Open Project named " + proj_name)
            
    def openSvn(self, name=None):
        """
        Display a widget to choose project versionned thx to SVN to open.
        Then open project.
        """
        print("todo : open svn project")
        pass
        """
        if not name:
            date = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
            name = 'project_%s' %date
        proj = self.projectManager.create(name)
        self.parent.cprojname = proj.name

        self._project_changed()
##        app.setActiveWindow(window.centralWidget())
        """
        
    def openGit(self, name=None):
        """
        Display a widget to choose project versionned thx to Git to open.
        Then open project.
        """
        print("todo : open git project")
        pass
        """
        if name is False:
            name = self.showOpenFileDialog()
        if name:
            proj_path = path(name).abspath()
            proj_name = proj_path.basename()
            proj_path = proj_path.dirname()
            proj = self.projectManager.load(proj_name,proj_path)
            # Send an event rather than setting by code
            self.parent.cprojname = proj.name
            
            self._project_changed()
        """

    def importFile(self, filename=None):
        """
        Import a file and add it in the project
        """
        project = self.session.project
        if project:
        
            if not filename:
                filename = self.showOpenFileDialog()

            if filename:
                f = open(filename, "r")
                txt = f.read() 
                f.close()
                
                tab_name = str(path(filename).splitpath()[-1])
                ext = str(path(filename).splitext()[-1])
                ext = ext.split(".")[-1]

                try:
                    self.parent.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add_script(tab_name, txt)
                    self.parent._update_locals()
                    self._current_proj_script_change()
                    self._current_proj_tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " +ext+ "not recognised"
                    logger.warning("Can't import file named " + filename + ". Unknow extension.")
        else:
            print "Doesn't work outside a project. Please create or open a project to continue."
            logger.warning("Can't import file. You are not inside project.")
        
    def new(self, name=None):
        """
        Create an empty project with a default name.
        """
        if not name:
            date = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
            name = 'project_%s' %date
        proj = self.projectManager.create(name)
        self.parent.cprojname = proj.name

        self._project_changed()
##        app.setActiveWindow(window.centralWidget())

    def newSvn(self, name=None):
        """
        Create an empty project versionned thx to SVN with a default name.
        """
        print("todo : new svn project")
        pass
        """
        if name is False:
            name = self.showOpenFileDialog()
        if name:
            proj_path = path(name).abspath()
            proj_name = proj_path.basename()
            proj_path = proj_path.dirname()
            proj = self.projectManager.load(proj_name,proj_path)
            # Send an event rather than setting by code
            self.parent.cprojname = proj.name
            
            self._project_changed()
        """
        
    def newGit(self, name=None):
        """
        Create an empty project versionned thx to Git with a default name.
        """
        print("todo : new git project")
        pass
        """
        if not name:
            date = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
            name = 'project_%s' %date
        proj = self.projectManager.create(name)
        self.parent.cprojname = proj.name

        self._project_changed()
##        app.setActiveWindow(window.centralWidget())
        """
        
    def newPython(self):       
        if self.session.project:
            tab_name = "script.py"
            self.parent.applet_container.newTab(applet_type="python", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  

            self.parent._update_locals()
            self._current_proj_script_change()
            self._current_proj_tree_view_change() 
        else:
            print("Open or create a project before using models")
        
    def newR(self):    
        if self.session.project:
            tab_name = "script.r"
            self.parent.applet_container.newTab(applet_type="r", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.parent._update_locals()
            self._current_proj_script_change()
            self._current_proj_tree_view_change()
        else:
            print("Open or create a project before using models")
        
    def newLpy(self):
        if self.session.project:
            tab_name = "script.lpy"
            self.parent.applet_container.newTab(applet_type="lpy", tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.parent._update_locals()
            self._current_proj_script_change()
            self._current_proj_tree_view_change()
        else:
            print("Open or create a project before using models")
                    
    def newVisualea(self):
        if self.session.project:
            tab_name = "workflow.wpy"
            self.parent.applet_container.newTab(applet_type="visualea",tab_name=tab_name)
            self.session.project.add_script(tab_name, self.session.applet_container.applets[-1].widget().get_text())  
            
            self.parent._update_locals()
            self._current_proj_script_change()
            self._current_proj_tree_view_change()
            
        else:
            print("Open or create a project before using models")
                    
    def removeModel(self, model_name):
        """
        :param model_name: Name of the model to remove in the current project
        """
        # TODO
        pass    
        
    def openModel(self):
        """"
        Open a (script-type) file
        """
        pass
    
    def openPython(self, fname=None):
        """
        Open a python script named "fname".
        If "fname"==None, display a dialog
        """
        print("todo : Open a Python Script")
        pass
        
    def changeCurrent(self, name):
        """
        set the project name 'name' current
        """
        # TODO : to implement
        #print name
        
        #self._project_changed()
        pass
        
    def renameCurrent(self, name):
        """
        Rename current project.
        """
        #print "rename"
##        self.parent.cproject.name = name
        
        self._project_changed()
        
    def closeCurrent(self):
        """
        close current project
        """
        name = self.session.cprojname
        
        if len(self.session.projects) > 1:
            del self.session.projects[name]
            for pname in self.session.projects:
                self.session.cprojname = pname
        else:
            warnings.warn("Can't close all projects. TODO : Permit to user to work outside project")
        
        # TODO : Permit to user to work outside project
        if len(self.session.projects) < 1:
            self.session.applet_container.addDefaultTab()

        self._project_changed()
    
    def saveCurrent(self):
        """
        Save current project.
        """
        current = self.session.project
        if current is not None:
            container = self.session.applet_container
        
            for i in range(container.count()):
                container.setCurrentIndex(i)
                name = container.tabText(i)
                container.widget(i).save(name)
                
            colors = self.session.control_panel.colormap_editor.getTurtle().getColorList()
            current.controls["color map"] = colors

            current.save()
        
    def saveAll(self):
        """
        Save all opened projects
        """
        for proj in self.parent.projects:
            proj.save()
        
    def displayCurrentName(self):
        """
        Display name of the current project
        """
        print self.session.cprojname
        
    def displayProjectTreeOnDisk(self):
        """
        Display a QTreeView of the current project on the disk.
        Permit to open files in click on his name.
        """  
        print self.session.project
        
    def _project_changed(self):
        """
        Update what is needed when the current project is changed
        """
        self.parent._update_locals()
        current = self.session.project
        if current:
            self._current_proj_scene_change()
            self._current_proj_control_change()
            self._current_proj_script_change()
            self._current_proj_tree_view_change()
            

    def _current_proj_control_change(self):
        if self.session.current_is_project():
            proj = self.session.project
            if not proj.controls.has_key("color map"):    
                proj.controls["color map"] = PglTurtle().getColorList()
            # Link with color map from application
            i = 0
            for color in proj.controls["color map"]:
                self.session.control_panel.colormap_editor.getTurtle().setMaterial(i, color)
                i += 1
            
            
            #newcontrols = self.session.control_panel_manager.get_managers()
            #for controlname in newcontrols:
            #    proj.controls[controlname] = newcontrols[controlname]
            
        
    def _current_proj_tree_view_change(self):
        self.session.project_layout_widget.update()
        
    def _current_proj_script_change(self):
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
            
            script = self.session.project
            name = script.name
            language = str(name).split('.')[-1]
            txt = script.value
            
            self.session.applet_container.openTab(language, name, txt)
            
        else:
            # If nothing opened
            self.session.applet_container.reset()
            
    def _current_proj_scene_change(self):
        if self.session.current_is_project():
            self.session.scene_widget.getScene().reset()
            project = self.session.project
            for w in project.scene:
                self.session.scene_widget.getScene().add(name=w,obj=project.scene[w])
