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
from openalea.vpltk.project.project import Script, Scripts
from openalea.plantgl.all import BezierCurve2D, NurbsCurve2D, Polyline2D, NurbsPatch
from openalea.oalab.control.picklable_curves import RedNurbs2D, RedBezierNurbs2D, RedPolyline2D, RedNurbsPatch
from openalea.lpy.gui.objectmanagers import get_managers
            
class ProjectWidget(QtGui.QWidget):
    """
    Widget which permit to manage projects.
    
    Permit to change current project and display what is inside current_project
    """
    def __init__(self, parent):
        super(ProjectWidget, self).__init__() 
        self.session = parent
        self.parent = self.session
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
        
    def showOpenFileDialog(self, extension="*.py *.lpy *.r *.wpy", where=None):
        if where is not None: 
            my_path = path(str(where)).abspath().splitpath()[0]
        else:
            my_path = path(settings.get_project_dir())
        logger.debug("Search to open file with extension "+extension+" from "+my_path)
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select File to open', 
                my_path, "Scripts Files (%s);;All (*)"%extension)
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
            if self.session.project is not None:
                if self.session.current_is_project():
                    self.projectManager.close(self.session.project.name)
            self.session._project = self.projectManager.load(proj_name,proj_path)
            self.session._is_script = False
            self.session._is_proj = True
            self._project_changed()
            logger.debug("Open Project named " + proj_name)
            
    def openSvn(self, name=None):
        """
        Display a widget to choose project versionned thx to SVN to open.
        Then open project.
        
        TODO
        """
        pass
        
    def openGit(self, name=None):
        """
        Display a widget to choose project versionned thx to Git to open.
        Then open project.
        
        TODO
        """
        pass

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

                try:
                    self.session.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add_script(tab_name, txt)
                    self.session._update_locals()
                    self._script_change()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " +ext+ "not recognised"
                    logger.warning("Can't import file named " + filename + " in current project. Unknow extension.")
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

                try:
                    self.session.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    self.session._update_locals()
                    #self._script_change()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name + " outside project")
                except:
                    print "File extension " +ext+ "not recognised"
                    logger.warning("Can't import file named " + filename + " outside project. Unknow extension: " + ext + " .")
        
    def new(self, name=None):
        """
        Create an empty project with a default name.
        """
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

    def newSvn(self, name=None):
        """
        Create an empty project versionned thx to SVN with a default name.
        
        TODO
        """
        pass
        
    def newGit(self, name=None):
        """
        Create an empty project versionned thx to Git with a default name.
        
        TODO
        """
        pass
        
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
        
    def openModel(self):
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
                
            colors = self.session.control_panel.colormap_editor.getTurtle().getColorList()
            current.controls["color map"] = colors
            
            geoms = self.session.control_panel.geometry_editor.getObjects()
            
            #current.controls["geometry"] = geoms
            for (manager, geom) in geoms:
                name = str(geom.getName())
                if isinstance(geom, BezierCurve2D):
                    geom = RedBezierNurbs2D(geom.ctrlPointList)
                    logger.debug("Transform BezierCurve2D into RedBezierNurbs2D")
                elif  isinstance(geom, NurbsCurve2D):
                    geom = RedNurbs2D(geom.ctrlPointList)
                    logger.debug("Transform NurbsCurve2D into RedNurbs2D")
                elif isinstance(geom, Polyline2D):
                    geom = RedPolyline2D(geom.pointList)
                    logger.debug("Transform Polyline2D into RedPolyline2D")
                elif isinstance(geom, NurbsPatch):
                    geom = RedNurbsPatch(geom.ctrlPointMatrix)
                    logger.debug("Transform NurbsPatch into RedNurbsPatch")
                else:
                    logger.debug("Transform Nothing %s"%str(geom))
                
                logger.debug("Save control geometry_%s_%s"%(manager.typename,name))

                current.controls["geometry_%s_%s"%(manager.typename,name)] = geom
            #scalars = self.session.control_panel.scalars_editor
            #current.controls["scalars"] = scalars

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
            logger.debug("Close Project")
        elif self.session.current_is_script():
            logger.debug("Close Scripts")
            
        self.session._project = None
        self.session._is_script = False
        self.session._is_proj = False
        
        self._scene_change()
        self._control_change()
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
            self._control_change()
            self._script_change()
            self._tree_view_change()
        elif self.session.current_is_script():
            self._tree_view_change()
            #self._script_change()
        else:
            pass
            
    def _control_change(self):
        logger.debug("Control changed")
        if self.session.current_is_project():
            proj = self.session.project
            if not proj.controls.has_key("color map"):    
                proj.controls["color map"] = PglTurtle().getColorList()
                logger.debug("Load colormap %s"%(geom))
            # Link with color map from application
            i = 0
            for color in proj.controls["color map"]:
                self.session.control_panel.colormap_editor.getTurtle().setMaterial(i, color)
                i += 1
            
            managers = get_managers()
            geom = self.session.control_panel.geometry_editor.getObjects()
            
            for control in proj.controls:
                if "geometry" in str(control).split("_")[0]:
                    type_name = str(control).split("_")[1]
                    manager = managers[type_name]
                    proj.controls[control].name = str(control).split("_")[-1]
                    geom.append((manager,proj.controls[control]))

            self.session.control_panel.geometry_editor.setObjects(geom)
            logger.debug("Load controls %s"%(geom))

            
            
            #i = 0
            #for scalar in proj.controls["scalars"]:
            #    self.session.control_panel.scalars_editor
            #    i += 1
            
            #newcontrols = self.session.control_panel_manager.get_managers()
            #for controlname in newcontrols:
            #    proj.controls[controlname] = newcontrols[controlname]
            
        
    def _tree_view_change(self):
        logger.debug("Tree View changed")
        self.session.project_layout_widget.update()
        
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
        self.session.scene_widget.getScene().reset()
        if self.session.current_is_project():
            project = self.session.project
            for w in project.scene:
                self.session.scene_widget.getScene().add(name=w,obj=project.scene[w])
