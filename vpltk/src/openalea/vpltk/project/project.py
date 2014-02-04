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
    /controls       (Controls, like color map or curve)
    /scene          (scene, scene 3D)
    /cache          (Intermediary saved objects)
    /startup          (Preprocessing scripts)
        *.py            (Preprocessing scripts)
        *import*.py     (Libs and packages to import in preprocessing)

"""
import os
import warnings
from openalea.core.path import path as _path
from openalea.core import settings
import cPickle
from configobj import ConfigObj

def check_unicity(name, all_names):
    """
    Check if an object with the name 'name' is already register
    in 'all_names'.
    
    If it is the case, the name is changed ("_1" is append).
    This is realize until the name becomes unique.
    
    :param name: name to check unicity (str)
    :param all_names: list of other present objects (list)
    
    TODO : remove this method if we want unicity of name, 
    like in a classical dict
    """
    #REVIEW: remove try catch

    while name in all_names:
        namesplited = name.split(".")
        if len(namesplited) == 2:
            begin_name = namesplited[0]
            extension = "." + namesplited[1]
        else:
            begin_name = name
            extension = ""
  
        try:
            end = begin_name.split("_")[-1]
            l = len(end)
            end = int(end)
            end += 1
            name = begin_name[0:-l] + str(end) + extension
        except:    
            name = begin_name + "_1" + extension
    return name

class Project(object):
    def __init__(self,project_name, project_path):
        self.name = str(project_name)
        self.path = _path(project_path)
        self.ns = dict()
        self.controls = dict()
        
        self.shell = None
        self.set_ipython()
        
        self.scripts = dict()
        self.controls = dict()
        self.cache = dict()
        self.scene = dict()
        self.startup = dict()
    
    def is_project(self):
        return True
        
    def is_script(self):
        return False
    #----------------------------------------
    # Public API
    #----------------------------------------    
    def create(self):
        self._create_default_folders()
        self.start()
        
    def start(self):
        # Load in object
        self._load("startup")
        # Load in shell
        self._startup_import()
        self._startup_run()
        
        self.load()
        
    def save(self):
        self._save("scripts")
        self._save("controls")
        self._save("startup")
        self._save("cache")
        self._save("scene")
        self._save_manifest()
        
    def _save_scripts(self):
        self._save("scripts")
        
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
        all_names = list()
        for n in self.scripts:
            all_names.append(n)
        name = check_unicity(name, all_names)
        
        self.scripts[str(name)] = str(script)
        
    #----------------------------------------
    # Rename
    #---------------------------------------- 
    def rename(self, categorie, old_name, new_name):
        """
        Rename a script, a scene or a control in the project. Can rename the project too.
        
        :param categorie: Can be "script", "control", "scene" or "project" (str)
        :param old_name: current name of thing to rename (str)
        :param new_name: futur name of thing to rename (str)
        """
        if (categorie == "script") or (categorie == "scripts") or (categorie == "Models"):
            # Remove in project
            self.scripts[str(new_name)] = self.scripts[str(old_name)]
            del self.scripts[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"scripts"
            cwd = os.getcwd()
            os.chdir(temp_path)
            try:
                os.remove(str(old_name))
            except:
                pass
            os.chdir(cwd) 
        
        if (categorie == "control") or (categorie == "Controls"):
            # Remove in project
            self.controls[str(new_name)] = self.controls[str(old_name)]
            del self.controls[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"controls"
            cwd = os.getcwd()
            os.chdir(temp_path)
            try:
                os.remove(str(old_name))
            except:
                pass
            os.chdir(cwd) 
            
        if (categorie == "scene") or (categorie == "Scene"):
             # Remove in project
            self.scene[str(new_name)] = self.scene[str(old_name)]
            del self.scene[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"scene"
            cwd = os.getcwd()
            try:
                os.remove(str(old_name))
            except:
                pass
            os.chdir(cwd) 
            
        if (categorie == "project"):
            self.name = new_name
            self.save()
            try:
                (self.path/old_name).removedirs()
            except:
                pass
            
            
    def load(self):
        self.scripts = self._load("scripts")
        self.controls = self._load("controls")
        self.cache = self._load("cache")
        self.scene = self._load("scene")
        self.startup = self._load("startup")
        
    #----------------------------------------
    # Protected 
    #---------------------------------------- 
    def _load(self, object_type):
        object_type = str(object_type)
        if object_type == "scene":
            return self._load_scene()
        
        return_object = dict()
        manifest = self._load_manifest()
        
        if manifest.has_key(object_type):
            temp_path = self.path/self.name/object_type
            if not temp_path.exists():
                return return_object
            files = manifest[object_type]
            for filename in files:
                filename = temp_path/filename
                return_object[filename.basename()] = open(filename, 'rU').read()
                
        # hack to add cache in namespace
        if object_type == "cache":
            for cache_name in return_object:
                self.ns[cache_name] = eval(return_object[cache_name], self.ns)
        # hack for controls
        # controls were Pickle.dumped so we need to cPickle.loads
        if object_type == "controls":
            for obj in return_object:
                return_object[obj] = cPickle.loads(return_object[obj])
            
        return return_object

    def _load_scene(self):
        return_object = dict()
        object_type = "scene"
        try:
            from openalea.plantgl.all import Scene
            sc = Scene()
            manifest = self._load_manifest()
        
            if manifest.has_key(object_type):
                temp_path = self.path/self.name/object_type
                if not temp_path.exists():
                    return return_object
                files = manifest[object_type]
            
                for filename in files:
                    fileName, fileExtension = os.path.splitext(str(filename))
                    sc.clear()
                    sc.read(fileName, "BGEOM")
                    return_object[fileName.basename()] = sc.deepcopy()
                    
        except ImportError:
            warnings.warn("You must install PlantGL if you want to load scene in project.")
        except Exception, e:
            print e
            warnings.warn("Impossible to load the scene")
        return return_object    
        
    def _save(self, object_type):
        object_type = str(object_type)
        object_ = eval("self.%s"%object_type)
        temp_path = self.path/self.name/object_type
        
        # Hack to save plantgl object
        if object_type == "scene":
            for sub_object in object_:
                name = str("%s/%s" %(temp_path,sub_object))
                object_[sub_object].save(name, "BGEOM")
        else:
            for sub_object in object_:
                file = open(temp_path/sub_object, "w")
                # Hack to save controls with cPickle
                if object_type == "controls":
                    cPickle.dump(object_[sub_object],file,0)
                else:
                    code = str(object_[sub_object])
                    code_enc = code.encode("utf8","ignore") 
                    file.write(code_enc)
                file.close()
     
    def _save_manifest(self):
        """
        Save in a manifest file what is present inside a project
        """
        config = ConfigObj()
        config.filename = self.path/self.name/"oaproject.cfg"

        config['scripts'] = self.scripts.keys()
        config['controls'] = self.controls.keys()
        config['scene'] = self.scene.keys()
        config['cache'] = self.cache.keys()
        config['startup'] = self.startup.keys()

        config.write()
        
    def _load_manifest(self):
        """
        Load a project from a manifest file
        """
        config = ConfigObj(self.path/self.name/"oaproject.cfg")
        return config

        
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
            warnings.warn("Directory %s alreay exits in %s" %(self.name,self.path))
            error = True
        
        folders = [self.path/self.name/'scripts',
                   self.path/self.name/'startup',
                   self.path/self.name/'controls', 
                   self.path/self.name/'cache', 
                   self.path/self.name/'scene' ]
        try:
            map(os.mkdir, folders)
        except OSError:
            warnings.warn("Directories %s alreay exits in %s\%s" %(folders,self.name,self.path))
            error = True
        
        if error:
            warnings.warn("---Warning!---\nPlease delete old directories before creating new!")
            raise OSError("Please delete old directories before creating new!")
        
    def __repr__(self):
        return "Project named " + str(self.name) + " in path " + str(self.path) + " . Scripts: " + str(self.scripts.keys()) + " . Controls: " + str(self.controls.keys()) + " . Scene: " + str(self.scene.keys())

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
            print 'Project %s in repository %s does not exist' %(project_name,project_path)
            return -1

    def close(self, project_name):
        if project_name in self.projects.keys():
            del self.projects[project_name]
            self.cproject = self.empty()
            
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
