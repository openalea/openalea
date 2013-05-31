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
    
    
---------------------
Project Architecture
---------------------
You are here the architecture of the project named "project_name",
stored in your computer.

/project_name
    /scripts          (Files sources, Script Python, LPy...)
    /data               (Data Files)
        /controls       (Controls, like color map or curve)
        /scene          (scene, scene 3D)
        /cache          (Intermediary saved objects)
    /startup          (Preprocessing scripts)
        *.py            (Preprocessing scripts)
        *import*.py     (Libs and packages to import in preprocessing)

"""
import os
import openalea.core.path as module_path
import warnings
from openalea.core.path import path as _path
from openalea.core import settings
import cPickle

##from openalea.vplab.scene.vplscene import VPLScene

class Project(object):
    def __init__(self,project_name, project_path):
        self.name = str(project_name)
        self.path = _path(project_path)
        self.ns = dict()
        self.controls = dict()
        
        # self.set_ipython()
        self.shell = None
        
        self.scripts = dict()
        self.controls = dict()
        self.cache = dict()
##        self.scene_struct = VPLScene()
##        self.scene = self.scene_struct.getScene()
        self.scene = dict()
    
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
        self.scene = self._load_scene()
        
    def save(self):
        self._save_startup()
        self._save_scripts()
        self._save_controls()
        self._save_cache()
        self._save_scene()
        
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

    def get_scene(self):
        return self.scene
    
    #----------------------------------------
    # Add
    #---------------------------------------- 
    def add_script(self, name, script):
        """
        Add a script in the project
        
        :param name: of the script to add (string)
        :param script: to add (string)
        """
        self.scripts[str(name)] = str(script)
        
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
        for filename in temp_files:
            if not filename.endswith('~'):
                scripts[filename] = open(filename, 'rU').read()
##                scripts[file] = file(filename,'rU').read()
            
        os.chdir(cwd)    
            
        return scripts
        
    def _load_controls(self):
        """
        Struct of controls:
        dict 'dict(Names : Values)'
        """
##        temp_path = self.path/self.name/"data"/"controls"
##        
##        cwd = os.getcwd()
##        os.chdir(temp_path)
## 
##        # Load Controls 
##        temp_files = os.listdir(temp_path)
##        for file_name in temp_files:
##            if not file_name.endswith('~'):
##                text = open(file_name, 'rU').read()
##                self.controls[file_name] = text


        temp_path = self.path/self.name/"data"/"controls"
        filename = '%s/control' %temp_path
        
        try:
            file = open(filename, 'r')
            
    ##        cwd = os.getcwd()
    ##        os.chdir(temp_path)

            try:
                self.controls = cPickle.load(file)
            except EOFError :
                  file.close()

            # Add controls in namespace
            for controlname in self.controls:
                self.ns[controlname] = eval(str(self.controls[controlname]))            

    ##        os.chdir(cwd)    
    
        except IOError:
            self.controls = dict()
        
        return self.controls
        
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
        
    def _load_scene(self):
        try:
            from openalea.plantgl.all import Scene
            import copy
            sc = Scene()
##            scene_struct = VPLScene()
##            scene = scene_struct.getScene()
            scene = dict()
            temp_path = self.path/self.name/"data"/"scene"
            
            cwd = os.getcwd()
            os.chdir(temp_path)
            
            temp_files = os.listdir(temp_path)
            for file in temp_files:
                if not file.endswith('~'):
                    fileName, fileExtension = os.path.splitext(str(file))
                    sc.clear()
                    sc.read(fileName, "BGEOM")
                    scene[fileName] = sc.deepcopy()
##                    scene_struct.add(name=fileName, obj=sc.deepcopy())
            os.chdir(cwd)          
                    
        except ImportError:
            scene = dict()
            warnings.warn("You must install PlantGL if you want to load scene in project.")
        except:
            scene = dict()
            warnings.warn("Impossible to load the scene")
        return scene    
        
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
        dict(Names : Values)

        """
        temp_path = self.path/self.name/"data"/"controls"
        filename = '%s/control' %temp_path
        
        file = open(filename, 'w')
        
##        cwd = os.getcwd()
##        os.chdir(temp_path)
        
##        temp_dict = dict()
        
        cPickle.dump(self.controls,file,0)
        
        file.close()
        
##        for controlName in self.controls:
##            file = open(controlName, "w")
##            code = str(self.controls[controlName])
##            code_enc = code.encode("utf8","ignore") 
##            file.write(code_enc)
##            file.close()
##       
##        os.chdir(cwd) 
        
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

    def _save_scene(self):
        temp_path = self.path/self.name/"data"/"scene"     
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        files = os.listdir(temp_path)
        for file in files:
            os.remove(file)
           
        scene = self.scene
        for sub_scene_name in scene:
            name = str("%s/%s" %(temp_path,sub_scene_name))
            scene[sub_scene_name].save(name, "BGEOM")
        
        os.chdir(cwd) 
        
##        TODO
##        temp_path = self.path/self.name/"data"/"scene" 
##        filename = '%s/scene' %temp_path
##        
##        file = open(filename, 'w')
##        
##        cPickle.dump(self.scene,file,0)
##        
##        file.close()
        
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
                   self.path/self.name/'data'/'scene' ]
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
    def __init__(self):
        super(ProjectManager, self).__init__()
        self.projects = {}
        self.cproject = self.empty()

    def get_current(self):
        return self.cproject
        
    def empty(self):
        """
        :return: a fake empty project
        """
        project_path = _path(settings.get_project_dir())
        proj = Project(project_name="fake", project_path=project_path)
        return proj
    
    def create(self, project_name, project_path=None):
        """
        Create new project
        :return: Project
        """
        if project_path is None:    
            project_path = _path(settings.get_project_dir())
        
        proj = Project(project_name, project_path)
        proj.create()
        
        self.projects[proj.name] = proj
        self.cproject = self.projects[proj.name]
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
            
            self.projects[proj.name] = proj
            self.cproject = self.projects[proj.name]
            return proj
        else:
            raise IOError('Project %s in repository %s does not exist' %(project_name,project_path))
            return -1

    def __getitem__(self, project_name):
        try:
            proj = self.load(project_name)
            return proj
        except:
            return self.empty()
    
    
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
