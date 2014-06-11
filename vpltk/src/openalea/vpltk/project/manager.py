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
from openalea.core.path import path as path_
from openalea.core import settings
from openalea.vpltk.project.project import Project
from openalea.core.singleton import Singleton
from openalea.core.observer import Observed, AbstractListener


class ProjectManager(Observed, AbstractListener):
    """
    Object which permit to access to projects: creation, loading, searching, ...

    It is a singleton.
    """
    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)
        self.projects = []
        self.cproject = self.default()
        self.find_links = [path_(settings.get_project_dir())]

        # TODO Move it into OALab ?
        if not "windows" in platform.system().lower():
            try:
                from openalea import oalab
                from openalea.deploy.shared_data import shared_data

                oalab_dir = shared_data(oalab)
                self.find_links.append(path_(oalab_dir))
            except ImportError:
                pass

        # TODO Search in preference file if user has path to append in self.find_links

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
        for path in self.find_links:
            for root, dirs, files in os.walk(path):
                if "oaproject.cfg" in files:
                    path, name = path_(root).abspath().splitpath()
                    if not ((path in [proj.path for proj in self.projects]) and (
                        name in [proj.name for proj in self.projects])):
                        project = Project(name, path)
                        project.load_manifest()
                        self.projects.append(project)

    def search(self, name=None):
        """
        Search a specific project that match filters.

        :use:
            >>> project_manager.search(name="myproject")

        :param name: name of project to search (str)
        :return: project if it is find, else None

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
        path = path_(settings.get_project_dir())
        proj = Project(name="temp", path=path)
        proj.centralized = False
        return proj

    def load_default(self):
        """
        Load default project if it exists, else create it.

        :return: the default loaded project
        """
        path = path_(settings.get_project_dir())
        proj = self.load(name="temp", path=path)

        if proj == -1:  # If can't load default project, create it
            proj = self.default()

        return proj

    def create(self, name, path=None):
        """
        Create new project and return it.

        :use:
            >>> project1 = project_manager.create('project1')
            >>> project2 = project_manager.create('project2', '/path/to/project')

        :param name: name of project to create (str)
        :param path: path where project will be saved. By default, path is the user path of all projects ($HOME/.openalea/projects/).
        :return: Project
        """
        if path is None:
            path = path_(settings.get_project_dir())

        self.cproject = Project(name, path)

        return self.get_current()

    def load(self, name, path=None):
        """
        Load existing project

        :use:
            >>> project1 = project_manager.load('project1')
            >>> project2 = project_manager.load('project2', '/path/to/project')

        :param name: name of project to load. Must be a string.
        :param path: path of project to load. Must be a path (see module path.py). By default, try to guess with name only. If there are various projects with the same name, return the first.
        :return: Project
        """
        if not path:
            for project in self.projects:
                if project.name == name:
                    self.cproject = project
                    project.load()
                    return self.get_current()
        else:
            full_path = path_(path) / name

            if full_path.exists():
                self.cproject = Project(name, path)
                self.cproject.load()
                return self.get_current()
        #raise IOError('Project %s in repository %s does not exist' %(name,path))
        #print 'Project %s in repository %s does not exist' %(name,path)
        return -1

    def close(self, name=None, path=None):
        """
        Close current project.

        :TODO: not yet implemented
        """
        # TODO: cleaner!
        del self._cproject

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
            self.notify_listeners(('current_project_change', self))

    @property
    def cproject(self):
        return self._cproject

    @cproject.setter
    def cproject(self, project):
        self._cproject = project
        project.register_listener(self)
        self.notify_listeners(('current_project_change', self))


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


if ( __name__ == "__main__"):
    main()                  
