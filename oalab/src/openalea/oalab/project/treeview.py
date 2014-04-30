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
from openalea.oalab.gui import resources_rc
import os

class ProjectLayoutWidget(QtGui.QWidget):
    """
    Widget to display the name of the current project AND the project
    """
    def __init__(self, session, controller, parent=None):
        super(ProjectLayoutWidget, self).__init__(parent=parent) 
        self.session = session
        self.treeview = ProjectTreeView(self.session, controller, parent)
        self.label = ProjectLabel(self.session, controller, parent)
        
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
    def __init__(self, session, controller, parent=None):
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
    def __init__(self, session, controller, parent=None):
        super(ProjectTreeView, self).__init__(parent) 
        #self.setIconSize(QtCore.QSize(30,30))
        self.session = session
        self.controller = controller
        
        if self.session.current_is_project():
            self.project = self.session.project
        else:
            self.project = None
            
        self.projectview = QtGui.QWidget()
        
        # project tree view
        self.proj_model = PrjctModel(session, controller, self.project)
        
        self.setHeaderHidden(True)
        self.setModel(self.proj_model)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self,QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),self.showMenu)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        QtCore.QObject.connect(self,QtCore.SIGNAL('doubleClicked(const QModelIndex&)'),self.on_opened_file)
        
    def update(self):
        self.reinit_treeview()
        
    def reinit_treeview(self):
        """ Reinitialise project view """
        
        if self.session.project:
            self.project = self.session.project
        else:
            self.project = None
        self.proj_model.set_proj(self.project)
        self.expandAll()
        
    def create_menu(self):
        menu = QtGui.QMenu(self)

        if self.controller.applet_container:
            for applet in self.controller.applet_container.paradigms.values():
                action = QtGui.QAction('New %s'%applet.default_name, self)
                action.triggered.connect(self.controller.applet_container.new_file)
                menu.addAction(action)
            menu.addSeparator()

            # If a file is selected
            # Permit to open it
            if self.project:
                item = self.getItem()
                if self.hasParent():
                    if item.parent().parent():
                        editAction = QtGui.QAction('Open File',self)
                        editAction.triggered.connect(self.open_file)
                        menu.addAction(editAction)
                        menu.addSeparator()

        if self.controller.project_manager:
            editMetadataAction = QtGui.QAction('Edit/Show Metadata',self)
            editMetadataAction.triggered.connect(self.controller.project_manager.edit_metadata)
            menu.addAction(editMetadataAction)
            menu.addSeparator()


            # importAction = QtGui.QAction('Import Model',self)
            # importAction.triggered.connect(self.controller.applet_container.importFile)
            # menu.addAction(importAction)
            #removeAction = QtGui.QAction('Remove Model',self)
            #removeAction.triggered.connect(self.controller.project_manager.removeModel)
            #menu.addAction(removeAction)
            # menu.addSeparator()
            # renameAction = QtGui.QAction('Rename Project',self)
            # renameAction.triggered.connect(self.controller.applet_container.renameCurrent)
            # menu.addAction(renameAction)
        return menu

    def on_opened_file(self):
        # If a file is selected
            # Permit to open it
            if self.project:
                item = self.getItem()
                if self.hasParent():
                    if item.parent().parent():
                        self.open_file()

    def open_file(self):
        item = self.getItem()
        filename = path(self.project.path)/self.project.name/item.parent().text()/item.text()
        self.controller.applet_container.open_file(filename=filename)


    def showMenu(self, event):
        """ function defining actions to do according to the menu's button chosen"""
        menu = self.create_menu()
        menu.exec_(self.mapToGlobal(event))

    def hasSelection(self):
        """function hasSelection: check if an object is selected, return True in this case"""
        return self.selectionModel().hasSelection()
        
    def hasParent(self):
        return bool(self.getParent())

    def getParent(self):
        if self.hasSelection():
            item = self.getItem()
            if item:
                parent = item.parent()
                return parent
        return None

    def getItem(self):
        if self.hasSelection():
            index = self.selectedIndexes()[0]
            item = index.model().itemFromIndex(index)
            return item
        return None

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
    def __init__(self, session, controller, project, parent=None):
        super(PrjctModel, self).__init__(parent)
        
        # Use it to store evrything to compare with new when a change occure
        self.controller = controller
        
        self.old_models = list()
        self.old_control = list()
        self.old_scene = list()
        
        self.proj = None
        self.set_proj(project)      

        #QtCore.QObject.connect(self,QtCore.SIGNAL('dataChanged( const QModelIndex &, const QModelIndex &)'),self.renamed)
        
        self.icons = dict()
        for applet in self.controller.applet_container.paradigms.values():
            self.icons[applet.extension] = applet.icon
        
    def renamed(self,x,y):
        if self.proj is not None:
            if self.proj.is_project():
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
                                self.proj.rename(category=parent.text(), old_name=i, new_name= item.text())

                    if parent.text() == "Control":
                        for i in children:
                            if i not in self.old_control:
                                self.proj.rename(category=parent.text(), old_name=i, new_name= item.text())

                    if parent.text() == "Scene":
                        for i in children:
                            if i not in self.old_scene:
                                self.proj.rename(category=parent.text(), old_name=i, new_name= item.text())
                                
                    # Save project
                    self.proj.save()
        

    def set_proj(self, proj=None):
        self.clear()
        
        if proj is not None:
            self.proj = proj
            self._set_levels()


    def _set_levels(self):

        icon_project = QtGui.QIcon(":/images/resources/openalea_icon2.png")
        icon_src = QtGui.QIcon(":/images/resources/filenew.png")
        icon_control = QtGui.QIcon(":/images/resources/node.png")
        icon_scene = QtGui.QIcon(":/images/resources/plant.png")
        icon_startup = QtGui.QIcon(":/images/resources/editredo.png")
        icon_data = QtGui.QIcon(":/images/resources/fileopen.png")
        icon_doc = QtGui.QIcon(":/images/resources/book.png")
        icon_cache = QtGui.QIcon(":/images/resources/editcopy.png")

        project = self.proj
        name = project.name
        parentItem = self.invisibleRootItem()
        item = QtGui.QStandardItem(name)

        files = project.files

        # Propose icon by default.
        # If project have another one, use it
        icon = icon_project
        if hasattr(project, "icon"):
            icon_name = project.icon
            if len(icon_name):
                if icon_name[0] is not ":":
                    #local icon
                    icon_name = path(project.path)/name/icon_name
                    #else native icon from oalab.gui.resources
                icon = QtGui.QIcon(icon_name)
        item.setIcon(icon)
        parentItem.appendRow(item)

        categories = files.keys()
        for category in categories:
            if hasattr(project, category):
                cat = getattr(project, category)
                if len(cat) > 0:
                    item2 = QtGui.QStandardItem(category)
                    item.appendRow(item2)
                    try:
                        icon = eval(str("icon_"+category))
                    except NameError:
                        icon = QtGui.QIcon()
                    item2.setIcon(icon)
                else:
                    # hide name of category if we don't have object of this category
                    pass

                if isinstance(cat,dict):
                    for obj in cat.keys():
                        item3 = QtGui.QStandardItem(obj)
                        if category == "src":
                            ext = obj.split(".")[-1]
                            if ext in self.icons.keys():
                                item3.setIcon(QtGui.QIcon(self.icons[ext]))
                        item2.appendRow(item3)
                else:
                    # Useful for category "localized" which store a bool and not a list
                    item3 = QtGui.QStandardItem(cat)
                    item2.appendRow(item3)


class PrjctManagerModel(QtGui.QStandardItemModel):
    """
    Item model to use TreeView with the project manager.
    
    Use: 

        from openalea.vpltk.project.manager import ProjectManager
        import sys
        app = QtGui.QApplication(sys.argv)
        
        project_manager = ProjectManager()
        project_manager.discover()

        # Model to transform a project into a tree
        proj_model = PrjctManagerModel(project_manager)

        # Create tree view and set model
        treeView = QtGui.QTreeView()
        treeView.setModel(proj_model)
        treeView.expandAll()

        # Display
        treeView.show()
        app.exec_()
    """
    def __init__(self, project_manager, parent=None):
        super(PrjctManagerModel, self).__init__(parent)
        self.projects = []
        self.set_proj_manag(project_manager)      

    def set_proj_manag(self, project_manager):
        self.clear()
        project_manager.discover()
        self.projects = project_manager.projects
        self._set_levels()

    def _set_levels(self):
        icon_project = QtGui.QIcon(":/images/resources/openalea_icon2.png")
        icon_src = QtGui.QIcon(":/images/resources/filenew.png")
        icon_control = QtGui.QIcon(":/images/resources/node.png")
        icon_scene = QtGui.QIcon(":/images/resources/plant.png")
        icon_startup = QtGui.QIcon(":/images/resources/editredo.png")
        icon_data = QtGui.QIcon(":/images/resources/fileopen.png")
        icon_doc = QtGui.QIcon(":/images/resources/book.png")
        icon_cache = QtGui.QIcon(":/images/resources/editcopy.png")

        for project in self.projects:
            name = project.name
            parentItem = self.invisibleRootItem()
            item = QtGui.QStandardItem(name)

            files = project.files
            
            # Propose icon by default.
            # If project have another one, use it
            icon = icon_project
            if hasattr(project, "icon"):
                icon_name = project.icon
                if len(icon_name):
                    if icon_name[0] is not ":":
                        #local icon
                        icon_name = path(project.path)/name/icon_name
                        #else native icon from oalab.gui.resources
                    icon = QtGui.QIcon(icon_name)

            item.setIcon(icon)
            parentItem.appendRow(item)
                        
            categories = files.keys()
            for category in categories:
                if hasattr(project, category):
                    cat = getattr(project, category)
                    if len(cat) > 0:
                        item2 = QtGui.QStandardItem(category)
                        item.appendRow(item2)
                        try:
                            icon = eval(str("icon_"+category))
                        except NameError:
                            icon = QtGui.QIcon()
                        item2.setIcon(icon)
                    else:
                        # hide name of category if we don't have object of this category
                        pass
                
                    
                    if isinstance(cat,dict):
                        for obj in cat.keys():
                            item3 = QtGui.QStandardItem(obj)

                            # ext = obj.split(".")[-1]
                            # if ext in self.icons.keys():
                            #     item.setIcon(QtGui.QIcon(self.icons[ext]))


                            item2.appendRow(item3)
                    else:    
                        # Useful for category "localized" which store a bool and not a list
                        item3 = QtGui.QStandardItem(cat)
                        item2.appendRow(item3)

    def _set_level_0_only(self):
        """
        Use it if you just want to see projects path
        """                   
        for name in self.projects:
            parentItem = self.invisibleRootItem()
            item = QtGui.QStandardItem(name)
            parentItem.appendRow(item)


def main():
    from openalea.vpltk.project.manager import ProjectManager
    import sys
    app = QtGui.QApplication(sys.argv)
    
    project_manager = ProjectManager()

    # Model to transform a project into a tree
    proj_model = PrjctManagerModel(project_manager)

    # Create tree view and set model
    treeView = QtGui.QTreeView()
    treeView.setModel(proj_model)
    #treeView.expandAll()

    # Display
    treeView.show()
    app.exec_()

if __name__ == "__main__":
    main()
