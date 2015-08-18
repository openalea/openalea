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

"""
TODO:
    - use project known categories instead of hard coded 'model', 'src', ...

"""
from openalea.core import settings
from openalea.core.observer import AbstractListener
from openalea.core.path import path
from openalea.core.plugin import iter_plugins
from openalea.core.service.data import DataClass, MimeType
from openalea.core.service.plugin import debug_plugin, plugins
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance, plugins
from openalea.core.service.project import write_project_settings, default_project, projects
from openalea.core.settings import get_default_home_dir
from openalea.oalab.project.creator import CreateProjectWidget
from openalea.oalab.project.pretty_preview import ProjectSelectorScroll
from openalea.oalab.service.drag_and_drop import add_drag_format, encode_to_qmimedata
from openalea.oalab.utils import ModalDialog
from openalea.oalab.utils import qicon
from openalea.oalab.widget import resources_rc
from openalea.vpltk.qt import QtGui, QtCore


class SelectCategory(QtGui.QWidget):

    def __init__(self, filename="", categories=None, dtypes=None, parent=None):
        super(SelectCategory, self).__init__(parent=parent)

        if categories is None:
            categories = Project.DEFAULT_CATEGORIES.keys()
        if dtypes is None:
            dtypes = [
                plugin.default_name for plugin in plugins(
                    'oalab.plugin',
                    criteria=dict(
                        implement='IParadigmApplet'))]
            dtypes.append('Other')
        self.categories = categories

        layout = QtGui.QFormLayout(self)

        self.label = QtGui.QLabel("Select in which category you want to add this file: ")
        self.l_dtypes = QtGui.QLabel("Data type")
        self.label2 = QtGui.QLabel("New filename: ")

        self.combo = QtGui.QComboBox(self)
        self.combo.addItems(categories)
        if 'model' in categories:
            self.combo.setCurrentIndex(categories.index('model'))

        self.combo_dtypes = QtGui.QComboBox(self)
        self.combo_dtypes.addItems(dtypes)
        self.combo_dtypes.setCurrentIndex(0)

        self.line = QtGui.QLineEdit(filename)

        layout.addRow(self.label, self.combo)
        layout.addRow(self.l_dtypes, self.combo_dtypes)
        layout.addRow(self.label2, self.line)

        self.setLayout(layout)

    def category(self):
        return str(self.combo.currentText())

    def name(self):
        return str(self.line.text())

    def dtype(self):
        return str(self.combo_dtypes.currentText())


class RenameModel(QtGui.QWidget):

    def __init__(self, models, model_name="", parent=None):
        super(RenameModel, self).__init__(parent=parent)
        self.models = models

        layout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel("Select model you want to rename: ")
        self.label2 = QtGui.QLabel("Write new name: ")
        self.combo = QtGui.QComboBox(self)
        self.combo.addItems(self.models)
        if not model_name:
            model_name = self.models[0]
        self.combo.setCurrentIndex(self.models.index(model_name))
        self.line = QtGui.QLineEdit(str(model_name))

#         self.ok_button = QtGui.QPushButton("Ok")

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.combo, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.line, 1, 1)
#         layout.addWidget(self.ok_button, 2, 0, 2, 2)

        self.setLayout(layout)

    def new_name(self):
        return self.line.text()

    def old_name(self):
        return self.combo.currentText()


class ProjectManagerWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.view = ProjectManagerView()
        self.model = self.view.model()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        self.menu_available_projects = QtGui.QMenu(u'Available Projects')

        self.actionNewProj = self.view.actionNewProj
        self.actionOpenProj = self.view.actionOpenProj

        group = "Project"
        self._actions = [[group, "Manage Project", self.view.actionNewProj, 0],
                         [group, "Manage Project", self.view.actionOpenProj, 0],
                         [group, "Manage Project", self.view.actionSaveProj, 0],
                         #                  [group, "Manage Project", self.view.actionSaveProjAs, 1],
                         [group, "Manage Project", self.view.actionCloseProj, 0],
                         #                  [group, "Manage Project", self.view.actionEditMeta, 1],
                         #                  ["Project", "Manage Project", self.actionRenameProject, 1],
                         ]
        self._actions += self.view._actions

        # Menu used to display all available projects.
        # This menu is filled dynamically each time this menu is opened
        self.menu_available_projects = QtGui.QMenu(u'Available Projects')
        self.menu_available_projects.aboutToShow.connect(self._update_available_project_menu)
        self.action_available_project = {}  # Dict used to know what project corresponds to triggered action

    def initialize(self):
        if plugin_instance_exists('oalab.applet', 'EditorManager'):
            paradigm_container = plugin_instance('oalab.applet', 'EditorManager')
            self.view.link_paradigm_container(paradigm_container)

        self.view.initialize()
        project = default_project()
        self.set_project(project)

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return [
            ["Project", "Manage", self.view.actionNewProj, 0],
            ["Project", "Manage", self.view.actionOpenProj, 0],
            ["Project", "Manage", self.view.actionSaveProj, 0],
            ["Project", "Manage", self.view.actionCloseProj, 0],
            ["Project", "Manage", self.view.actionSaveProjAs, 1],
            ["Project", "Manage", self.view.actionEditMeta, 1],
        ]

    def toolbars(self):
        actions = [action[2] for action in self.toolbar_actions()]
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

    def project(self):
        return self.view.project()

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
            for project in _projects:
                icon_path = project.icon_path
                icon_name = icon_path if icon_path else ":/images/resources/openalealogo.png"
                action = QtGui.QAction(QtGui.QIcon(icon_name), project.name, self.menu_available_projects)
                action.triggered.connect(self._on_open_project_triggered)
                menu.addAction(action)
                self.action_available_project[action] = project
            self.menu_available_projects.addMenu(menu)
        return self.menu_available_projects

    def _on_open_project_triggered(self):
        project = self.action_available_project[self.sender()]
        self.set_project(project)

    def set_project(self, project):
        self.view.set_project(project)

    ####################################################################
    # Settings
    ####################################################################
    def writeSettings(self):
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


class ProjectManagerView(QtGui.QTreeView, AbstractListener):

    def __init__(self):
        QtGui.QTreeView.__init__(self)
        AbstractListener.__init__(self)

        self._project = None
        self.paradigm_container = None
        self._model = ProjectManagerModel()
        self.setModel(self._model)

        self._model.dataChanged.connect(self._on_model_changed)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.connect(self, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.open)

        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self._actions = []

        self.actionEditMeta = QtGui.QAction(qicon("book.png"), "Edit Project Information", self)
        self.actionEditMeta.triggered.connect(self.edit_metadata)

        self.actionImportFile = QtGui.QAction(qicon("open.png"), "Import file", self)
        self.actionImportFile.triggered.connect(self.import_file)

        self.actionSaveProjAs = QtGui.QAction(qicon("save.png"), "Save As", self)
        self.actionSaveProjAs.triggered.connect(self.save_as)

        self.actionSaveProj = QtGui.QAction(qicon("save.png"), "Save project", self)
        self.actionSaveProj.triggered.connect(self.save)
        self.actionSaveProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))

        self.actionCloseProj = QtGui.QAction(qicon("closeButton.png"), "Close project", self)
        self.actionCloseProj.triggered.connect(self.close)
        self.actionCloseProj.setShortcut(self.tr("Ctrl+Shift+W"))

        self.actionNewProj = QtGui.QAction(qicon("new.png"), "New Project", self)
        self.actionNewProj.triggered.connect(self.new_project)
        self.actionNewProj.setShortcut(self.tr("Ctrl+Shift+N"))

        self.actionOpenProj = QtGui.QAction(qicon("open.png"), "Open Project", self)
        self.actionOpenProj.triggered.connect(self.open_project)
        self.actionOpenProj.setShortcut(self.tr('Ctrl+Shift+O'))

        self.paradigms = {}
        self._new_file_actions = {}
        self.paradigms_actions = []
        for plugin in plugins('oalab.plugin', criteria=dict(implement='IParadigmApplet')):
            applet = debug_plugin('oalab.plugin', func=plugin)
            if applet:
                self.paradigms[plugin.name] = applet
                action = QtGui.QAction(QtGui.QIcon(applet.icon), "New " + applet.default_name, self)
                action.triggered.connect(self.new_file)
                self.paradigms_actions.append(action)
                self._new_file_actions[action] = applet.default_name
                self._actions.append(["Project", "Manage", action, 1],)

    def link_paradigm_container(self, paradigm_container):
        self.paradigm_container = paradigm_container
        self.paradigm_container.paradigms_actions = self.paradigms_actions

    #  API
    def initialize(self):
        pass

    def notify(self, sender, event=None):
        signal, data = event
        print event
        if signal == 'project_changed':
            self.refresh()

    def set_project(self, project):
        if self._project:
            self._project.unregister_listener(self)
        self._project = project
        if self._project:
            project.register_listener(self)

        # TODO: Dirty hack to remove asap. Close project selector if widget has been created
        if hasattr(self, "proj_selector"):
            del self.proj_selector

        self._model.set_project(project)

        if project:
            self.close_all_scripts()
            # self.open_all_scripts_from_project(project)
            self.expandAll()
        else:
            self.close_all_scripts()

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
        if index is None or project is None or data is None:
            return (None, None, None)
        else:
            category, name = data
            return project, category, name

    #  Slots

    def _on_model_changed(self):
        self.expandAll()

    #  Contextual menu

    def add_new_file_actions(self, menu):
        for applet in self.paradigms.values():
            action = QtGui.QAction(qicon(applet.icon), 'New %s' % applet.default_name, self)
            action.triggered.connect(self.new_file)
            self._new_file_actions[action] = applet
            menu.addAction(action)
        menu.addSeparator()

    def create_menu(self):
        menu = QtGui.QMenu(self)
        project, category, obj = self.selected_data()

        if category == 'category' and obj == 'model':
            self.add_new_file_actions(menu)

        elif category == 'category' and obj == 'data':
            import_data = QtGui.QAction(qicon('import.png'), 'Import data', self)
            import_data.triggered.connect(self.open)
            menu.addAction(import_data)

        elif category == 'category' and obj in ('startup', 'doc', 'lib'):
            new_startup = QtGui.QAction(qicon('filenew.png'), 'New file', self)
            new_startup.triggered.connect(self._new_file)
            menu.addAction(new_startup)

        if category == 'model':
            self.add_new_file_actions(menu)

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

        if category in ['project']:
            menu.addAction(self.actionEditMeta)
            menu.addAction(self.actionSaveProj)
            menu.addAction(self.actionSaveProjAs)
            menu.addAction(self.actionCloseProj)

        return menu

    def contextMenuEvent(self, event):
        if self.project() is None:
            return
        menu = self.create_menu()
        menu.exec_(event.globalPos())

    #  Action's slots

    def edit_metadata(self):
        project = self.project()
        if project:
            project_creator = CreateProjectWidget(project)
            dialog = ModalDialog(project_creator)
            if dialog.exec_():
                _proj = project_creator.project()
                if _proj.name != project.name or _proj.projectdir != project.projectdir:
                    project.move(_proj.path)
                project.metadata = project_creator.metadata()
                project.save()

    def open_project(self, name=False, path=None):
        """
        If name==false, display a widget to choose project to open.
        Then open project.
        """
        self.proj_selector = ProjectSelectorScroll(projects=projects())
        self.proj_selector.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.proj_selector.show()

    def new_project(self):
        project_creator = CreateProjectWidget()
        dialog = ModalDialog(project_creator)
        if dialog.exec_():
            project = project_creator.project()
            project.set_project(project)
            project.save()
            write_project_settings()

    def open_all_scripts_from_project(self, project):
        if self.paradigm_container is not None:
            for model in project.model.values():
                self.paradigm_container.open_data(model)

    def _new_file(self):
        category = 'model'
        try:
            dtype = self._new_file_actions[self.sender()]
            name = '%s_%s.%s' % (dtype, category, DataClass(MimeType(name=dtype)).extension)
        except KeyError:
            dtype = None
            name = 'new_file.ext'

        category, data = self.add(self.project(), name, code='', dtype=dtype, category=category)
        if data:
            self.open_data(data)

    def new_file(self, dtype=None):
        try:
            applet = self._new_file_actions[self.sender()]
        except KeyError:
            dtype = None
        else:
            dtype = applet.default_name
        project, category, data = self.selected_data()
        code = ''
        project = self.project()

        if category == 'category':
            category = data
        elif category in project.DEFAULT_CATEGORIES:
            pass
        else:
            category = None

        if dtype is None and category in ['startup', 'lib']:
            dtype = 'Python'

        if category in ['startup', 'lib']:
            d = {'startup': 'start.py', 'lib': 'algo.py'}
            name = d[category]
        elif dtype:
            klass = DataClass(MimeType(name=dtype))
            name = '%s_%s.%s' % (klass.default_name, category, klass.extension)
        else:
            name = category
        category, data = self.add(project, name, code, dtype=dtype, category=category)
        if self.paradigm_container and data:
            self.paradigm_container.open_data(data)

    def add(self, project, name, code, dtype=None, category=None):
        project = self.project()
        if dtype is None:
            dtypes = [pl.default_name for pl in plugins('openalea.core', criteria=dict(implement='IModel'))]
        else:
            dtypes = [dtype]

        if category:
            categories = [category]
        else:
            categories = project.DEFAULT_CATEGORIES.keys()
        selector = SelectCategory(filename=name, categories=categories, dtypes=dtypes)
        dialog = ModalDialog(selector)
        if dialog.exec_():
            category = selector.category()
            filename = selector.name()
            dtype = selector.dtype()
            path = project.path / category / filename
            data = project.get_item(category, filename)
            if path.exists() and data is None:
                box = QtGui.QMessageBox.information(self, 'Data yet exists',
                                                    'Data with name %s already exists in this project, just add it' % filename)
                code = None
                data = project.add(category=category, filename=filename, content=code, dtype=dtype)
            elif path.exists() and data:
                pass
            if data:
                self.open_in_editor(category, name)
                return category, data
        return None, None

    def open_in_editor(self, category, name):
        project = self.project()
        if self.paradigm_container is None:
            paradigm_container = plugin_instance('oalab.applet', 'EditorManager')
            self.link_paradigm_container(paradigm_container)
        self.paradigm_container.show()
        self.paradigm_container.open_data(project.get(category, name))

    def open(self):
        project, category, name = self.selected_data()
        if project:
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
                self.open_in_editor(category, name)

    def _rename(self, project, category, name):
        if category in project.DEFAULT_CATEGORIES:
            filelist = getattr(project, category).keys()
            renamer = RenameModel(filelist, name)
            dialog = ModalDialog(renamer)
            if dialog.exec_():
                old_name = renamer.old_name()
                new_name = renamer.new_name()
                project.rename_item(category, old_name, new_name)
        elif category == 'project':
            self.edit_metadata()

    def rename(self):
        project, category, name = self.selected_data()
        if project:
            self._rename(project, category, name)

    def remove(self):
        project, category, name = self.selected_data()
        if project:
            project.remove(category, filename=name)

    def delete(self):
        project, category, name = self.selected_data()
        if project:
            if category in project.DEFAULT_CATEGORIES:
                data = project.get(category, name)

                confirm = QtGui.QLabel('Remove %s ?' % data.path)
                dialog = ModalDialog(confirm)
                if dialog.exec_():
                    project.remove(category, data)
                    data.path.remove()
                    if self.paradigm_container:
                        self.paradigm_container.close_data(data)

    def save(self):
        project = self.project()
        if project:
            project.save()

    def save_as(self):
        project = self.project()
        if project:
            p = path(self.showNewProjectDialog(default_name=None, text="Select name to save project")).abspath()
            projectdir, name = p.splitpath()
            if name:
                project.save_as(projectdir, name)

    def close(self):
        self.set_project(None)

    def close_all_scripts(self):
        if self.paradigm_container is None:
            return
        self.paradigm_container.closeAll()

    def import_file(self):
        print 'import_file'

    def showNewProjectDialog(self, default_name=None, text=None, parent=None):
        my_path = path(settings.get_project_dir())
        if default_name:
            my_path = my_path / default_name
        if not text:
            text = 'Select name to create project'
        fname = QtGui.QFileDialog.getSaveFileName(parent, text, my_path)
        return fname

    def showOpenProjectDialog(self, parent=None):
        my_path = path(settings.get_project_dir())
        fname = QtGui.QFileDialog.getExistingDirectory(parent, 'Select Project Directory', my_path)
        return fname


class ProjectManagerModel(QtGui.QStandardItemModel):

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self._data = {}
        self._root_item = None
        self._project = None

        add_drag_format(self, 'openalealab/data')
        add_drag_format(self, 'openalealab/model')

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

    def project(self):
        return self._project

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
            lib=QtGui.QIcon(":/images/resources/codefile-red.png"),
        )

        name = project.name
        parentItem = self.invisibleRootItem()
        item = QtGui.QStandardItem(name)
        self._root_item = name

        item.setIcon(self.project_icon(project))
        parentItem.appendRow(item)

        for category in project.DEFAULT_CATEGORIES:
            item2 = QtGui.QStandardItem(category)
            item.appendRow(item2)

            if category in icons:
                item2.setIcon(icons[category])

            if not hasattr(project, category):
                continue

            data_dict = getattr(project, category)

            names = data_dict.keys()
            for name in sorted(names):
                data = data_dict[name]
                item3 = QtGui.QStandardItem(name)
                if hasattr(data, 'icon'):
                    data_icon_path = data.icon
                else:
                    data_icon_path = ''
                item3.setIcon(QtGui.QIcon(data_icon_path))
                item3.setData((category, data))
                item2.appendRow(item3)

    def projectdata(self, index):
        if index is None:
            return None
        if self._project is None:
            return

        if index.parent().data() in self._project.DEFAULT_CATEGORIES:
            category = index.parent().data()
            name = index.data()
            return category, name
        elif index.data() in self._project.DEFAULT_CATEGORIES:
            return ('category', index.data())
        elif index.data() == self._root_item:
            return ('project', index.data())
        else:
            return None

    def mimeData(self, indices):
        for index in indices:
            pass

        category, name = self.projectdata(index)
        if category in ('model', 'data'):
            data = self._project.get_item(category, name)
            return encode_to_qmimedata(data, 'openalealab/%s' % category)
        else:
            return QtGui.QStandardItemModel.mimeData(self, indices)
