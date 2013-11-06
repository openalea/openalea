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
from openalea.core.path import path
from openalea.core import settings
import os

class ProjectLayoutWidget(QtGui.QWidget):
    """
    Widget to display the name of the current project AND the project
    """
    def __init__(self, session):
        super(ProjectLayoutWidget, self).__init__(parent=None) 
        self.session = session
        self.treeview = ProjectTreeView(self.session)
        self.label = ProjectLabel(self.session)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.treeview)
        
        self.setLayout(layout)
        
    def clear(self):
        self.treeview.reinit_treeview()
        self.label.setText("")  
        
    def update(self):
        self.treeview.update()
        self.label.update()
        
    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return self.treeview.mainMenu()

class ProjectLabel(QtGui.QLabel):
    """
    Widget to display the name of the current project.
    """
    def __init__(self, session):
        super(ProjectLabel, self).__init__(parent=None) 
        self.session = session
        self.update()
        
    def update(self):    
        if self.session.current_is_project():
            label = self.session.project.name
        else:
            label = ""
        self.setText(label)  

class ProjectTreeView(QtGui.QTreeView):
    """
    Widget to display Tree View of project.
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
        
    def update(self):
        self.reinit_treeview()
        
    def reinit_treeview(self):
        """ Reinitialise project view """
        
        if self.session.current_is_project():
            self.project = self.session.project
        else:
            self.project = None
        self.proj_model.set_proj(self.project)
        self.expandAll()



    def create_menu_actions(self):
        self.newPyAction = QtGui.QAction('New Python Model',self)
        QtCore.QObject.connect(self.newPyAction,QtCore.SIGNAL('triggered(bool)'),self.session.project_widget.newPython)
        self.newLPyAction = QtGui.QAction('New L-System Model',self)
        QtCore.QObject.connect(self.newLPyAction,QtCore.SIGNAL('triggered(bool)'),self.session.project_widget.newLpy)
        self.newWFAction = QtGui.QAction('New Workflow Model',self)
        QtCore.QObject.connect(self.newWFAction,QtCore.SIGNAL('triggered(bool)'),self.session.project_widget.newVisualea)
        self.newRAction = QtGui.QAction('New R Model',self)
        QtCore.QObject.connect(self.newRAction,QtCore.SIGNAL('triggered(bool)'),self.session.project_widget.newR)
        
        self.addPyAction = QtGui.QAction('Import Python Model',self)
        QtCore.QObject.connect(self.addPyAction,QtCore.SIGNAL('triggered(bool)'),self._addPy)
        self.addLPyAction = QtGui.QAction('Import L-System Model',self)
        QtCore.QObject.connect(self.addLPyAction,QtCore.SIGNAL('triggered(bool)'),self._addLPy)
        self.addWFAction = QtGui.QAction('Import Workflow Model',self)
        QtCore.QObject.connect(self.addWFAction,QtCore.SIGNAL('triggered(bool)'),self._addWorkflow)        
        self.addRAction = QtGui.QAction('Import R Model',self)
        QtCore.QObject.connect(self.addRAction,QtCore.SIGNAL('triggered(bool)'),self._addR)  
                
        #self.renameAction = QtGui.QAction('Rename',self)
        #QtCore.QObject.connect(self.renameAction,QtCore.SIGNAL('triggered(bool)'),self.renameSelection)
        
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
        menu.addAction(self.newPyAction)
        menu.addAction(self.newLPyAction)
        menu.addAction(self.newWFAction)
        menu.addAction(self.newRAction)      
        menu.addSeparator()
        menu.addAction(self.addPyAction)
        menu.addAction(self.addLPyAction)
        menu.addAction(self.addWFAction)   
        menu.addAction(self.addRAction)   
        #menu.addSeparator()
        #menu.addAction(self.renameAction)  
        
        
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
        #self.renameAction.setEnabled(self.hasParent())        
        menu.exec_(self.mapToGlobal(event))

    def showFileDialog(self, format):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select Project Directory', 
                my_path, format)
        return fname


    #def renameSelection(self):
        #""" rename an object in the list """
        #index = self.selectedIndexes()[0]
        #item = index.model().itemFromIndex(index)
        #name = str(item.text())
        
        #parent = item.parent()
        #parent_name = str(parent.text())

        #print name, parent_name

            
        ##self.model().item...
            
        #self.emit(QtCore.SIGNAL('renameRequest(int)'),self.selection)

    def hasSelection(self):
        """function hasSelection: check if an object is selected, return True in this case"""
        return self.selectionModel().hasSelection()
        
    def hasParent(self):
        if self.hasSelection():
            index = self.selectedIndexes()[0]
            item = index.model().itemFromIndex(index)
            parent = item.parent()
            return bool(parent)
        else:
            return False

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
            
    def _addR(self):
        """
        Add R script in current project.
        """
        fname = self.showFileDialog("R file (*.r)")
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

    """
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
        pass"""


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
        
        # Use it to store evrything to compare with new when a change occure
        self.old_models = list()
        self.old_controls = list()
        self.old_scene = list()
        
        self.proj = None
        self.set_proj(project)      

        QtCore.QObject.connect(self,QtCore.SIGNAL('dataChanged( const QModelIndex &, const QModelIndex &)'),self.renamed)
        
    def renamed(self,x,y):
        # Get item and his parent
        parent = self.item(x.parent().row())
        # Check if you have the right to rename
        if parent:
            item = parent.child(x.row())
        
            # List brothers of item
            children = list()
            raw = parent.rowCount()
            for i in range(raw):
                child = parent.child(i)
                children.append(child.text())
            
            # Search which is the old_item which was changed and rename it
            if parent.text() == "Models":
                for i in self.old_models:
                    if i not in children:
                        self.proj.rename(categorie=parent.text(), old_name=i, new_name= item.text())

            if parent.text() == "Controls":
                for i in children:
                    if i not in self.old_controls:
                        self.proj.rename(categorie=parent.text(), old_name=i, new_name= item.text())

            if parent.text() == "Scene":
                for i in children:
                    if i not in self.old_scene:
                        self.proj.rename(categorie=parent.text(), old_name=i, new_name= item.text())
                        
            # Save project
            self.proj.save()
        

    def set_proj(self, proj=None):
        self.clear()
        
        if proj is not None:
            self.proj = proj
            self._set_level_0()
            self._set_level_1()

    def _set_level_0(self):
        ## TODO if you want to see all objects of the project
        level0 = ["Models", "Controls", "Scene"]       
                            
        for name in level0:
            parentItem = self.invisibleRootItem()
            item = QtGui.QStandardItem(name)
            if name == "Controls": icon = QtGui.QIcon(":/images/resources/node.png")
            elif name == "Scene": icon = QtGui.QIcon(":/images/resources/flower.ico")
            elif name == "Models": icon = QtGui.QIcon(":/images/resources/package.png")
            item.setIcon(icon)
            parentItem.appendRow(item)

            
    def _set_level_1(self):
        self.old_models = list()
        self.old_controls = list()
        self.old_scene = list()
        
        rootItem = self.invisibleRootItem()
        
        # Controls
        parentItem = rootItem.child(1)
        for name in self.proj.controls:
            item = QtGui.QStandardItem(name)
            item.setIcon(QtGui.QIcon(":/images/resources/bool.png"))
            #parentItem.appendRow(item)    
            self.old_controls.append(name)
             
        # Models
        parentItem = rootItem.child(0)
        for name in self.proj.scripts:
            item = QtGui.QStandardItem(name)
            if name.split(".")[-1] == "wpy":
                item.setIcon(QtGui.QIcon(":/images/resources/openalealogo.png"))
            elif name.split(".")[-1] == "py":
                item.setIcon(QtGui.QIcon(":/images/resources/Python-logo.png"))
            elif name.split(".")[-1] == "r":
                item.setIcon(QtGui.QIcon(":/images/resources/RLogo.png"))
            elif name.split(".")[-1] == "lpy":
                item.setIcon(QtGui.QIcon(":/lpy_images/resources/lpy/logo.png"))
            else:
                item.setIcon(QtGui.QIcon(":/images/resources/openalea_icon2.png"))
            parentItem.appendRow(item)
            self.old_models.append(name)
        
        # Scene
        parentItem = rootItem.child(2)
        for name in self.proj.scene:
            item = QtGui.QStandardItem(name)
            item.setIcon(QtGui.QIcon(":/images/resources/plant.png"))
            parentItem.appendRow(item) 
            self.old_scene.append(name)
