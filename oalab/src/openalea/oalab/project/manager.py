# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
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
from openalea.core.path import path as path_
from openalea.core import settings
from openalea.core import logger
from openalea.core.customexception import UserException
from openalea.vpltk.project.manager import ProjectManager
from openalea.oalab.project.creator import CreateProjectWidget
from openalea.oalab.project.pretty_preview import ProjectSelectorScroll
from openalea.oalab.gui import resources_rc # do not remove this import else icon are not drawn
from openalea.oalab.gui.utils import qicon
from openalea.oalab.session.session import Session
from openalea.vpltk.plugin import iter_plugins
from openalea.oalab.service.applet import get_applet
from openalea.oalab.service.control import clear_ctrl_manager


from openalea.oalab.gui.utils import ModalDialog, make_info_dialog

class ErrActionOnNoneProject(UserException):
    title = u'Error: cannot do operations outside project'
    message = u'%(value)s cannot be done outside project.'
    desc = """All projects are closed.
    If you really want to do this action, please open an existing project or create a new one."""

class ErrActionOnTemporaryProject(UserException):
    title = u'Error: cannot do operations on temporary project'
    message = u'%(value)s cannot be done on temporary project.'
    desc = """Temporary project is used only at first launch but working on it has no sense.
    If you want to perform action on project, you must create a real project before."""

CATEGORIES = ["model", "startup", "data", "lib"]
class ProjectManagerWidget(QtGui.QWidget):
    """
    Object which permit to manage projects.

    :Warning: this QWidget is not used like a widget but like the interface between GUI (buttons "newProj", "newScript",...)
    and objects (project, control, ...)

    :TODO: Refactor it
    """

    def __init__(self, parent=None):
        super(ProjectManagerWidget, self).__init__(parent)

        # TODO: Check editor_manager is available when used or use signal instead of calling applet explicitly
        self.editor_manager = None

        self._actions = []
        self.session = Session()
        self.setAccessibleName("Project Manager")

        self.projectManager = ProjectManager()

        self.actionNewProj = QtGui.QAction(qicon("new.png"), "New Project", self)
        self.actionNewProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(qicon("open.png"), "Open Project", self)
        self.actionOpenProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(qicon("save.png"), "Save project", self)
        self.actionSaveProjAs = QtGui.QAction(qicon("save.png"), "Save As", self)
        # self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(qicon("closeButton.png"), "Close project", self)
        self.actionEditMeta = QtGui.QAction(qicon("book.png"), "Edit Metadata", self)
        self.actionAddFile = QtGui.QAction(qicon("bool.png"), "Add", self)
        self.actionRenameProject = QtGui.QAction(qicon("editpaste.png"), "Rename Project", self)
        self.actionRenameModel = QtGui.QAction(qicon("editcopy.png"), "Rename Model", self)

        self.actionNewProj.triggered.connect(self.new)
        self.actionOpenProj.triggered.connect(self.open)
        self.actionSaveProjAs.triggered.connect(self.saveAs)
        self.actionSaveProj.triggered.connect(self.saveCurrent)
        self.actionCloseProj.triggered.connect(self.closeCurrent)
        self.actionEditMeta.triggered.connect(self.edit_metadata)
        self.actionAddFile.triggered.connect(self.add_file_to_project)
        self.actionRenameProject.triggered.connect(self.renameCurrent)
        self.actionRenameModel.triggered.connect(self.on_model_renamed)

        self._actions = [["Project", "Manage Project", self.actionNewProj, 0],
                         ["Project", "Manage Project", self.actionOpenProj, 0],
                         ["Project", "Manage Project", self.actionSaveProj, 0],
                         ["Project", "Manage Project", self.actionSaveProjAs, 1],
                         ["Project", "Manage Project", self.actionCloseProj, 1],
                         ["Project", "Manage Project", self.actionEditMeta, 1],
                         ["Project", "Manage Project", self.actionAddFile, 0],
                         ["Project", "Manage Project", self.actionRenameProject, 1],
                         ["Project", "Manage Project", self.actionRenameModel, 1],
        ]

        # Menu used to display all available projects.
        # This menu is filled dynamically each time this menu is opened
        self.menu_available_projects = QtGui.QMenu(u'Available Projects')
        self.menu_available_projects.aboutToShow.connect(self._update_available_project_menu)
        self.action_available_project = {} # Dict used to know what project corresponds to triggered action

    def initialize(self):
        self.editor_manager = get_applet(identifier='EditorManager')
        self.defaultProj()
        self.saveCurrent()

    def defaultProj(self):
        proj = self.projectManager.load_default()
        proj.save()
        self.openProject(proj)

    def actions(self):
        return self._actions

    def open(self, name=False, path=None):
        """
        If name==false, display a widget to choose project to open.
        Then open project.
        """
        self.projectManager.discover()
        projects = self.projectManager.projects
        self.proj_selector = ProjectSelectorScroll(projects=projects, open_project=self.openProject)
        self.proj_selector.show()

    def openProject(self, project):
        """
        Open a project in application

        :param project: opened project from vpltk
        """
        project_name = project.name
        project_path = project.projectdir
        if hasattr(self, "proj_selector"):
            self.proj_selector.hide()
        self.closeCurrent()

        project = self.projectManager.load(project_name, project_path)

        logger.debug("Project " + str(project) + " opened")

        from openalea.oalab.service.ipython import get_interpreter
        interpreter = get_interpreter()
        if interpreter:
            ns = interpreter.locals
        else:
            ns = dict()
        project.start(namespace=ns)
        logger.debug("Project " + str(project) + " started")

        project.world = self.session.world
        self.session.project = project
        self.session._is_proj = True

        self.set_controls_in_control_manager(project)

        self.session.update_namespace()
        self.open_all_scripts_from_project()
        self._scene_change()

        logger.debug("Project opened: " + str(self.session.project.name))
        self.session.project = project
        return self.session.project

    def new(self):
        """
        Create an default empty project with a default name.

        Open a window to define metadata of the project.
        """
        project_creator = CreateProjectWidget()
        dialog = ModalDialog(project_creator)
        if dialog.exec_():
            _project = project_creator.project()
            project = self.projectManager.create(_project.name, _project.projectdir)
            project.metadata = _project.metadata
            self.session.project = project


    def checkProjectOperation(self, action):
        if self.session.project is None:
            error = ErrActionOnTemporaryProject(action)
            make_info_dialog(error)
            return False
        else:
            return True

    def edit_metadata(self):
        if self.checkProjectOperation('change metadata'):
            project = self.session.project
            project_creator = CreateProjectWidget(project)
            project_creator.setMetaDataMode()
            dialog = ModalDialog(project_creator)
            if dialog.exec_():
                self.metadata_edited(project_creator.metadata())

    def metadata_edited(self, metadata):
        self.session.project.metadata = metadata
        return self.session.project

    def add_file_to_project(self):
        """
        Add an opened file to the current project (in source for the moment).

        :todo: propose to the user where to add it (not only in source)
        """
        if self.checkProjectOperation('add file'):
            text = self.editor_manager.tabText(self.editor_manager.currentIndex())
            text = path_(text).splitall()[-1]
            categories = list(CATEGORIES)
            categories.extend(self.session.project.files.keys())
            categories = list(set(categories))

            selector = SelectCategory(filename=text, categories=categories)
            dialog = ModalDialog(self.selector)
            if dialog.exec_():
                category = selector.category()

                text = self.editor_manager.currentWidget().get_text()
                index = self.editor_manager.currentIndex()
                filename = self.selector.line.text()
                ret = self.session.project.add(category=category, name=filename, value=text)
                if ret:
                    self.editor_manager.setTabText(index, filename)
            else:
                print(
            "We can't add model %s to current project. The extension of model seems to be unknown." % str(filename))
            self.session.update_namespace()

    def renameCurrent(self, new_name=None):
        """
        Rename current project.
        """
        if self.checkProjectOperation('rename'):
            name = self.session.project.name
            if not new_name:
                new_name = showNewProjectDialog(default_name=path_(name) / "..",
                                                text='Select new name to save project')
            if new_name:
                self.session.project.rename(category="project", old_name=name, new_name=new_name)

    def new_startup(self):
        """
        Create a startup file and add it to the project.
        """
        proj = self.session.project
        if proj:
            ret = self.session.project.add(category="startup", name="start.py", value="")
            proj._save("startup")
            proj.save_manifest()
            if ret:
                filename = proj.path / "startup" / "start.py"
                self.editor_manager.open_file(filename=filename)

    def on_startup_rename(self, startup_name=""):
        """
        Display a pop up to rename a startup file.

        :param startup_name: name of startup file to remane
        """
        if self.checkProjectOperation('Rename startup file'):
            startups = self.session.project.startup
            list_startups = startups.keys()
            self.renamer = RenameModel(list_startups, startup_name)
            self.renamer.show()
            self.renamer.ok_button.clicked.connect(self._rename_startup_from_renamer)

    def on_model_renamed(self, model_name=""):
        """
        Display a pop up to rename a model.

        :param model_name: name of model to remane
        """
        if self.checkProjectOperation('Rename model'):
            models = self.session.project.list_models()
            self.renamer = RenameModel(list_models, model_name)
            self.renamer.show()
            self.renamer.ok_button.clicked.connect(self._rename_model_from_renamer)

    def _rename_model_from_renamer(self):
        """
        Get informations from the pop up and rename the model
        """
        model_name = self.renamer.combo.currentText()
        new_name = self.renamer.line.text()
        self.renamer.hide()
        self.rename_model(model_name, new_name)

    def _rename_startup_from_renamer(self):
        """
        Get informations from the pop up and rename the startup
        """
        startup_name = self.renamer.combo.currentText()
        new_name = self.renamer.line.text()
        self.renamer.hide()
        self.rename_startup(startup_name, new_name)

    def rename_model(self, old_name, new_name):
        """
        Rename the model.
        """
        if old_name and new_name:
            self.session.project.rename(category="model", old_name=old_name, new_name=new_name)

    def rename_startup(self, old_name, new_name):
        """
        Rename a startup file.
        """
        if old_name and new_name:
            self.session.project.rename(category="startup", old_name=old_name, new_name=new_name)

    def del_model(self, model_name):
        self.session.project.remove(category="model", name=model_name)

    def del_startup(self, startup_name):
        self.session.project.remove(category="startup", name=startup_name)

    def saveAs(self):
        """
        Save current project but permit to rename and move it..
        """
        name = showNewProjectDialog(default_name=None, text="Select name to save project")
        if name:
            self.session.project.rename(category="project", old_name=self.session.project.name, new_name=name)
            self.saveCurrent()

    def saveCurrent(self):
        """
        Save current project.
        """
        container = self.editor_manager
        if container is None: # CPL
            return
        container.save_all()
        proj = self.session.project
        proj.control = self.get_controls_from_control_manager(proj)
        self.session.project.save()

    def closeCurrent(self):
        """
        Close current project.
        """
        if hasattr(self.session, "name"):
            logger.debug("Close Project named %s" % self.session.project.name)
            self.projectManager.close(self.session.project.name)
        else:
            logger.debug("Close empty Project")
        self.session.project_manager.close()
        self.session._is_proj = False
        editor = get_applet(identifier='EditorManager')
        if editor:
            editor.closeAll()
        self.clear_ctrl_mngr()
        self.session.update_namespace()
        self._scene_change()

    def open_all_scripts_from_project(self):
        logger.debug("Open All models")
        if self.session.project:
            project = self.session.project
            models = project.get_models()
            if not isinstance(models, list):
                models = [models]
            for model in models:
                self.editor_manager.open_file(model=model)

    def _scene_change(self):
        logger.debug("Scene changed")
        self.session.world.reset()
        project = self.session.project
        for w in project.world:
            self.session.world.add(name=w, obj=project.world[w])

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
        self.openProject(self.action_available_project[self.sender()])

    def clear_ctrl_mngr(self):
        """
        Clear the *control manager*
        :return:
        """
        # @GBY
        clear_ctrl_manager()

    def set_controls_in_control_manager(self, project):
        """
        Set control in *control manager* from loaded project.

        :param project: project to get controls
        """
        # @GBY
        ctrls = project.control

        self.clear_ctrl_mngr()
        if ctrls:
            for ctrl in ctrls:
                # @GBY
                pass

    def get_controls_from_control_manager(self, project):
        """
        Get control from *control manager* and set them into current project.

        :param project: project to set controls
        """
        # @GBY
        ctrls = None
        # TODO:
        # We want all controls, so we can imagine something like that:
        # ctrls = get_control("*")
        project.control = ctrls

def showNewProjectDialog(default_name=None, text=None, parent=None):
    my_path = path_(settings.get_project_dir())
    if default_name:
        my_path = my_path / default_name
    if not text:
        text = 'Select name to create project'
    fname = QtGui.QFileDialog.getSaveFileName(parent, text,
                                              my_path)
    return fname


def showOpenProjectDialog(parent=None):
    my_path = path_(settings.get_project_dir())
    fname = QtGui.QFileDialog.getExistingDirectory(parent, 'Select Project Directory',
                                                   my_path)
    return fname


class SelectCategory(QtGui.QWidget):
    def __init__(self, filename="", categories=None, dtypes=None, parent=None):
        super(SelectCategory, self).__init__(parent=parent)

        if categories is None:
            categories = CATEGORIES
        if dtypes is None:
            dtypes = [plugin.default_name for plugin in iter_plugins('oalab.paradigm_applet')]
            dtypes.append('Other')
        self.categories = categories

        layout = QtGui.QFormLayout(self)

        self.label = QtGui.QLabel("Select in which category you want to add this file: ")
        self.l_dtypes = QtGui.QLabel("Data type")
        self.label2 = QtGui.QLabel("New filename: ")

        self.combo = QtGui.QComboBox(self)
        self.combo.addItems(categories)
        self.combo.setCurrentIndex(0)

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
        self.combo.setCurrentIndex(0)
        if not model_name:
            model_name = self.models[0]
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

