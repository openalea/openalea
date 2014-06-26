# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
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

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener
from openalea.vpltk.project import ProjectManager
from openalea.oalab.gui import resources_rc
from openalea.oalab.service.applet import get_applet
from openalea.oalab.gui.utils import qicon
from openalea.oalab.project.pretty_preview import ProjectSelectorScroll
from openalea.oalab.project.creator import CreateProjectWidget
from openalea.oalab.gui.utils import ModalDialog
from openalea.core.path import path
from openalea.core import settings
from openalea.vpltk.project.project import remove_extension

from openalea.oalab.project.manager import SelectCategory, RenameModel

"""
TODO:
    - use project known categories instead of hard coded 'model', 'src', ...

"""

class ProjectManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.view = ProjectManagerView()
        self.model = self.view.model()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        self.projectManager = ProjectManager()
        self.projectManager.register_listener(self)

        self.paradigm_container = None
        self.menu_available_projects = QtGui.QMenu(u'Available Projects')

#         self.actionRenameProject.triggered.connect(self.rename)

        group = "Project"
        self._actions = [[group, "Manage Project", self.view.actionNewProj, 0],
                         [group, "Manage Project", self.view.actionOpenProj, 0],
                         [group, "Manage Project", self.view.actionSaveProj, 0],
                         [group, "Manage Project", self.view.actionSaveProjAs, 1],
                         [group, "Manage Project", self.view.actionCloseProj, 0],
                         [group, "Manage Project", self.view.actionEditMeta, 1],
                         [group, "Manage Project", self.view.actionAddFile, 0],
#                          ["Project", "Manage Project", self.actionRenameProject, 1],
        ]

        # Menu used to display all available projects.
        # This menu is filled dynamically each time this menu is opened
        self.menu_available_projects = QtGui.QMenu(u'Available Projects')
        self.menu_available_projects.aboutToShow.connect(self.view._update_available_project_menu)


    def initialize(self):
        self.view.initialize()
        self.view.update()

    def actions(self):
        return self._actions

    def set_project(self, project):
        self.projectManager.cproject = project
        self.view.reset()

    def notify(self, sender, event=None):
        signal, data = event
        project = self.projectManager.cproject
        if signal == 'project_changed':
            self.set_project(project)
        elif signal == 'project_updated':
            self.view.refresh()

class ProjectManagerView(QtGui.QTreeView):
    def __init__(self):
        QtGui.QTreeView.__init__(self)
        self.paradigm_container = None

        self._model = ProjectManagerModel()
        self.projectManager = ProjectManager()
        self.setModel(self._model)

        self._model.dataChanged.connect(self._on_model_changed)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.connect(self, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.openIndex)

        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self.actionNewProj = QtGui.QAction(qicon("new.png"), "New Project", self)
        self.actionNewProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(qicon("open.png"), "Open Project", self)
        self.actionOpenProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(qicon("save.png"), "Save project", self)
        self.actionSaveProjAs = QtGui.QAction(qicon("save.png"), "Save As", self)
        self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(qicon("closeButton.png"), "Close project", self)
        self.actionEditMeta = QtGui.QAction(qicon("book.png"), "Edit Metadata", self)
        self.actionAddFile = QtGui.QAction(qicon("bool.png"), "Add model to current Project", self)
        self.actionRenameProject = QtGui.QAction(qicon("editpaste.png"), "Rename Project", self)
        self.actionRenameModel = QtGui.QAction(qicon("editcopy.png"), "Rename Model", self)

        self.actionNewProj.triggered.connect(self.new)
        self.actionOpenProj.triggered.connect(self.open)
        self.actionSaveProjAs.triggered.connect(self.saveAs)
        self.actionSaveProj.triggered.connect(self.save)
        self.actionCloseProj.triggered.connect(self.close)
        self.actionEditMeta.triggered.connect(self.edit_metadata)
        self.actionAddFile.triggered.connect(self.add_current_file)

        self.action_available_project = {} # Dict used to know what project corresponds to triggered action


    def initialize(self):
        self.paradigm_container = get_applet(identifier='EditorManager')

    def reset(self):
        project = self.project()
        if project:
            self.close_all_scripts()
            if project.state != 'loaded':
                project.load()
            self.open_all_scripts_from_project(project)
        else:
            self.close_all_scripts()

        self._model.set_project(project)

        # TODO: Dirty hack to remove asap. Close project selector if widget has been created
        if hasattr(self, "proj_selector"):
            self.proj_selector.close()
            del self.proj_selector

    def refresh(self):
        self._model.refresh()

    def _on_model_changed(self):
        self.expandAll()

    def project(self):
        if self.projectManager:
            return self.projectManager.cproject

    def open(self, name=False, path=None):
        """
        If name==false, display a widget to choose project to open.
        Then open project.
        """
        self.projectManager.discover()
        projects = self.projectManager.projects
        self.proj_selector = ProjectSelectorScroll(projects=projects, open_project=self.set_project)
        self.proj_selector.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.proj_selector.show()

    def close(self):
        self.projectManager.cproject = None

    def new(self):
        project_creator = CreateProjectWidget()
        dialog = ModalDialog(project_creator)
        if dialog.exec_():
            _project = project_creator.project()
            project = self.projectManager.create(_project.name, _project.projectdir)
            project.metadata = _project.metadata

    def edit_metadata(self):
        project = self.project()
        if project:
            project_creator = CreateProjectWidget(project)
            project_creator.setMetaDataMode()
            dialog = ModalDialog(project_creator)
            if dialog.exec_():
                project.metadata = project_creator.metadata()

    def save(self):
        project = self.project()
        if project:
            project.save()

    def saveAs(self):
        project = self.project()
        if project:
            name = self.showNewProjectDialog(default_name=None, text="Select name to save project")
            if name:
                project.rename(category="project", old_name=project.name, new_name=name)

    def add_current_file(self):
        project = self.project()
        if self.paradigm_container is None or project is None:
            return
        text = self.paradigm_container.tabText(self.paradigm_container.currentIndex())
        text = path(text).splitall()[-1]
        categories = ["model"]
        categories.extend(project.files.keys())
        self.selector = SelectCategory(filename=text, categories=categories)
        self.selector.show()
        self.selector.ok_button.clicked.connect(self._add_file_from_selector)

    def _add_file_from_selector(self):
        project = self.project()
        category = self.selector.combo.currentText()
        self.selector.hide()

        text = self.paradigm_container.currentWidget().get_text()
        index = self.paradigm_container.currentIndex()
        filename = self.selector.line.text()
        filename_without_ext = remove_extension(filename)
        ret = project.add(category=category, name=filename, value=text)
        if ret:
            self.paradigm_container.setTabText(index, filename_without_ext)

    def showNewProjectDialog(self, default_name=None, text=None, parent=None):
        my_path = path(settings.get_project_dir())
        if default_name:
            my_path = my_path / default_name
        if not text:
            text = 'Select name to create project'
        fname = QtGui.QFileDialog.getSaveFileName(parent, text,
                                                  my_path)
        return fname


    def showOpenProjectDialog(self, parent=None):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getExistingDirectory(parent, 'Select Project Directory',
                                                       my_path)
        return fname

    def _update_available_project_menu(self):
        """
        Discover all projects and generate an action for each one.
        Then connect this action to _on_open_project_triggered
        """
        self.projectManager.discover()
        self.menu_available_projects.clear()
        self.action_available_project.clear()
        for project in self.projectManager.projects:
            icon_path = project.icon_path
            icon_name = icon_path if icon_path else ":/images/resources/openalealogo.png"
            action = QtGui.QAction(QtGui.QIcon(icon_name), project.name, self.menu_available_projects)
            action.triggered.connect(self._on_open_project_triggered)
            self.menu_available_projects.addAction(action)
            self.action_available_project[action] = project

    def _on_open_project_triggered(self):
        project = self.action_available_project[self.sender()]
        self.projectManager.cproject = project

    def open_all_scripts_from_project(self, project):
        if self.paradigm_container is None:
            return
        models = project.models()
        if not isinstance(models, list):
            models = [models]
        for model in models:
            self.paradigm_container.open_file(model=model)

    def close_all_scripts(self):
        if self.paradigm_container is None:
            return
        self.paradigm_container.closeAll()


    def create_menu(self):
        menu = QtGui.QMenu(self)
        if self.paradigm_container:
            for applet in self.paradigm_container.paradigms.values():
                action = QtGui.QAction('New %s' % applet.default_name, self)
                action.triggered.connect(self.paradigm_container.new_file)
                menu.addAction(action)
            menu.addSeparator()

        data = None
        for index in self.selectedIndexes():
            data = self._model.projectdata(index)
        if data is None:
            return menu
        else:
            category, obj = data
            if category in ['model', 'src', 'project']:
                rename = QtGui.QAction('Rename %s' % obj, self)
                rename.triggered.connect(self.rename)
                menu.addAction(rename)

            if category in ['model', 'src']:
                editAction = QtGui.QAction('Open %s' % obj, self)
                editAction.triggered.connect(self.open)
                menu.addAction(editAction)
                menu.addSeparator()

                remove = QtGui.QAction('Remove %s' % obj, self)
                remove.triggered.connect(self.remove)
                menu.addAction(remove)

            if category in ['project']:
                editMetadataAction = QtGui.QAction('Edit/Show Metadata', self)
                editMetadataAction.triggered.connect(self.edit_metadata)
                menu.addAction(editMetadataAction)

        return menu

    def contextMenuEvent(self, event):
        if self.projectManager.cproject is None:
            return
        menu = self.create_menu()
        menu.exec_(event.globalPos())

    def open(self):
        indices = self.selectedIndexes()
        for index in indices:
            self.openIndex(index)

    def openIndex(self, index):
        data = self._model.projectdata(index)
        if data:
            category, name = data
            model = self.projectManager.cproject.get(*data)
            self.paradigm_container.open_file(model=model)

    def rename(self):
        indices = self.selectedIndexes()
        project = self.projectManager.cproject
        for index in indices:
            data = self._model.projectdata(index)
            if data and project:
                category, old_name = data

                models = project.models()
                if isinstance(models, list):
                    list_models = [mod.name for mod in models]
                else:
                    list_models = [models.name]
                renamer = RenameModel(list_models, old_name)
                dialog = ModalDialog(renamer)
                if dialog.exec_():
                    old_name = renamer.old_name()
                    new_name = renamer.new_name()
                    project.rename(category, old_name, new_name)

    def remove(self):
        indices = self.selectedIndexes()
        self._model.remove(indices)

    def getIndex(self):
        indices = self.selectedIndexes()
        for index in indices:
            return index

    def getItem(self):
        index = self.getIndex()
        if index:
            return self._model.itemFromIndex(index)

    def startDrag(self, supportedActions):
        index = self.getIndex()
        item = self.getItem()
        data = self._model.projectdata(index)
        if data is None:
            return
        category, obj = data
        # Check item in src
        # TODO move this part in dragEnterEvent with mimetype
        if category in ['src', 'model']:
            text = item.text()

            # name_without_ext = ".".join(text.split(".")[:-1])
            name_without_ext = text
            name_without_space = "_".join(name_without_ext.split())
            for sym in ["-", "+", "*", "/", "\""]:
                name_without_space = "_".join(name_without_space.split(sym))

            python_call_string = '%s = Model("%s")' % (name_without_space, name_without_ext)
            icon = item.icon()
            pixmap = icon.pixmap(20, 20)

            itemData = QtCore.QByteArray()
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
            model_id = name_without_ext
            dataStream.writeString(str(python_call_string))
            dataStream.writeString(str(model_id))

            mimeData = QtCore.QMimeData()
            mimeData.setText(python_call_string)
            mimeData.setData("openalealab/model", itemData)

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)

            drag.start(QtCore.Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalealab/model"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("openalealab/model"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        event.ignore()

class ProjectManagerModel(QtGui.QStandardItemModel):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self._data = {}
        self._root_item = None
        self._project = None

    def project_icon(self, project):
        # Propose icon by default.
        # If project have another one, use it
        icon_project = QtGui.QIcon(":/images/resources/openalea_icon2.png")
        icon = icon_project
        if hasattr(project, "icon"):
            icon_name = project.icon
            if len(icon_name):
                if icon_name[0] is not ":":
                    # local icon
                    icon_name = project.path / icon_name
                    # else native icon from oalab.gui.resources
                icon = QtGui.QIcon(icon_name)
        return icon

    def set_project(self, project):
        self._project = project
        self.refresh()

    def refresh(self):
        self.clear()
        project = self._project
        if project is None:
            return

        icons = dict(
            project=QtGui.QIcon(":/images/resources/openalea_icon2.png"),
            src=QtGui.QIcon(":/images/resources/filenew.png"),
            control=QtGui.QIcon(":/images/resources/node.png"),
            world=QtGui.QIcon(":/images/resources/plant.png"),
            startup=QtGui.QIcon(":/images/resources/editredo.png"),
            data=QtGui.QIcon(":/images/resources/fileopen.png"),
            doc=QtGui.QIcon(":/images/resources/book.png"),
            cache=QtGui.QIcon(":/images/resources/editcopy.png"),
            model=QtGui.QIcon(":/images/resources/new.png"),
        )

        name = project.name
        parentItem = self.invisibleRootItem()
        item = QtGui.QStandardItem(name)
        self._root_item = name

        files = project.files

        item.setIcon(self.project_icon(project))
        parentItem.appendRow(item)


        categories = sorted(['model'] + files.keys())
        for category in categories:
            item2 = QtGui.QStandardItem(category)
            item.appendRow(item2)

            if category in icons:
                item2.setIcon(icons[category])

            if not hasattr(project, category):
                continue

            if category == 'model':
                data_dict = project._model
            else:
                data_dict = getattr(project, category)

            names = data_dict.keys()
            for name in names:
                data = data_dict[name]
                item3 = QtGui.QStandardItem(name)
                if hasattr(data, 'icon'):
                    data_icon_path = data.icon
                else:
                    data_icon_path = ''
                item3.setIcon(QtGui.QIcon(data_icon_path))
                item3.setData((category, data))
                item2.appendRow(item3)


#         categories = files.keys()
#         for category in categories:
#             if hasattr(project, category):
#                 cat = getattr(project, category)
#                 if cat is not None:
#                     if len(cat) > 0:
#                         item2 = QtGui.QStandardItem(category)
#                         item.appendRow(item2)
#                         try:
#                             icon = eval(str("icon_" + category))
#                         except NameError:
#                             icon = QtGui.QIcon()
#                         item2.setIcon(icon)
#                 else:
#                     # hide name of category if we don't have object of this category
#                     pass
#
#                 if isinstance(cat, dict):
#                     for obj in cat.keys():
#                         l = obj.split(".")
#                         name = ".".join(l[:-1])
#                         ext = l[-1]
#                         item3 = QtGui.QStandardItem(obj)
#                         if category == "src":
#                             item3 = QtGui.QStandardItem(name)
#                             item3.setData((category, name))
#                             if ext in self.icons.keys():
#                                 item3.setIcon(QtGui.QIcon(self.icons[ext]))
#                         item2.appendRow(item3)
#                 else:
#                     # Useful for category "localized" which store a bool and not a list
#                     item3 = QtGui.QStandardItem(cat)
#                     item2.appendRow(item3)

    def projectdata(self, index):
        # use self.itemData() ?
        if index.data() in ['model', 'src']:
            return ('category', index.data())
        elif index.parent().data() in ['model', 'src']:
            return (index.parent().data(), index.data())
        elif index.data() == self._root_item:
            return ('project', index.data())
        else:
            return None

