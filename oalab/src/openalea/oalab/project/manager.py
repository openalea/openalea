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
from openalea.vpltk.project.manager import ProjectManager
from openalea.oalab.project.creator import CreateProjectWidget


class ProjectManagerWidget(QtGui.QWidget):
    """
    Object which permit to manage projects.

    :Warning: this QWidget is not used like a widget but like the interface between GUI (buttons "newProj", "newScript",...)
    and objects (project, control, ...)

    :TODO: Refactor it
    """

    def __init__(self, session, controller, parent=None):
        super(ProjectManagerWidget, self).__init__(parent)

        self._actions = []
        self.paradigms_actions = []
        self.session = session
        self.controller = controller
        self.setAccessibleName("Project Manager")

        self.projectManager = ProjectManager()

        for proj in self.projectManager.projects:
            self.session._project = proj

        self.actionEditFile = QtGui.QAction(QtGui.QIcon(":/images/resources/edit.png"), "Edit file", self)
        self.actionImportFile = QtGui.QAction(QtGui.QIcon(":/images/resources/import.png"), "Import", self)

        self.actionNewProj = QtGui.QAction(QtGui.QIcon(":/images/resources/new.png"), "New", self)
        self.actionNewProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenProj = QtGui.QAction(QtGui.QIcon(":/images/resources/open.png"), "Open", self)
        self.actionOpenProj.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveProj = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"), "Save", self)
        self.actionSaveProjAs = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"), "Save As", self)
        # self.actionSaveProj.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseProj = QtGui.QAction(QtGui.QIcon(":/images/resources/closeButton.png"), "Close All", self)

        self.connect(self.actionNewProj, QtCore.SIGNAL('triggered(bool)'), self.new)
        self.connect(self.actionOpenProj, QtCore.SIGNAL('triggered(bool)'), self.open)
        self.connect(self.actionSaveProjAs, QtCore.SIGNAL('triggered(bool)'), self.saveAs)
        self.connect(self.actionSaveProj, QtCore.SIGNAL('triggered(bool)'), self.saveCurrent)
        self.connect(self.actionCloseProj, QtCore.SIGNAL('triggered(bool)'), self.closeCurrent)

        self.connect(self.actionImportFile, QtCore.SIGNAL('triggered(bool)'), self.importFile)
        self.connect(self.actionEditFile, QtCore.SIGNAL('triggered(bool)'), self.editFile)

        self._actions = [["Project", "Manage Project", self.actionNewProj, 1],
                         ["Project", "Manage Project", self.actionOpenProj, 0],
                         ["Project", "Manage Project", self.actionSaveProj, 0],
                         ["Project", "Manage Project", self.actionSaveProjAs, 1],
                         ["Project", "Manage Project", self.actionCloseProj, 1],
                         # ["Model", "New Model", self.actionEditFile, 0],
                         ["Model", "New Model", self.actionImportFile, 0]]

        self.extensions = ""
        self.connectParadigmContainer()

        self.defaultProj()

    def connectParadigmContainer(self):
        # Connect actions from applet_container.paradigms to menu (newPython, newLpy,...)
        for applet in self.controller.applet_container.paradigms.values():
            action = QtGui.QAction(QtGui.QIcon(applet.icon), applet.default_name, self)
            action.triggered.connect(self.newModel)
            self._actions.append(["Model", "New Model", action, 0],)
            self.paradigms_actions.append(action)
            self.extensions = self.extensions + applet.pattern + " "

    def defaultProj(self):
        proj = self.projectManager.load_default()
        self.session._project = proj
        self.session._is_proj = True

        if not self.session.project.src:
            txt = '''# -*- coding: utf-8 -*-
"""
OpenAlea Lab editor

This temporary script is saved in temporary project in
%s

You can rename/move this project thanks to the button "Save As" in menu.
"""''' % str(self.session.project.path / self.session.project.name)
            self.session.project.add(category="src", name=".temp.py", value=txt)

        self._project_changed()
        self._load_control()

    def actions(self):
        return self._actions

    def open(self, name=False, project_path=None):
        """
        If name==false, display a widget to choose project to open.
        Then open project.
        """
        self.closeCurrent()
        # self.controller.applet_container.closeAll()
        """
        if name is False:
            name = showOpenProjectDialog()
        if name:
            proj_path = path(name).abspath()
            proj_name = proj_path.basename()
            proj_path = proj_path.dirname()
            if project_path:
                proj_path = path(project_path)
            logger.debug("Open Project named " + proj_name)
            if self.session.project is not None:
                if self.session.current_is_project():
                    logger.debug("Close Project named " + self.session.project.name)
                    self.projectManager.close(self.session.project.name)
                    logger.debug("Project named " + self.session.project.name + " closed.")

            proj = self.projectManager.load(proj_name, proj_path)

            logger.debug("Project " + str(proj) + " loaded")

            if proj == -1:
                logger.warning("Project was not loaded...")
                return -1
            else:
                return self.openProject(proj)"""


    def openProject(self, project):
        """
        Open a project in application from project

        :param project: project from vpltk
        """
        project.start()
        logger.debug("Project " + str(project) + " opened")

        project.scene = self.session.scene
        self.session._project = project
        self.session._is_proj = True
        self._project_changed()
        self._load_control()

        logger.debug("Project opened: " + str(self.session._project))
        return self.session._project

    def editFile(self, filename=None, extension=None):
        """
        Permit to edit a file which is outside project.
        And add link to file in project.
        """
        if extension is None:
            extension = self.extensions

        if self.session.current_is_project():
            project = self.session.project
            if not filename:
                if extension:
                    filename = showOpenFileDialog(extension)
                else:
                    filename = showOpenFileDialog()
            if filename:
                filename = path(filename).abspath()

                f = open(filename, "r")
                txt = f.read()
                f.close()

                tab_name = str(path(filename).splitpath()[-1])
                ext = str(path(filename).splitext()[-1])
                ext = ext.split(".")[-1]
                logger.debug("Try to import file named " + tab_name + " . With applet_type " + ext)

                try:
                    self.controller.applet_container.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                    project.add("src", filename, txt)
                    self.controller._update_locals()
                    self._tree_view_change()
                    logger.debug("Import file named " + tab_name)
                except:
                    print "File extension " + ext + " not recognised"
                    logger.warning("Can't import file named %s in current project. Unknow extension." % filename)
        else:
            print "You are not working inside project. Please create or load one first."


    def importFile(self, filename=None, extension=None):
        """
        Import a file and add it to the project.

        :param filename: name of file to add in project
        :param extension:
        """
        if extension is None:
            extension = self.extensions

        if self.session.current_is_project():
            project = self.session.project
            if not filename:
                filename = showOpenFileDialog(extension)
            if filename:
                filename = path(filename)
                f = open(filename, "r")
                txt = f.read()
                f.close()
                name = filename.splitpath()[1]
                project.add("src", name, txt)
                self.controller._update_locals()
                self._project_changed()
                logger.debug("Import file named " + name)
        else:
            print "You are not working inside project. Please create or load one first."

    def new(self):
        """
        Create an default empty project with a default name.

        Open a window to define metadata of the project.
        """
        self.project_creator = CreateProjectWidget()
        self.project_creator.show()
        self.connect(self.project_creator, QtCore.SIGNAL('ProjectOpened(PyQt_PyObject)'), self.openProject)

    def newModel(self, applet_type=None, tab_name=None, script=""):
        """
        Create a new model of type 'applet_type

        :param applet_type: type of applet to add. Can be Workflow, LSystem, Python, R
        """
        if self.session.current_is_project():
            if not applet_type:
                button = self.sender()
                applet_type = button.text() # can be Workflow, LSystem, Python, R
                # TODO: this approach is not reliable. If a developer change action name, it breaks the system
                # a better approach should be to define a "newModel" method in IApplet and call it directly
                # for instance in __init__ : action.triggered.connect(applet.newModel)
            Applet = self.controller.applet_container.paradigms[applet_type]
            if not tab_name:
                tab_name = Applet.default_file_name
            self.controller.applet_container.newTab(applet_type=applet_type, tab_name=tab_name, script=script)
            text = self.controller.applet_container.applets[-1].widget().get_text()
            self.session.project.add("src", tab_name, text)
            self.controller._update_locals()
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def removeModel(self, model_name):
        """
        :param model_name: Name of the model to remove in the current project
        """
        if self.session.current_is_project():
            self.session.project.remove("src", model_name)
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def openModel(self, fname=None, extension="*.*"):
        """"
        Open a (script-type) file named "fname".
        If "fname"==None, display a dialog with filter "extension".

        :param fname: filename to open. Default = None
        :param extension: extension of file to open. Default = "*.*"
        """
        if self.session.current_is_project():
            self.importFile(filename=fname, extension=extension)
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def renameCurrent(self, new_name=None):
        """
        Rename current project.
        """
        if self.session.current_is_project():
            name = self.session.project.name
            if not new_name:
                new_name = showNewProjectDialog(default_name=path(name) / "..",
                                                text='Select new name to save project')
            self.session.project.rename(category="project", old_name=name, new_name=new_name)
            self._project_changed()
        else:
            print(
                "You are not working inside project, so you can't use 'rename project'. Please create or load one first.")

    def saveAs(self):
        """
        Save current project but permit to rename and move it..
        """
        if self.session.current_is_project():
            name = showNewProjectDialog(default_name=None, text="Select name to save project")
            if name:
                self.session.project.rename(category="project", old_name=self.session.project.name, new_name=name)
                self._tree_view_change()
                self.saveCurrent()
        else:
            print "You are not working inside project. Please create or load one first."

    def saveCurrent(self):
        """
        Save current project.
        """
        if self.session.current_is_project():
            container = self.controller.applet_container
            for i in range(container.count()):
                container.setCurrentIndex(i)
                name = container.tabText(i)
                container.widget(i).save(name)
            self._update_control()
            self.session.project.save()
            self._project_changed()

        else:
            print "You are not working inside project. Please create or load one first."

    def closeCurrent(self):
        """
        Close current project.
        """
        if self.session.current_is_project():
            logger.debug("Close Project named %s" % self.session.project.name)
            self.projectManager.close(self.session.project.name)
            self.session._project = None
            self.session._is_proj = False
            self._clear_control()
            self.controller.applet_container.closeAll()
            self._project_changed()
        else:
            print "You are not working inside project. Please create or load one first."

    def _project_changed(self):
        """
        Update what is needed when the current project is changed
        """
        logger.debug("Project changed")
        self.controller._update_locals()
        self._scene_change()
        self._control_change() # do nothing
        self._script_change()
        self._tree_view_change()

    def update_from_widgets(self):
        self._update_control()

    def _load_control(self):
        """
        Get control from project and put them into widgets
        """
        if self.controller.applets.has_key('ControlPanel'):
            logger.debug("Load Controls")
            self.controller.applets['ControlPanel'].load()

    def _update_control(self):
        """
        Get control from widget and put them into project
        """
        if self.controller.applets.has_key('ControlPanel'):
            logger.debug("Update Controls")
            self.controller.applets['ControlPanel'].update()

    def _clear_control(self):
        if self.controller.applets.has_key('ControlPanel'):
            logger.debug("Clear Controls")
            self.controller.applets['ControlPanel'].clear()

    def _control_change(self):
        pass

    def _tree_view_change(self):
        logger.debug("Tree View changed")
        self.controller.applets['Project'].update()

    def _script_change(self):
        logger.debug("Script changed")
        if self.session.current_is_project():
            project = self.session.project
            self.controller.applet_container.reset()
            for script in project.src:
                language = str(script).split('.')[-1]
                self.controller.applet_container.openTab(language, script, project.src[script])

    def _scene_change(self):
        logger.debug("Scene changed")
        if self.session.current_is_project():
            self.session.scene.reset()
            project = self.session.project
            for w in project.scene:
                self.session.scene.add(name=w, obj=project.scene[w])


def showNewProjectDialog(default_name=None, text=None, parent=None):
    my_path = path(settings.get_project_dir())
    if default_name:
        my_path = my_path / default_name
    if not text:
        text = 'Select name to create project'
    fname = QtGui.QFileDialog.getSaveFileName(parent, text,
                                              my_path)
    return fname


def showOpenProjectDialog(parent=None):
    my_path = path(settings.get_project_dir())
    fname = QtGui.QFileDialog.getExistingDirectory(parent, 'Select Project Directory',
                                                   my_path)
    return fname


def showOpenFileDialog(extension=None, where=None, parent=None):
    if extension is None:
        extension = self.extensions

    if where is not None:
        my_path = path(str(where)).abspath().splitpath()[0]
    else:
        my_path = path(settings.get_project_dir())
    logger.debug("Search to open file with extension " + extension + " from " + my_path)
    fname = QtGui.QFileDialog.getOpenFileName(parent, 'Select File to open',
                                              my_path, "All (*);;Scripts Files (%s)" % extension)
    return fname
