# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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
TODO:
    - use project known categories instead of hard coded 'model', 'src', ...

"""
from openalea.core.observer import AbstractListener
from openalea.core.path import path
from openalea.core.service.project import (projects, set_active_project)
from openalea.core.settings import get_default_home_dir
from openalea.oalab.project.dialog import rename_model, edit_metadata, new_project
from openalea.oalab.project.selector import ProjectSelector
from openalea.oalab.project.qtmodel import ProjectModel
from openalea.oalab.project.preview import DEFAULT_PROJECT_ICON
from openalea.oalab.utils import ModalDialog, qicon, obj_icon
from openalea.oalab.widget import resources_rc
from openalea.vpltk.qt import QtGui, QtCore


class ProjectBrowserWidget(QtGui.QWidget):
    item_added = QtCore.Signal(object, str, str) # project, category, name
    item_clicked = QtCore.Signal(object, str, str) # project, category, name
    item_double_clicked = QtCore.Signal(object, str, str) # project, category, name
    item_removed = QtCore.Signal(object, str, object) # project, category, item
    project_closed = QtCore.Signal(object) # old project
    project_open = QtCore.Signal(object) # new project

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.view = ProjectBrowserView()
        self._transfer_view_signals()

        self.model = self.view.model()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        self._create_actions()
        self._create_menus()

    def closeEvent(self, event):
        self.write_settings()
        event.accept()

    def _transfer_view_signals(self):
        self.view.item_added.connect(self.item_added)
        self.view.item_clicked.connect(self.item_clicked.emit)
        self.view.item_double_clicked.connect(self.item_double_clicked.emit)
        self.view.item_removed.connect(self.item_removed)
        self.view.project_closed.connect(self.project_closed.emit)
        self.view.project_open.connect(self.project_open.emit)

    def _create_actions(self):
        self.actionNewProj = QtGui.QAction(qicon("new.png"), "New Project", self)
        self.actionNewProj.triggered.connect(self.new_project)
        self.actionNewProj.setShortcut(self.tr("Ctrl+Shift+N"))

        group = "Project"
        self._actions = [[group, "Manage Project", self.actionNewProj, 0],
                         [group, "Manage Project", self.view.actionOpenProj, 0],
                         [group, "Manage Project", self.view.actionCloseProj, 0],
                         [group, "Manage Project", self.view.actionEditMeta, 1],
                         ]
        self._actions += self.view._actions

    def _create_menus(self):
        # Menu used to display all available projects.
        # This menu is filled dynamically each time this menu is opened
        self.menu_available_projects = QtGui.QMenu(u'Available Projects')
        self.menu_available_projects.aboutToShow.connect(self._update_available_project_menu)
        self.action_available_project = {}  # Dict used to know what project corresponds to triggered action

    def project(self):
        return self.view.project()

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self._actions

    def toolbars(self):
        actions = [action[2] for action in self._actions]
        toolbar = QtGui.QToolBar("Project")
        toolbar.addActions(actions)
        return [toolbar]

    def menus(self):
        actions = [action[2] for action in self.toolbar_actions()]
        menu = QtGui.QMenu('File', self)
        menu.addActions(actions)
        menu.addSeparator()
        menu.addMenu(self.menu_available_projects)
        return [menu]

    def _update_available_project_menu(self):
        """
        Discover all projects and generate an action for each one.
        Then connect this action to _on_open_project_triggered
        """
        self.menu_available_projects.clear()
        self.action_available_project.clear()

        all_projects = {}  # dict parent dir -> list of Project objects
        for project in projects():
            all_projects.setdefault(project.projectdir, []).append(project)

        home = path(get_default_home_dir())
        for projectdir, _projects in all_projects.iteritems():
            relpath = home.relpathto(projectdir)
            title = unicode(relpath)
            menu = QtGui.QMenu(title, self.menu_available_projects)
            for project in sorted(_projects, key=lambda project: project.title):
                icon = obj_icon(project, default=DEFAULT_PROJECT_ICON, paths=[project.path])
                action = QtGui.QAction(icon, project.title, self.menu_available_projects)
                action.triggered.connect(self._on_open_project_triggered)
                menu.addAction(action)
                self.action_available_project[action] = project
            self.menu_available_projects.addMenu(menu)
        return self.menu_available_projects

    def _on_open_project_triggered(self):
        project = self.action_available_project[self.sender()]
        self.set_project(project)

    def new_project(self):
        project = new_project()
        if project is not None:
            self.set_project(project)

    def set_project(self, project):
        set_active_project(project)
        self.view.set_project(project)

    ####################################################################
    # Settings
    ####################################################################
    def write_settings(self):
        """
        Register current settings (geometry and window state)
        in a setting file
        """
        cproject = self.project()
        from openalea.core.settings import Settings
        config = Settings()
        if cproject:
            last_proj = cproject.name
            config.set("ProjectManager", "Last Project", last_proj)
        else:
            config.set("ProjectManager", "Last Project", "")

        config.write()


class ProjectBrowserView(QtGui.QTreeView, AbstractListener):
    item_added = QtCore.Signal(object, str, str) # project, category, name
    item_clicked = QtCore.Signal(object, str, str) # project, category, name
    item_double_clicked = QtCore.Signal(object, str, str) # project, category, name
    item_removed = QtCore.Signal(object, str, object) # project, category, item
    project_closed = QtCore.Signal(object) # old project
    project_open = QtCore.Signal(object) # new project

    def __init__(self):
        QtGui.QTreeView.__init__(self)
        AbstractListener.__init__(self)

        self._model = ProjectModel()

        self.setModel(self._model)
        self._model.dataChanged.connect(self._on_model_changed)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.connect(self, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.open)

        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self._create_actions()

    def _create_actions(self):
        self._actions = []

        self.actionEditMeta = QtGui.QAction(qicon("book.png"), "Edit Project Information", self)
        self.actionEditMeta.triggered.connect(self.edit_metadata)

        self.actionCloseProj = QtGui.QAction(qicon("closeButton.png"), "Close project", self)
        self.actionCloseProj.triggered.connect(self.close)
        self.actionCloseProj.setShortcut(self.tr("Ctrl+Shift+W"))

        self.actionOpenProj = QtGui.QAction(qicon("open.png"), "Open Project", self)
        self.actionOpenProj.triggered.connect(self.open_project)
        self.actionOpenProj.setShortcut(self.tr('Ctrl+Shift+O'))

    #  API
    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'project_changed':
            self.refresh()

    def set_project(self, project):
        old_proj = self._model.project()
        if old_proj:
            old_proj.unregister_listener(self)
        if project:
            project.register_listener(self)

        # TODO: Dirty hack to remove asap. Close project selector if widget has been created
        if hasattr(self, "proj_selector"):
            del self.proj_selector

        self._model.set_project(project)

        if project:
            self.project_closed.emit(old_proj)
            self.project_open.emit(project)
        else:
            self.project_closed.emit(old_proj)

    def refresh(self):
        self._model.refresh()

    #  Convenience methods

    def getItem(self):
        index = self.getIndex()
        if index:
            return self._model.itemFromIndex(index)

    def getIndex(self):
        indices = self.selectedIndexes()
        for index in indices:
            return index

    def project(self):
        return self._model.project()

    def selected_data(self):
        index = self.getIndex()
        project = self.project()
        data = self._model.projectdata(index)
        if project is None:
            return (None, None, None)
        elif project and data is None:
            return project, None, None
        else:
            category, name = data
            return project, category, name

    #  Slots

    def _on_model_changed(self):
        self.expandAll()

    #  Contextual menu

    def create_menu(self):
        menu = QtGui.QMenu(self)
        project, category, obj = self.selected_data()

        if project and category is None:
            menu.addAction(self.actionEditMeta)
            menu.addAction(self.actionCloseProj)

        elif category == 'category' and obj == 'data':
            import_data = QtGui.QAction(qicon('import.png'), 'Import data', self)
            import_data.triggered.connect(self.open)
            menu.addAction(import_data)

        if category in ['model', 'src', 'startup', 'doc', 'data', 'lib']:
            editAction = QtGui.QAction(qicon('open.png'), 'Open "%s"' % obj, self)
            menu.addAction(editAction)
            editAction.triggered.connect(self.open)

            rename = QtGui.QAction(qicon('Crystal_Clear_action_editcopy.png'), 'Rename', self)
            rename.triggered.connect(self.rename)
            menu.addAction(rename)

            remove = QtGui.QAction(qicon('Crystal_Clear_action_edit_remove.png'), 'Remove', self)
            remove.triggered.connect(self.remove)
            menu.addAction(remove)

            menu.addSeparator()

            deleteAction = QtGui.QAction(qicon('Crystal_Clear_action_stop.png'), 'Delete', self)
            menu.addAction(deleteAction)
            deleteAction.triggered.connect(self.delete)

        return menu

    def contextMenuEvent(self, event):
        if self.project() is None:
            return
        menu = self.create_menu()
        menu.exec_(event.globalPos())

    #  Action's slots

    def edit_metadata(self):
        project = self.project()
        rvalue = edit_metadata(project)
        if rvalue:
            self.refresh()

    def open_project(self, name=False, path=None):
        """
        If name==false, display a widget to choose project to open.
        Then open project.
        """
        self.proj_selector = ProjectSelector()
        dialog = ModalDialog(self.proj_selector)
        dialog.resize(800, 600)
        dialog.setContentsMargins(3, 3, 3, 3)
        if dialog.exec_():
            project = self.proj_selector.project()
            if project:
                self.set_project(project)
                set_active_project(project)

    def open(self):
        project, category, name = self.selected_data()
        if project and category:
            if category == 'category' and name == 'data':
                p = QtGui.QFileDialog.getOpenFileName(self, 'Select File to open', project.path, "All (*)")
                if p:
                    p = path(p)
                    project.add(name, path=p)
            elif category == 'category':
                pass
            elif category == 'project':
                pass
                # self.open_all_scripts_from_project(project)
            elif category == 'data':
                from openalea.file.files import start
                start(project.get(category, name).path)
            else:
                self.item_double_clicked.emit(project, category, name)

    def _rename(self, project, category, name):
        if category in project.categories:
            rename_model(project, category, name)
        elif category == 'project':
            self.edit_metadata()

    def rename(self):
        project, category, name = self.selected_data()
        if project and category:
            self._rename(project, category, name)

    def remove(self):
        project, category, name = self.selected_data()
        if project and category:
            project.remove(category, filename=name)

    def delete(self):
        project, category, name = self.selected_data()
        if project:
            if category in project.categories:
                data = project.get(category, name)

                confirm = QtGui.QLabel('Remove %s ?' % data.path)
                dialog = ModalDialog(confirm)
                if dialog.exec_():
                    project.remove(category, data)
                    data.path.remove()
                    self.item_removed.emit(project, category, data)

    def close(self):
        self.set_project(None)

    def import_file(self):
        print 'import_file'
