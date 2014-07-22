# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
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

import os
import platform
from openalea.core.path import path
from openalea.core import settings
from openalea.vpltk.project.project import Project
from openalea.core.singleton import Singleton
from openalea.core.observer import Observed, AbstractListener
from ConfigParser import NoSectionError, NoOptionError

class ProjectManager(Observed, AbstractListener):
    """
    Object which permit to access to projects: creation, loading, searching, ...

    It is a singleton.

    >>> from openalea.vpltk.project import ProjectManager
    >>> project_manager = ProjectManager()

    """
    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)
        self.projects = []
        self._cproject = None
        self._cwd = path('.').abspath()
        self.find_links = self.search_path()

        self.shell = None
        # TODO Search in preference file if user has path to append in self.find_links
        self._cproject = self.default()

    @staticmethod
    def search_path():
        """

        """

        find_links = [path(settings.get_project_dir())]

        # TODO Move it into OALab ?
        if not "windows" in platform.system().lower():
            try:
                from openalea import oalab
                from openalea.deploy.shared_data import shared_data

                oalab_dir = shared_data(oalab)
                find_links.append(path(oalab_dir))
            except ImportError:
                pass

        find_links = set(find_links)
        config = settings.Settings()
        l = list(find_links)
        # wralea path
        try:
            s = config.get("ProjectManager", "Path")
            l = eval(s)
        except NoSectionError, e:
            config.add_section("ProjectManager")
            config.add_option("ProjectManager", "Path", str(l))
        except NoOptionError, e:
            config.add_option("ProjectManager", "Path", str(l))

        find_links = set()
        l = map(path, set(l))
        for p in l:
            p = p.abspath()
            if not p.isdir():
                continue
            find_links.add(str(p))

        return list(find_links)


    def write_settings(self):
        """ Add a new path to the settings. """
        l = list(set(self.find_links))
        l = map(str, l)
        config = settings.Settings()
        config.set("ProjectManager", "Path", str(l))
        config.write()

    def discover(self):
        """
        Discover projects from your disk and put them in self.projects.

        Projects are not loaded, only metadata are.

        :use:
            >>> project_manager.discover()
            >>> list_of_projects = project_manager.projects

        To discover new projects, you can add path into *self.find_links*

        .. code-block:: python

            project_manager.find_links.append('path/to/search/projects')
            project_manager.discover()
        """
        self.projects = []
        for _path in self.find_links:
            for root, dirs, files in os.walk(_path):
                if "oaproject.cfg" in files:
                    _path, name = path(root).abspath().splitpath()
                    if not ((_path in [proj.projectdir for proj in self.projects]) and (
                        name in [proj.name for proj in self.projects])):
                        project = Project(name, _path)
                        project.load_manifest()
                        self.projects.append(project)

    def search(self, name=None):
        """
        Search a specific project that match filters.

        :use:
            >>> project = project_manager.search(name="myproject")

        :param name: name of project to search (str)
        :return: project if it is found, else None

        If various projects are find, return the first (arbitrary)

        :TODO: implement with real filter (ex: name = "*mtg*", authors = "*OpenAlea*", ...)
        """
        if name:
            proj = [proj for proj in self.projects if proj.name == name]
        else:
            proj = self.projects
            if not isinstance(proj, list):
                proj = [proj]
        if len(proj):
            return proj[0]
        return None

    def get_current(self):
        """
        :return: current active project

        :use:
            >>> project = project_manager.get_current()
        """
        return self.cproject

    def default(self):
        """
        :return: a default empty project
        """
        _path = path(settings.get_project_dir())
        proj = Project(name="temp", projectdir=_path)
        proj.centralized = False

        if not proj.list_models():
            txt = '''"""
OpenAlea Lab editor
This temporary script is saved in temporary project in
%s

You can rename/move this project thanks to the button "Save As" in menu.
"""''' % str(proj.path)
            proj.new_model(name="temp.py", code=txt)

        return proj

    def load_default(self):
        """
        Load default project if it exists, else create it.

        :return: the default loaded project
        """
        _path = path(settings.get_project_dir())
        try:
            if not _path.exists():
                _path.makedirs()
        except:
            pass

        proj = self.load("temp", _path)

        if proj is None: # If can't load default project, create it
            proj = self.default()

        return proj

    def create(self, name, projectdir=None):
        """
        Create new project and return it.

        :use:
            >>> project1 = project_manager.create('project1')
            >>> project2 = project_manager.create('project2', '/path/to/project')

        :param name: name of project to create (str)
        :param path: path where project will be saved. By default, path is the user path of all projects ($HOME/.openalea/projects/).
        :return: Project
        """
        if projectdir is None:
            projectdir = settings.get_project_dir()
        else:
            projectdir = path(projectdir).abspath()
            if projectdir not in self.find_links:
                self.find_links.append(projectdir)
                self.write_settings()

        project = Project(name, projectdir)
        self.cproject = project

        return self.cproject

    def load(self, name, proj_path=None):
        """
        Load existing project

        :use:
            >>> project1 = project_manager.load('project1')
            >>> project2 = project_manager.load('project2', '/path/to/project')

        :param name: name of project to load. Must be a string.
        :param proj_path: path of project to load. Must be a path (see module path.py). By default, try to guess with name only. If there are various projects with the same name, return the first.
        :return: Project
        """
        if not proj_path:
            for project in self.projects:
                if project.name == name:
                    self.cproject = project
                    project.start(shell=self.shell)
                    return self.get_current()
        else:
            # full_path = path(proj_path).abspath() / name / ".." / ".." # TODO : why ?
            full_path = path(proj_path) / name
            # print full_path
            if full_path.exists():
                self.cproject = Project(name, proj_path)
                self.cproject.start(shell=self.shell)
                return self.get_current()

        # raise IOError('Project %s in repository %s does not exist' %(name,proj_path))
        print 'Project %s in repository %s does not exist' %(name,full_path)
        return None

    def close(self, name=None, proj_path=None):
        """
        Close current project.

        :TODO: not yet implemented
        """
        # TODO: cleaner!
        self.cproject = None

    def __getitem__(self, name):
        self.cproject = self.search(name)
        return self.get_current()

    def clear(self):
        """
        Clear the list of projects.
        """
        self.projects = []
        self.cproject = self.default()

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'project_change':
            self.notify_listeners(('project_updated', self))
            self.notify_listeners(('current_project_change', self))

    @property
    def cproject(self):
        return self._cproject

    @cproject.setter
    def cproject(self, project):
        if project is self._cproject:
            if project and not project.started:
                project.start(shell=self.shell)
            return
        if project is None:
            os.chdir(self._cwd)
            if self._cproject:
                self._cproject.unregister_listener(self)
                del self._cproject
            self._cproject = None
        else:
            if (project.path).isdir():
                os.chdir(project.path)
            self._cproject = project
            if not project.started:
                project.start(shell=self.shell)
            project.register_listener(self)
        self.notify_listeners(('project_changed', self))
        self.notify_listeners(('current_project_change', self))

    def set_shell(self, shell):
        """ Set the ipython shell to load a project.

        """
        self.shell = shell


def main():
    from openalea.vpltk.qt import QtGui
    from openalea.vpltk.shell.ipythoninterpreter import Interpreter
    from openalea.vpltk.shell.ipythonshell import ShellWidget
    import sys

    # Create Window with IPython shell
    app = QtGui.QApplication(sys.argv)
    interpreter = Interpreter()
    shellwdgt = ShellWidget(interpreter)
    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()

    # Create Project Manager
    PM = ProjectManager()

    # Create or load project
    name = "project_test"
    proj = PM.load(name)

    app.exec_()


if (__name__ == "__main__"):
    main()
