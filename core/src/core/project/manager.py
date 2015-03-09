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
import sys

from openalea.core.path import path as Path
from openalea.core import settings
from openalea.core.project.project import Project
from openalea.core.singleton import Singleton
from openalea.core.observer import Observed, AbstractListener
from ConfigParser import NoSectionError, NoOptionError
from openalea.core.plugin import iter_plugins
from openalea.core.control.manager import ControlManager
from openalea.core.service.ipython import interpreter


class ProjectManager(Observed, AbstractListener):

    """
    Object which permit to access to projects: creation, loading, searching, ...

    It is a singleton.

    >>> from openalea.core.project import ProjectManager
    >>> project_manager = ProjectManager()

    """
    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)

        self._cproject = None
        self._cwd = Path('.').abspath()
        self.old_syspath = sys.path

        self.cm = ControlManager()

        self.projects = []
        self.repositories = self.search_path()
        self.previous_project = "temp"

        self.shell = interpreter()
        # TODO Search in preference file if user has path to append in self.repositories
        self.cproject = self.default()


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
            lst = eval(s, {"path": Path})
        except NoSectionError:
            config.add_section("ProjectManager")
            config.add_option("ProjectManager", "Path", str([str(path) for path in lst]))
        except NoOptionError:
            config.add_option("ProjectManager", "Path", str([str(path) for path in lst]))

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

    @property
    def defaultdir(self):
        return Path(settings.get_project_dir())

    def load_settings(self):
        config = settings.Settings()
        try:
            self.previous_project = config.get("ProjectManager", "Last Project")
        except (settings.NoSectionError, settings.NoOptionError):
            pass

    def write_settings(self):
        """ Add a new path to the settings. """
        lst = list(set(self.repositories))
        lst = map(str, lst)
        config = settings.Settings()
        config.set("ProjectManager", "Path", str(lst))

        try:
            config.set("ProjectManager", "Last Project", str(self.previous_project))
        except settings.NoSectionError, e:
            config.add_section("ProjectManager")
            config.add_option("ProjectManager", "Last Project", str(self.previous_project))
        except settings.NoOptionError, e:
            config.add_option("ProjectManager", "Last Project", str(self.previous_project))

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
        regexpr = kwargs.pop('regexpr', False)
        name = kwargs.pop('name', None)
        alias = kwargs.pop('alias', None)
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
        _path = self.defaultdir
        proj = Project(_path / "temp")
        if not proj.path.exists():
            txt = '''"""
OpenAlea Lab editor
This temporary script is saved in temporary project in
%s

You can rename/move this project thanks to the button "Save As" in menu.
"""''' % str(proj.path)
            proj.add("model", filename="model.py", content=txt)
            proj.save()

        return proj

    def create(self, name, projectdir=None, **kwargs):
        """
        Create new project and return it.

        :use:
            >>> project1 = project_manager.create('project1')
            >>> project2 = project_manager.create('project2', '/path/to/project')

        :param name: name of project to create (str)
        :param path: path where project will be saved.
                     By default, path is the user path of all projects ($HOME/.openalea/projects/).
        :return: Project
        """
        if projectdir is None:
            projectdir = self.defaultdir
        else:
            projectdir = Path(projectdir).abspath()
            if projectdir not in self.repositories:
                self.repositories.append(projectdir)
                self.write_settings()

        project = Project(projectdir / name, **kwargs)

        return project

    def load_default(self):
        self.discover()
        self.load_settings()
        projects = [proj for proj in self.projects if proj.name == self.previous_project]
        if len(projects):
            project = projects[0]
        else:
            project = self.default()
        self.cproject = project

    def load(self, name, projectdir=None, **kwargs):
        """
        Load existing project

        :use:
            >>> project1 = project_manager.load('project1')
            >>> project2 = project_manager.load('project2', '/path/to/project')

        :param name: name of project to load. Must be a string.
        :param projectdir: path of project to load. Must be a path (see module path.py).
                           By default, try to guess with name only.
                           If there are various projects with the same name, return the first.
        :return: Project
        """
        project = None
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
                self.notify_listeners(('start_project', self))
                project.start(shell=self.shell)
                self.notify_listeners(('project_started', self))
            return
        if project is None:
            os.chdir(self._cwd)
            if self._cproject:
                self.notify_listeners(('close_project', self))
                self._cproject.unregister_listener(self)
                self._cproject.stop()
                del self._cproject
            self._cproject = None
            self.notify_listeners(('project_closed', self))
        else:
            if project.path.isdir():
                os.chdir(project.path)
            self._cproject = project
            if not project.started:
                project.start(shell=self.shell)
            project.register_listener(self)

        self.update_namespace(self.shell)
        self.notify_listeners(('project_changed', self))

    def update_namespace(self, interpreter):
        """
        Definition: Update namespace
        """
        if self._cproject:
            if self._cproject.path.exists():
                os.chdir(self._cproject.path)
                sys.path.insert(0, str(self._cproject.path / 'lib'))
            else:
                os.chdir(self.tmpdir)
                sys.path.insert(0, str(self.tmpdir / 'lib'))
            interpreter.user_ns.update(self._cproject.ns)
            interpreter.user_ns['project'] = self._cproject
            interpreter.user_ns['data'] = self._cproject.path / 'data'
        else:
            # close
            sys.path = self.old_syspath


def main():
    import sys
    from openalea.vpltk.qt import QtGui
    from openalea.core.service.ipython import interpreter
    from openalea.oalab.shell import ShellWidget

    # Create Window with IPython shell
    app = QtGui.QApplication(sys.argv)
    interp = interpreter()
    shellwdgt = ShellWidget(interp)
    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(shellwdgt)
    mainWindow.show()

    # Create Project Manager
    pm = ProjectManager()

    # Create or load project
    name = "project_test"
    pm.load(name)

    app.exec_()


if (__name__ == "__main__"):
    main()
