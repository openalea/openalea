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
        self.scripts = self._load_scripts()
        self.controls = self._load_controls()
        self.cache = self._load_cache()
        self.world = self._load_world()
        
        # Load in shell
        self._startup_import()
        self._startup_run()
        
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
            scripts[file] = open(file).read()
            
        os.chdir(cwd)    
            
        return scripts
        
    def _load_controls(self):
        controls = dict()
        temp_path = self.path/self.name/"data"/"controls"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
 
        # Load Controls 
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            controls[file] = open(file).read()
        
        # Add controls in namespace
        for control in controls:
            for key in eval(controls[control]):
                self.ns[key] = eval(controls[control])[key]
        
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
            cache[file] = open(file).read()

        # Add cache in namespace
        for cache_dict in cache:
            for key in eval(cache[cache_dict]):
                self.ns[key] = eval(cache[cache_dict])[key]
        
        os.chdir(cwd)    
            
        return cache
        
    def _load_world(self):
        world = dict()
        temp_path = self.path/self.name/"data"/"world"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        temp_files = os.listdir(temp_path)
        for file in temp_files:
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
            file.write(repr(self.startup[unit_startup]))
            file.close()
       
        os.chdir(cwd) 
        
    def _save_scripts(self):
        temp_path = self.path/self.name/"scripts"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for script in self.scripts:
            file = open(script, "w")
            file.write(repr(self.scripts[script]))
            file.close()
       
        os.chdir(cwd) 
        
    def _save_controls(self):
        temp_path = self.path/self.name/"data"/"controls"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for control in self.controls:
            file = open(control, "w")
            file.write(repr(self.controls[control]))
            file.close()
       
        os.chdir(cwd) 
        
    def _save_cache(self):
        temp_path = self.path/self.name/"data"/"cache"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for unit_cache in self.cache:
            file = open(unit_cache, "w")
            file.write(repr(self.cache[unit_cache]))
            file.close()
       
        os.chdir(cwd)    

    def _save_world(self):
        temp_path = self.path/self.name/"data"/"world"
        
        cwd = os.getcwd()
        os.chdir(temp_path)
        
        for unit_world in self.world:
            file = open(unit_world, "w")
            file.write(repr(self.world[unit_world]))
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
        
'''
class Old_Project(object):
    def __init__(self, project_name, project_path=None, controls=None, world=None, global_workflow=None, namespace={}):
        """
        New project
        :param project_name: name of the project. Must be a string.
        :param project_path: of the project. Must be a path.
        :param controls: of VirtualPlantsLab. Must be a dict. Default=None.
        :param world: of VirtualPlantsLab. Must be a dict. Default=None. 
        :param global_workflow: of VirtualPlantsLab. Must be a dict. Default=None. 
        :param namespace: of current project. Must be a dict. Default={}. 
        """
        self.name = project_name
        if project_path is None:    self.path = _path(settings.get_project_dir())/self.name
        else:                       self.path = _path(project_path)/self.name
        self.ns = namespace
        
        self.setup(controls, world, global_workflow)
        

    def setup(self, controls, world, global_workflow):    
        """
        :param controls: of VirtualPlantsLab. Must be a dict. Default=None. 
        :param world: of VirtualPlantsLab. Must be a dict. Default=None.
        :param global_workflow: of VirtualPlantsLab. Must be a dict. Default=None.
        """
        if controls is None:
            self.controls = dict()
        else:    
            self.controls = controls
        if world is None:
            self.world = dict()
        else:    
            self.world = world
        if global_workflow is None:
            self.global_workflow = dict()
        else:    
            self.global_workflow = global_workflow
    
    def namespace(self):
        return dict(self.ns)
            
    def __str__(self):
        return """name: %s
        class: %s
        path: %s
        controls: %s
        world: %s
        workflow: %s""" % (self.name, self.__class__, self.path, self.controls, self.world, self.global_workflow)        
            
'''
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
      
'''
      
class Old_ProjectManager(object):
    """
    Object which manage projects: creation, loading, saving   
    Should it be a Singleton?
    """    
    
    def __init__(self, shell=None):
        """
        :param shell: where projects will be executed, import will be done...
        """
        if shell == None:
            try:
                shell = get_ipython()
            except:
                shell = None
                
        self.shell = shell
    
    #----------------------------------------
    # Public API
    #----------------------------------------
    def create(self, project_name, path):
        """
        Create new project
        :return: Project
        """
        self._create_folders(project_name, path)
        proj = Project(project_name, path)
        return proj
        
    def load(self, project_name, path):
        """
        Load existing project
        :return: Project
        """
        proj = Project(project_name, path)
        # Pre-processing
        self._import_libs(project_name, path)
        self._import_pkgs(project_name, path)
        self._push_cache(project_name, path)
        self._run_startup(project_name, path)
        
        # Set attributes into the object project from the disk
        controls = self._get_controls(project_name, path)
        world = self._get_world(project_name, path)
        global_workflow = self._get_global_workflow(project_name, path)
        proj.setup(controls, world, global_workflow)

        return proj
        
    def save(self, project, cache=None):
        """
        Save project on the disk at project.path
        :param project: to save
        :param cache: only if you want to save it. Must be a dict.
        """
        self._set_controls(project)
        self._set_world(project)
        self._set_global_workflow(project)
        if cache is None:
            cache = dict()
        self._set_cache(project, cache)

    #----------------------------------------
    # 
    #----------------------------------------    
    def __getitem__(self, project_name):
        prj_path = path(setting.get_userpkg_dir())/'projects'
        # return self.load(project_name, "C:\Users\su200116\Documents/temp")
        return self.load(project_name, prj_path)

    # def __setitem__(self, project_name, project):
        # self.save(project_name, project)    

    #----------------------------------------
    # Protected 
    #----------------------------------------
    def _set_controls(self, project):
        """
        Save controls
        :param project: in which you want to save controls
        """
        #filename = "%s/%s/data/controls.py" %(project.path,project.name)
        filename = project.path/project.name/"data"/"controls.py"

        try:
            file = open(filename, "w")
        except:
            print("Can't open file '%s'" %filename)
            return None
        try:    
            file.write(repr(project.controls))
            file.close()
        except:
            print("Can't write controls in '%s'" %(filename))
            return None

    def _set_world(self, project):
        """
        Save world
        :param project: in which you want to save world
        """
        filename = project.path/project.name/"data"/"world.py"
        
        try:
            file = filename.open("w")
        except:
            print("Can't open file '%s'" %filename)
            return None
        try:    
            file.write(str(project.world))
            file.close()
        except:
            print("Can't write world in '%s'" %(filename))
            return None 
        
    def _set_global_workflow(self, project):
        """
        Save global_workflow
        :param project: in which you want to save global_workflow
        """
        # filename = "%s/%s/src/%s.py" %(project.path,project.name,project.name)
        # try:
            # file = open(filename, "w")
        # except:
            # print("Can't open file '%s'" %filename)
            # return None
        # try:    
            # file.write(str(project.global_workflow))
            # file.close()
        # except:
            # print("Can't write global_workflow in '%s'" %(filename))
            # return None 
        
    def _set_cache(self, project, cache):
        """
        Save cache
        :param project: in which you want to save cache
        :param cache: to save
        """
        if cache == None:
            cache = dict()
        filename = "%s/%s/data/cache.py" %(project.path,project.name)
        try:
            file = open(filename, "w")
        except:
            print("Can't open file '%s'" %filename)
            return None
        try:    
            file.write(str(cache))
            file.close()
        except:
            print("Can't write cache in '%s'" %(filename))
            return None    
        
    def _push_cache(self, project_name, path):
        """
        Get cache and push it in shell.
        """
        # Get Cache
        filename = "%s/%s/data/cache.py" %(path,project_name)
        try:
            file = open(filename, "Ur")
        except:
            print("Can't open file '%s'" %filename)
            return
        
        cache = eval(file.read())   

        # Push Cache
        self.ns.update(cache)
        
        try:
            self.shell.push(cache)
        except:
            print("Can't push cache '%s' in shell '%s'" %(cache, self.shell))
            return
        
    def _run_startup(self, project_name, path):
        """
        Get startup and run it in shell.
        """
        # Get startup
        full_path = module_path.path"%s/%s/startup" %(path,project_name)
        startupfiles = os.listdir(full_path)
        # Run startup
        for startupfile in startupfiles:
            execfile(startupfile,self.ns)
            try:
                self.shell.magic('run -i %s/%s' %(full_path,startupfile)) 
            except:
                try:
                    self.shell.execute('%%run -i %s/%s' %(full_path,startupfile)) 
                except:    
                    print("Can't run magic command run or import file '%s'" %startupfile)
                    return
        
    def _import_libs(self, project_name, path):
        """
        Get libs and import them in shell.
        """
        full_path = "%s/%s/libs" %(path,project_name)
        libfiles = os.listdir(full_path)
        libs_to_push = {}
        for libfile in libfiles:
            mod = libfile.split('.')[0]
            if mod != "packages":
                libs_to_push[mod] = __import__(mod)
        try:
            self.shell.push(libs_to_push)
        except:
            print("Can't imports libs '%s' in shell '%s'" %(libs_to_push, self.shell))
            return

    def _import_pkgs(self, project_name, path):
        """
        Get packages and import them in shell.
        """
        filename = "%s/%s/libs/packages.py" %(path,project_name)
        try:
            file = open(filename, "Ur")
        except:
            print("Can't open file '%s'" %filename)
            return

        
        
        try:    
            for line in file:
                l = line.split(" ")
                if len(l) == 3:
                    self.shell.runcode('from %s import %s as %s' %(l[0],l[1],l[2])) 
                elif len(l) == 2:
                    self.shell.runcode('import %s as %s' %(l[0],l[1])) 
                elif len(l) == 1:
                    self.shell.runcode('import %s'%(l[0])) 
        except:
            print("Can't imports packages from '%s' in shell '%s'" %(filename, self.shell))
            return
    
    def _get_controls(self, project_name, path):
        """
        Get controls.
        :return: a dict of controls
        """
        filename = "%s/%s/data/controls.py" %(path,project_name)
        try:
            file = open(filename, "Ur")
        except:
            print("Can't open file '%s'" %filename)
            return None
        try:    
            controls = eval(file.read())
            return controls 
        except:
            print("Can't eval controls from '%s'" %(filename))
            return None
            
    def _get_world(self, project_name, path):
        """
        Get the world!
        :return: a dict which is the world
        """
        filename = "%s/%s/data/world.py" %(path,project_name)
        try:
            file = open(filename, "Ur")
        except:
            print("Can't open file '%s'" %filename)
            return None
        try:    
            world = eval(file.read())
            return world 
        except:
            print("Can't eval world from '%s'" %(filename))
            return None
        
    def _get_global_workflow(self, project_name, path):
        """
        Get the global workflow
        :return: a dict which is the global workflow
        """
        # filename = "%s/%s/src/%s.py" %(path,project_name,project_name)
        # try:
            # file = open(filename, "Ur")
        # except:
            # print("Can't open file '%s'" %filename)
            # return None
        # try:    
            # global_workflow = eval(file.read())
            # return global_workflow 
        # except:
            # print("Can't eval global_workflow from '%s'" %(filename))
            # return None 

    def _create_folders(self, project_name, path):
        """
        Create the default folders and default empty files
        :param project_name: name of the project to create
        :param path: of the project to create
        """
        error = False
        
        os.chdir(path)
        try:
            os.mkdir(project_name)
        except OSError:
            print("Directory %s alreay exits in %s" %(project_name,path))
            error = True
        
        os.chdir(project_name)
        folders = ['data', 'src', 'startup', 'libs']
        try:
            map(os.mkdir, folders)
        except OSError:
            print("Directories %s alreay exits in %s\%s" %(folders,path,project_name))
            error = True
        
        if error:
            print("---Warning!---")
            print("Please delete old directories before creating new!")
        else:
            # Create files
            self._create_empty_files(project_name, path)
        
    def _create_empty_files(self, project_name, path):
        """
        Create the default empty files
        :param project_name: name of the project to create
        :param path: of the project to create
        """
        os.chdir(path)
        
        os.chdir(project_name)
        os.chdir("data")
        f1 = open("controls.py", "w")
        f1.write("{}")
        f1.close()
        f2 = open("world.py", "w")
        f2.write("{}")
        f2.close()
        f3 = open("cache.py", "w")
        f3.write("{}")
        f3.close()
        
        os.chdir("..\src")
        f4 = open("%s.py" %project_name, "w")
        f4.write("{}")
        f4.close()
        
        os.chdir("..\libs")
        open("packages.py", "w")
'''       
    
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
    PM = ProjectManager(shell=shellwdgt)
    
    # Create or load project
    project_name = "project_test"
    path = "C:\OpenAlea\openalea\oalab\src\openalea\oalab"
    # PM.create(project_name, path)
    PM.load(project_name, path)

    app.exec_()

    
if( __name__ == "__main__"):
    main()                  