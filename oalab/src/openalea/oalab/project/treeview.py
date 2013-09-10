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

"""
Display a tree view of the project in oalab
"""

__revision__ = "$Id: "

from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import to_qvariant
from openalea.oalab.gui import resources_rc
from openalea.core.path import path
from openalea.core import settings
import os


class ProjectTreeView(QtGui.QTreeView):
    """
    Tab Widget to display Tree View of project.
    """
    def __init__(self, session):
        super(ProjectTreeView, self).__init__() 
        #self.setIconSize(QtCore.QSize(30,30))
        self.session = session
        
        if self.session.current_is_project():
            self.project = self.session.project
        else:
            self.project = None
            
        self.projectview = QtGui.QWidget()
        
        # project tree view
        self.proj_model = PrjctModel(self.project)
        
        self.setHeaderHidden(True)
        self.setModel(self.proj_model)
        
        
        self.create_menu_actions()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self,QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),self.showMenu)


    def reinit_treeview(self):
        """ Reinitialise project view """
        
        if self.session.current_is_project():
            self.project = self.session.project
        else:
            self.project = None
        self.proj_model.set_proj(self.project)
        self.expandAll()



    def create_menu_actions(self):
        self.addPyAction = QtGui.QAction('Add Python Model',self)
        QtCore.QObject.connect(self.addPyAction,QtCore.SIGNAL('triggered(bool)'),self._addPy)
        self.addLPyAction = QtGui.QAction('Add L-System Model',self)
        QtCore.QObject.connect(self.addLPyAction,QtCore.SIGNAL('triggered(bool)'),self._addLPy)
        self.addWFAction = QtGui.QAction('Add Workflow Model',self)
        QtCore.QObject.connect(self.addWFAction,QtCore.SIGNAL('triggered(bool)'),self._addWorkflow)        
        
        self.renameAction = QtGui.QAction('Rename',self)
        QtCore.QObject.connect(self.renameAction,QtCore.SIGNAL('triggered(bool)'),self.renameSelection)
        
##        # actions on Models
##        self.newAction = QtGui.QAction('New Model',self)
##        QtCore.QObject.connect(self.newAction,QtCore.SIGNAL('triggered(bool)'),self._newModel)
##        self.editAction = QtGui.QAction('Edit Model',self)
##        QtCore.QObject.connect(self.editAction,QtCore.SIGNAL('triggered(bool)'),self._editModel)
##        self.renameAction = QtGui.QAction('Rename Model',self)
##        QtCore.QObject.connect(self.renameAction,QtCore.SIGNAL('triggered(bool)'),self._renameModel)
##        self.delAction = QtGui.QAction('Delete Model',self)
##        QtCore.QObject.connect(self.delAction,QtCore.SIGNAL('triggered(bool)'),self._delModel)
##
##        # actions on Controls
##        self.newCtrlAction = QtGui.QAction('New Control',self)
##        QtCore.QObject.connect(self.newCtrlAction,QtCore.SIGNAL('triggered(bool)'),self._newCtrlModel)
##        self.editCtrlAction = QtGui.QAction('Edit Control',self)
##        QtCore.QObject.connect(self.editCtrlAction,QtCore.SIGNAL('triggered(bool)'),self._editCtrlModel)
##        self.renameCtrlAction = QtGui.QAction('Rename Control',self)
##        QtCore.QObject.connect(self.renameCtrlAction,QtCore.SIGNAL('triggered(bool)'),self._renameCtrlModel)
##        self.delCtrlAction = QtGui.QAction('Delete Control',self)
##        QtCore.QObject.connect(self.delCtrlAction,QtCore.SIGNAL('triggered(bool)'),self._delCtrlModel)
##        
##        # actions on Scene
##        self.newSceneCpAction = QtGui.QAction('Hide/Show Scene Component',self)
##        QtCore.QObject.connect(self.newSceneCpAction,QtCore.SIGNAL('triggered(bool)'),self._newSceneCpModel)
##        self.renameSceneCpAction = QtGui.QAction('Rename Scene Component',self)
##        QtCore.QObject.connect(self.renameSceneCpAction,QtCore.SIGNAL('triggered(bool)'),self._renameSceneCpModel)
##        self.delSceneCpAction = QtGui.QAction('Delete Scene Component',self)
##        QtCore.QObject.connect(self.delSceneCpAction,QtCore.SIGNAL('triggered(bool)'),self._delSceneCpModel)


    def create_menu(self):
        menu = QtGui.QMenu(self)
        menu.addAction(self.addPyAction)
        menu.addAction(self.addLPyAction)
        menu.addAction(self.addWFAction)      
        menu.addAction(self.renameAction)  
        
        
##        menu.addAction(self.newAction)
##        menu.addAction(self.editAction)
##        menu.addAction(self.renameAction)
##        menu.addAction(self.delAction)
##        menu.addSeparator()
##        menu.addAction(self.newCtrlAction)
##        menu.addAction(self.editCtrlAction)
##        menu.addAction(self.renameCtrlAction)
##        menu.addAction(self.delCtrlAction)
##        menu.addSeparator()
##        menu.addAction(self.newSceneCpAction)
##        menu.addAction(self.renameSceneCpAction)
##        menu.addAction(self.delSceneCpAction)
        
        return menu
        

    def showMenu(self, event):
        """ function defining actions to do according to the menu's button chosen"""
        menu = self.create_menu()
        
##        print self.selectionModel()
##        print self.selectionModel()
##        .itemFromIndex()
        self.renameAction.setEnabled(self.hasSelection())        
        
        menu.exec_(self.mapToGlobal(event))

    def showFileDialog(self, format):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select Project Directory', 
                my_path, format)
        return fname


    def renameSelection(self):
        """ rename an object in the list """
        pass
##        if self.hasSelection() :
##            self.emit(QtCore.SIGNAL('renameRequest(int)'),self.selection)

    def hasSelection(self):
        """function hasSelection: check if an object is selected, return True in this case"""
        return self.selectionModel().hasSelection()

    def _addPy(self):
        """
        Add python script in current project.
        
        1) Open File Dialog
        2) Select File
        3) Open File
        4) Add file in project
        """
        fname = self.showFileDialog("Python file (*.py)")
        if fname:
            script = open(fname, 'rU').read()

            name = os.path.split(fname)[1]
            self.project.add_script(name, script)
          
            # TODO : Use signals !
            self.session.project_widget._project_changed()

    def _addLPy(self):
        """
        Add lpy script in current project.
        """
        fname = self.showFileDialog("LPy file (*.lpy)")
        if fname:
            script = open(fname, 'rU').read()

            name = os.path.split(fname)[1]
            self.project.add_script(name, script)
          
            # TODO : Use signals !
            self.session.project_widget._project_changed()

    def _addWorkflow(self):
        """
        Add workflow in current project.
        """
        fname = self.showFileDialog("Visualea file (*.wpy)")
        if fname:
            script = open(fname, 'rU').read()

            name = os.path.split(fname)[1]
            self.project.add_script(name, script)
          
            # TODO : Use signals !
            self.session.project_widget._project_changed()

    def _newModel(self):
        pass

    def _editModel(self):
        pass

    def _renameModel(self):
        pass

    def _delModel(self):
        pass


    def _newCtrlModel(self):
        pass

    def _editCtrlModel(self):
        pass

    def _renameCtrlModel(self):
        pass

    def _delCtrlModel(self):
        pass


    def _newSceneCpModel(self):
        pass

    def _renameSceneCpModel(self):
        pass

    def _delSceneCpModel(self):
        pass


    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Project"  


class PrjctModel(QtGui.QStandardItemModel):
    """
    Item model to use TreeView with a project.
    
    Use:
    
    # Project to display
    project = ...

    # Model to transform a project into a tree
    proj_model = PrjctModel(project)

    # Create tree view and set model
    treeView = QtGui.QTreeView()
    treeView.setModel(proj_model)
    
    # Display
    treeView.show()
    """
    def __init__(self, project, parent=None):
        super(PrjctModel, self).__init__(parent)
        
        self.proj = None
        self.set_proj(project)

    def set_proj(self, proj=None):
        self.clear()
        
        if proj is not None:
            self.proj = proj
            self._set_level_0()
            self._set_level_1()

    def _set_level_0(self):
        level0 = ["Controls", "Models", "Scene"]
                            
        for name in level0:
            parentItem = self.invisibleRootItem()
            item = QtGui.QStandardItem(name)
            if name == "Controls": icon = QtGui.QIcon(":/images/resources/node.png")
            elif name == "Scene": icon = QtGui.QIcon(":/images/resources/flower.ico")
            elif name == "Models": icon = QtGui.QIcon(":/images/resources/package.png")
            item.setIcon(icon)
            parentItem.appendRow(item)

            
    def _set_level_1(self):
        rootItem = self.invisibleRootItem()
        
        # Controls
        parentItem = rootItem.child(0)
        for name in self.proj.controls:
            item = QtGui.QStandardItem(name)
            item.setIcon(QtGui.QIcon(":/images/resources/bool.png"))
            parentItem.appendRow(item)    
             
        # Models
        parentItem = rootItem.child(1)
        for name in self.proj.scripts:
            item = QtGui.QStandardItem(name)
            item.setIcon(QtGui.QIcon(":/images/resources/openalea_icon2.png"))
            parentItem.appendRow(item)
        
        # Scene
        parentItem = rootItem.child(2)
        for name in self.proj.scene:
            item = QtGui.QStandardItem(name)
            item.setIcon(QtGui.QIcon(":/images/resources/plant.png"))
            parentItem.appendRow(item) 
