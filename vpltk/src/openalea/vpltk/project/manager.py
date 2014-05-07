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


class ProjectManager(object):
    """
    Object which manage projects: creation, loading, saving, searching, ...

    It is a singleton.
    """
    __metaclass__ = Singleton

    def __init__(self):
        super(ProjectManager, self).__init__()
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
            >>> print project_manager.projects

        To discover new projects, you can add path into *self.find_links*

        .. code-block:: python

            project_manager.find_links.append('path/to/search/projects')
            project_manager.discover()
        """
        self.clear()
        for path in self.find_links:
            for root, dirs, files in os.walk(path):
                if "oaproject.cfg" in files:
                    path = root
                    path, name = path_(path).splitpath()
                    if not ((path in [proj.path for proj in self.projects]) and (
                        name in [proj.name for proj in self.projects])):
                        project = Project(name, path)
                        project.load()
                        self.projects.append(project)

    def search(self, *args, **kwargs):
        """
        Search a specific project that match filters.

        :use:
            >>> project_manager.search(name="*mtg*", author="*Godin*")

        :TODO: not implemented yet
        """
        return self.projects

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
        self.cproject.create()

        return self.get_current()

    def load(self, name, path=None):
        """
        Load existing project

        :use:
            >>> project1 = project_manager.load('project1')
            >>> project2 = project_manager.load('project2', '/path/to/project')

        :param name: name of project to load. Must be a string.
        :param path: path of project to load. Must be a path (see module path.py). By default, the path is the openaelea.core.settings.get_project_dir() ($HOME/.openalea/projects/).
        :return: Project
        """
        if not path:
            path = path_(settings.get_project_dir())

        full_path = path_(path) / name

        if full_path.exists():
            self.cproject = Project(name, path)
            self.cproject.load()

            return self.get_current()
        else:
            #raise IOError('Project %s in repository %s does not exist' %(name,path))
            #print 'Project %s in repository %s does not exist' %(name,path)
            return -1

    def close(self, name=None, path=None):
        """
        :TODO: not yet implemented
        """
        pass
        # del self.cproject
        # self.cproject = self.default()

    """
    def __getitem__(self, name):
        try:
            self.cproject = self.load(name)
            return self.get_current()
        except:
            return self.default()"""

    def clear(self):
        """
        Clear the list of projects.
        """
        self.projects = []
        self.cproject = self.default()


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
    proj.shell = shellwdgt

    app.exec_()


if ( __name__ == "__main__"):
    main()                  
