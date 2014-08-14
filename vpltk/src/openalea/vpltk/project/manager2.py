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
from openalea.core.path import path as Path
from openalea.core import settings
from openalea.vpltk.project.project2 import Project
from openalea.core.singleton import Singleton
from openalea.core.observer import Observed, AbstractListener
from ConfigParser import NoSectionError, NoOptionError
from openalea.vpltk.plugin import iter_plugins

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

        self._cproject = None
        self._cwd = Path('.').abspath()

        self.projects = []
        self.repositories = self.search_path()

        self.shell = None
        # TODO Search in preference file if user has path to append in self.repositories
        self._cproject = self.default()

    @staticmethod
    def search_path():
        """
        Return a list of all path containing projects
        """
        repositories = set()

        # 1. Add default user project dir
        repositories.add(Path(settings.get_project_dir()))

        # 2. Add project repositories defined by packages
        for plugin in iter_plugins('oalab.project_repository'):
            for repository in plugin():
                repositories.add(repository)

        # 3. Read repositories defined by users and saved in config
        config = settings.Settings()
        lst = list(repositories)
        try:
            s = config.get("ProjectManager", "Path")
            lst = eval(s)
        except NoSectionError, e:
            config.add_section("ProjectManager")
            config.add_option("ProjectManager", "Path", str(lst))
        except NoOptionError, e:
            config.add_option("ProjectManager", "Path", str(lst))

        for repo in lst:
            repositories.add(repo)

        # Remove all paths to directories that don't exist
        final_list = set()
        for p in repositories:
            p = Path(p).abspath()
            if not p.isdir():
                continue
            final_list.add(p)


        return list(final_list)


    def write_settings(self):
        """ Add a new path to the settings. """
        lst = list(set(self.repositories))
        lst = map(str, lst)
        config = settings.Settings()
        config.set("ProjectManager", "Path", str(lst))
        config.write()

    def discover(self, config_name='oaproject.cfg'):
        """
        Discover projects from your disk and put them in self.projects.

        Projects are not loaded, only metadata are.

        :use:
            >>> project_manager.discover()
            >>> list_of_projects = project_manager.projects

        To discover new projects, you can add path into *self.repositories*

        .. code-block:: python

            project_manager.repositories.append('path/to/search/projects')
            project_manager.discover()
        """
        projects = {}
        for _path in self.repositories:
            _path = Path(_path)
            if not _path.exists():
                continue
            for p in _path.walkfiles(config_name):
                project = Project(p.parent)
                projects[project.path] = project
        self.projects = projects.values()


    def search(self, **kwargs):
        """
        Search a specific project that match filters.

        :use:
            >>> project = project_manager.search(name="myproject")

        :param name: name of project to search (str)
        :return: project if it is found, else None

        If various projects are find, return the first (arbitrary)

        :TODO: implement with real filter (ex: name = "*mtg*", authors = "*OpenAlea*", ...)
        """
        regexpr = kwargs['regexpr'] if 'regexpr' in kwargs else False
        name = kwargs['name'] if 'name' in kwargs else None
        alias = kwargs['alias'] if 'alias' in kwargs else None
        if regexpr:
            raise NotImplementedError

        projects = []
        for proj in self.projects:
            if name:
                if proj.path.name != name:
                    continue
            if alias:
                if proj.alias != alias:
                    continue
            projects.append(proj)
        return projects

    def default(self):
        """
        :return: a default empty project
        """
        _path = Path(settings.get_project_dir())
        proj = Project(_path / "temp")
        proj.centralized = False

        if not proj.model:
            txt = '''"""
OpenAlea Lab editor
This temporary script is saved in temporary project in
%s

You can rename/move this project thanks to the button "Save As" in menu.
"""''' % str(proj.path)
            proj.add("model", filename="model.py", content=txt)

        if not proj.path.exists():
            proj.save()

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
            projectdir = Path(settings.get_project_dir())
        else:
            projectdir = Path(projectdir).abspath()
            if projectdir not in self.repositories:
                self.repositories.append(projectdir)
                self.write_settings()

        project = Project(projectdir / name)
        self.cproject = project

        return self.cproject

    def load(self, name, projectdir=None, **kwargs):
        """
        Load existing project

        :use:
            >>> project1 = project_manager.load('project1')
            >>> project2 = project_manager.load('project2', '/path/to/project')

        :param name: name of project to load. Must be a string.
        :param projectdir: path of project to load. Must be a path (see module path.py). By default, try to guess with name only. If there are various projects with the same name, return the first.
        :return: Project
        """
        if 'proj_path' in kwargs:
            projectdir = kwargs['proj_path']
        elif 'path' in kwargs:
            projectdir = kwargs['path']

        if not projectdir:
            projects = self.search(name=name)
            if projects:
                project = projects[0]
        else:
            full_path = Path(projectdir) / name
            if full_path.exists():
                project = Project(full_path)
            else:
                print 'Project %s in repository %s does not exist' % (name, projectdir)

        if project:
            self.cproject = project
            return self.cproject

    def close(self, name=None, proj_path=None):
        """
        Close current project.

        :TODO: not yet implemented
        """
        # TODO: cleaner!
        self.cproject = None

    def __getitem__(self, name):
        projects = self.search(name)
        if projects:
            return projects[0]
        else:
            return None

    def clear(self):
        """
        Clear the list of projects.
        """
        self.projects = []
        self.cproject = self.default()

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'project_changed':
            self.notify_listeners(('project_updated', self))

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
            if project.path.isdir():
                os.chdir(project.path)
            self._cproject = project
            if not project.started:
                project.start(shell=self.shell)
            project.register_listener(self)
        self.notify_listeners(('project_changed', self))

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
    pm = ProjectManager()

    # Create or load project
    name = "project_test"
    proj = pm.load(name)

    app.exec_()


if (__name__ == "__main__"):
    main()
