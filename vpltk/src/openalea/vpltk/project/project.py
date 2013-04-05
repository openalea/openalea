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

You can then manipulate P and these attributes (name, controls, world, global_workflow)
.. code-block::
    P1.controls['newcontrol'] = my_new_control
    print P1

When you have finished, you can save the project:
.. code-block::
    PM.save(P1)    
    
    
---------------------
Project Architecture
---------------------
You are here the architecture of the project named "project_name",
stored in your computer.

/project_name
    /scripts          (Files sources, Script Python, LPy...)
    /data               (Data Files)
        /controls       (Controls, like color map or curve)
        /world          (World, scene 3D)
        /cache          (Intermediary saved objects)
    /startup          (Preprocessing scripts)
        *.py            (Preprocessing scripts)
        *import*.py     (Libs and packages to import in preprocessing)

"""
import os
import path as module_path
from path import path as _path
from openalea.core import settings

class Project(object):
    def __init__(self,project_name, project_path):
        self.name = str(project_name)
        self.path = _path(project_path)
        self.ns = dict()
        
        # self.set_ipython()
        self.shell = None
    
    #----------------------------------------
    # Public API
    #----------------------------------------    
    def create(self):
        self._create_default_folders()
        self.start()
        
    def start(self):
        # Load in object
        self.startup = self._load_startup()

        # Load in shell
        self._startup_import()
        self._startup_run()
        
        self.scripts = self._load_scripts()
        self.controls = self._load_controls()
        self.cache = self._load_cache()
        self.world = self._load_world()
        
    def save(self):
        self._save_startup()
        self._save_scripts()
        self._save_controls()
        self._save_cache()
        self._save_world()
        
    def set_ipython(self, shell=None):
        if not self.use_ipython():
            try:
                # Try to get automatically current IPython shell
                shell = get_ipython()
            except:
                shell = None
        self.shell = shell
        
    def use_ipython(self):
        """
        :return: True if project is instaciated with a shell IPython.
        Else, return False.
        """
        if self.shell == None:
            return False
        else:
            return True

    #----------------------------------------
    # Protected 
    #---------------------------------------- 
    def _load_startup(self):
        startup = dict()
        temp_path = self.path/self.name/"startup"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            startup[file] = open(file).read()
            
        os.chdir(cwd)    
            
        return startup
        
    def _load_scripts(self):
        scripts = dict()
        temp_path = self.path/self.name/"scripts"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            if not file.endswith('~'):
                scripts[file] = open(file).read()
            
        os.chdir(cwd)    
            
        return scripts
        
    def _load_controls(self):
        """
        Struct of controls:
        dict 'key = FileName' 'value = dict(Names : Values)'
        ie. {FileName : {Name:Value, Name2:Value2, ...} }
        """
        controls = dict()
        temp_path = self.path/self.name/"data"/"controls"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
 
        # Load Controls 
        temp_files = os.listdir(temp_path)
        for file_name in temp_files:
            if not file_name.endswith('~'):
                text = open(file_name).read()
                temp_dict = eval(text, self.ns)
                controls[file_name] = temp_dict

        # Add controls in namespace
        for filename in controls:
            for name in controls[filename]:
                self.ns[name] = eval(controls[filename][name])
        
        os.chdir(cwd)    
            
        return controls
        
    def _load_cache(self):
        cache = dict()
        temp_path = self.path/self.name/"data"/"cache"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        # Load Cache
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            if not file.endswith('~'):
                cache[file] = open(file).read()

        # Add cache in namespace
        for cache_dict in cache:
            for key in eval(cache[cache_dict], self.ns):
                self.ns[key] = eval(cache[cache_dict], self.ns)[key]
        
        os.chdir(cwd)    
            
        return cache
        
    def _load_world(self):
        world = dict()
        temp_path = self.path/self.name/"data"/"world"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            if not file.endswith('~'):
                world[file] = open(file).read() in temp_path
            
        # TODO ? : merge world from (dict of dict) in (dict)
        
        os.chdir(cwd)    
            
        return world    
        
    def _save_startup(self):
        temp_path = self.path/self.name/"startup"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for unit_startup in self.startup:
            file = open(unit_startup, "w")
            code = str(self.startup[unit_startup])
            code_enc = code.encode("utf8","ignore") 
            file.write(code_enc)
            file.close()
       
        os.chdir(cwd) 
        
    def _save_scripts(self):
        temp_path = self.path/self.name/"scripts"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for script in self.scripts:
            file = open(script, "w")
            code = str(self.scripts[script])
            code_enc = code.encode("utf8","ignore") 
            file.write(code_enc)
            file.close()
       
        os.chdir(cwd) 
        
    def _save_controls(self):
        """
        Struct of controls:
        dict 'key = FileName' 'value = dict(Names : Values)'
        ie. {FileName : {Name:Value, Name2:Value2, ...} }

        On the disk, controls are group by FileName in dict {Name:Value}
        """
        temp_path = self.path/self.name/"data"/"controls"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        temp_dict = dict()
        
        for FileName in self.controls:
            for Name in self.controls[FileName]:
                temp_dict[Name] = self.controls[FileName][Name]

            file = open(FileName, "w")
            code = str(temp_dict)
            code_enc = code.encode("utf8","ignore") 
            file.write(code_enc)
            file.close()
       
        os.chdir(cwd) 
        
    def _save_cache(self):
        temp_path = self.path/self.name/"data"/"cache"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for unit_cache in self.cache:
            file = open(unit_cache, "w")
            code = str(self.cache[unit_cache])
            code_enc = code.encode("utf8","ignore") 
            file.write(code_enc)
            file.close()
       
        os.chdir(cwd)    

    def _save_world(self):
        temp_path = self.path/self.name/"data"/"world"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for unit_world in self.world:
            file = open(unit_world, "w")
            code = str(self.world[unit_world])
            code_enc = code.encode("utf8","ignore") 
            file.write(code_enc)            
            file.close()
       
        os.chdir(cwd) 
        
    def _startup_import(self): 
        use_ip = self.use_ipython()
    
        for s in self.startup:
            if s.find('import') != -1:
                exec(self.startup[s],self.ns)
                if use_ip:
                    self.shell.runcode(self.startup[s])

    def _startup_run(self):
        use_ip = self.use_ipython()
    
        for s in self.startup:
            if s.find('import') == -1:
                exec(self.startup[s],self.ns)
                if use_ip:
                    self.shell.runcode(self.startup[s])
        
    def _create_default_folders(self):
        """
        Create the default folders for the current project
        """
        error = False
        
        try:
            os.mkdir(self.path/self.name)
        except OSError:
            print("Directory %s alreay exits in %s" %(self.name,self.path))
            error = True
        
        folders = [self.path/self.name/'data', 
                   self.path/self.name/'scripts',
                   self.path/self.name/'startup',
                   self.path/self.name/'data'/'controls', 
                   self.path/self.name/'data'/'cache', 
                   self.path/self.name/'data'/'world' ]
        try:
            map(os.mkdir, folders)
        except OSError:
            print("Directories %s alreay exits in %s\%s" %(folders,self.name,self.path))
            error = True
        
        if error:
            print("---Warning!---")
            print("Please delete old directories before creating new!")
            raise OSError("Please delete old directories before creating new!")
        

class ProjectManager(object):
    """
    Object which manage projects: creation, loading, saving   
    Should it be a Singleton?
    """
    def create(self, project_name, project_path=None):
        """
        Create new project
        :return: Project
        """
        if project_path is None:    
            project_path = _path(settings.get_project_dir())
        
        proj = Project(project_name, project_path)
        proj.create()
        return proj
    
    def load(self, project_name, project_path=None):
        """
        Load existing project
        
        :param project_name: name of project to load. Must be a string.
        :param project_path: path of project to load. Must be a path (see module path.py).
        Default=None means that the path is the openaelea.core.settings.get_project_dir()
        :return: Project
        """
        if project_path is None:    
            project_path = _path(settings.get_project_dir())
        
        full_path = _path(project_path)/project_name
        
        if full_path.exists():
            proj = Project(project_name, project_path)
            proj.start()
            return proj
        else:
            raise IOError('Project %s in repository %s does not exist' %(project_name,project_path))
            return -1

    def __getitem__(self, project_name):
        return self.load(project_name)
      
    
    
def main():
    print("Warning: Need OpenAlea.VPLTK to work") 
    from openalea.vpltk.qt import qt as qt_
    from openalea.vpltk.shell.ipythoninterpreter import Interpreter
    from openalea.vpltk.shell.ipythonshell import ShellWidget
    import sys
    
    # Create Window with IPython shell
    app = qt_.QtGui.QApplication(sys.argv)
    interpreter = Interpreter()
    shellwdgt = ShellWidget(interpreter)
    mainWindow = qt_.QtGui.QMainWindow()
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
