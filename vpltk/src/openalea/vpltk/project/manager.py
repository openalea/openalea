"""
---------------------
How to use module
---------------------        
You can create load or save a project(P) thanks to the project manager (PM).

When you create or load a P, the PM return a P like here:

.. code-block::
    PM = ProjectManager()
    P1 = PM.create('project1')
    P2 = PM.load('project2')
    P3 = PM['project2']

You can then manipulate P and these attributes (name, controls, scene, global_workflow)
.. code-block::
    P1.controls['newcontrol'] = my_new_control
    print P1

When you have finished, you can save the project:
.. code-block::
    PM.save(P1)    

"""
import os
from openalea.core.path import path as path_
from openalea.core import settings
from openalea.vpltk.project.project import Project
from configobj import ConfigObj

def read_manifest(filename):
        """
        Read a manifest file (oaproject.cfg by default).
        
        :param filename: full filename of manifest file to read
        :return: a ConfigObj (dict) with what is in manifest file
        """
        config = ConfigObj(filename)
        return config

class ProjectManager(object):
    """
    Object which manage projects: creation, loading, saving   
    Should it be a Singleton?
    """
    def __init__(self):
        super(ProjectManager, self).__init__()
        self.projects = []
        #self.projects_list = []
        self.cproject = self.empty()
        self.find_links = [path_(settings.get_project_dir())]
        
        try:
            from openalea import oalab
            from openalea.deploy.shared_data import shared_data
            oalab_dir = shared_data(oalab)
            self.find_links.append(path_(oalab_dir))
        except ImportError:
            pass
            
    def discover(self):
        for project_path in self.find_links:
            for root, dirs, files in os.walk(project_path):
                if "oaproject.cfg" in files: 
                    if root not in self.projects:
                        project_path = root
                        mani = ConfigObj(path_(project_path)/"oaproject.cfg")
                        project_path, name = path_(project_path).splitpath()
                        if mani.has_key("name"):
                            name = mani["name"]
                        project = Project(name, project_path)
                        project._load_manifest()
                        self.projects.append(project)
                            
    def search(self):
        pass

    def get_current(self):
        return self.cproject
        
    def empty(self):
        """
        :return: a fake empty project
        """
        project_path = path_(settings.get_project_dir())
        proj = Project(project_name="temp", project_path=project_path)
        proj.centralized = False
        return proj
    
    def load_empty(self):
        """
        :return: the default loaded project
        """
        project_path = path_(settings.get_project_dir())       
        proj = self.load(project_name="temp", project_path=project_path)
        
        if proj == -1: #If can't load default project, create it
            proj = self.empty()
            
        return proj
    
    def create(self, project_name, project_path=None):
        """
        Create new project
        :return: Project
        """
        if project_path is None:    
            project_path = path_(settings.get_project_dir())
        
        proj = Project(project_name, project_path)
        proj.create()
        
        #self.projects[proj.name] = proj
        self.cproject = proj
        return proj
    
    def load(self, project_name, project_path=None):
        """
        Load existing project
        
        :param project_name: name of project to load. Must be a string.
        :param project_path: path of project to load. Must be a path (see module path.py).
        Default=None means that the path is the openaelea.core.settings.get_project_dir()
        :return: Project
        """
        if not project_path:    
            project_path = path_(settings.get_project_dir())
        
        full_path = path_(project_path)/project_name
        
        if full_path.exists():
            proj = Project(project_name, project_path)
            proj.start()
            
            #self.projects[proj.name] = proj
            self.cproject = proj
            return proj
        else:
            #raise IOError('Project %s in repository %s does not exist' %(project_name,project_path))
            #print 'Project %s in repository %s does not exist' %(project_name,project_path)
            return -1

    def close(self, project_name):
        pass
        # TODO
        
        #if project_name in self.projects.keys():
        #    del self.projects[project_name]
            
    def __getitem__(self, project_name):
        try:
            proj = self.load(project_name)
            return proj
        except:
            return self.empty()
            
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
    project_name = "project_test"
    proj = PM.load(project_name)
    proj.shell = shellwdgt

    app.exec_()

    
if( __name__ == "__main__"):
    main()                  
