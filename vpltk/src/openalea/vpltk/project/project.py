"""   
---------------------
Project Architecture
---------------------
You have here the architecture of the project named "project_name",
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
from openalea.core.path import path as path_
from openalea.vpltk.project.configobj import ConfigObj

from openalea.vpltk.project.loader import get_loader, BGEOMLoader, CPickleLoader, GenericLoader
from openalea.vpltk.project.saver import get_saver, BGEOMSaver, CPickleSaver, GenericSaver

class Project(object):
    def __init__(self,project_name, project_path):
        # Metadata
        self.name = str(project_name)
        self.path = path_(project_path)
        self.icon = ""
        self.authors = "OpenAlea Consortium"
        self.description = ""
        self.version = "0.1"
        self.license = "CeCILL-C"
        self.dependencies = ""
        self.citation = ""
        self.long_description = ""

        # Data, scripts, ...
        self.ns = dict()
        self.scripts = dict()
        self.controls = dict()
        self.cache = dict()
        self.scene = dict()
        self.startup = dict()
        
        self.shell = None
        self._set_ipython()
        self._to_save_in_manifest = ['scripts', 'controls', 'scene', 'cache', 'startup']
        self._to_save_in_metadata = ['name', 'icon', 'authors', 'description', 'version', 'license', 'dependencies', 'long_description']

    #----------------------------------------
    # Public API
    #----------------------------------------    
    def create(self):
        self.start()
        
    def start(self):
        # Load in object
        self.load()
        # Load in shell
        self._startup_import()
        self._startup_run()

    def load(self):
        self.load_manifest()
        for category in self._to_save_in_manifest:
            obj = self._load(str(category))
            setattr(self, category, obj)
        
    def save(self):
        for category in self._to_save_in_manifest:
            self._save(str(category))
        self.save_manifest()

    def get(self, category, name):
        """
        :param category: category of object to get
        :param name: name of object to get
        
        :use: >>> get(category="scripts", name="myscript.py")
        """
        if hasattr(self, category):
            cat = getattr(self, category)
            if hasattr(cat, name):
                return cat[name]
            elif hasattr(cat, "has_key"):
                # if category is a dict
                if cat.has_key(name):
                    return cat[name]
        return None
    
    def add(self, category, name, value):
        """
        Add an object in the project
        
        :param category: *type* of object to add ("scripts", "control", "scene", ...)
        :param name: filename of the object to add (path or str)
        :param value: to add (string)
        """
        if not hasattr(self, category):
            setattr(self, category, dict())
        cat = getattr(self, category)
        cat[name] = value
    
    def remove(self, category, name):
        """
        Remove an object in the project
        
        Remove nothing on disk.
        
        :category: category of object to remove ("scripts", "control", "scene", ...) (str)
        :param name: filename of the script to remove (path or str)
        """
        category = str(category)
        filename = path_(name)
        
        if hasattr(self, category):
            cat = getattr(self, category)
            if cat.has_key(filename):
                del cat[filename]
                
    def rename(self, category, old_name, new_name):
        """
        Rename a script, a scene or a control in the project. Can rename the project too.
        
        :param category: Can be "script", "control", "scene" or "project" (str)
        :param old_name: current name of thing to rename (str)
        :param new_name: futur name of thing to rename (str)
        
        :TODO: become generical (cf. remove or add method)
        """
        if (category == "script") or (category == "scripts") or (category == "Models"):  
            if not new_name:
                self.remove(category, old_name)
                return          
            # Remove in project
            self.scripts[str(new_name)] = self.scripts[str(old_name)]
            del self.scripts[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"scripts"
            cwd = os.getcwd()
            if temp_path.exists():
                os.chdir(temp_path)
                try:
                    os.remove(str(old_name))
                except:
                    pass
                os.chdir(cwd) 
        
        if (category == "control") or (category == "Controls"):
            # Remove in project
            self.controls[str(new_name)] = self.controls[str(old_name)]
            del self.controls[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"controls"
            
            if temp_path.exists():
                cwd = os.getcwd()
                os.chdir(temp_path)
                try:
                    os.remove(str(old_name))
                except:
                    pass
                os.chdir(cwd) 
            
        if (category == "scene") or (category == "Scene"):
             # Remove in project
            self.scene[str(new_name)] = self.scene[str(old_name)]
            del self.scene[str(old_name)]
            
            # Remove on disk
            temp_path = self.path/self.name/"scene"
            if temp_path.exists():
                cwd = os.getcwd()
                try:
                    os.remove(str(old_name))
                except:
                    pass
                os.chdir(cwd) 
            
        if (category == "project"):
            self.name = new_name
            self.save()
            try:
                (self.path/old_name).removedirs()
            except:
                pass
                
    #----------------------------------------
    # Manifest
    #---------------------------------------- 
    def save_manifest(self):
        """
        Save in a manifest file what is present inside a project
        """
        config = ConfigObj()
        config.filename = self.path/self.name/"oaproject.cfg"
        
        config['metadata'] = dict()
        config['manifest'] = dict()
        
        for info in self._to_save_in_metadata:
            config['metadata'][info] = getattr(self, info)
            
        for files in self._to_save_in_manifest:
            filenames = getattr(self, files)
            if filenames.keys():
                config['manifest'][files] = filenames.keys()

        config.write()
        
    def load_manifest(self):
        """
        Load a project from a manifest file
        
        :warning: load metadata and list of filenames but does not load files
        """
        config = ConfigObj(self.path/self.name/"oaproject.cfg")
        if config.has_key('metadata'):
            for info in config["metadata"].keys():
                setattr(self, info, config['metadata'][info])

        if config.has_key('manifest'):
            # Load file names in good place (dict.keys()) but don't load entire object:
            # ie. load keys but not values
            for files in config["manifest"].keys():
                filedict = dict()
                for f in config['manifest'][files]:
                    filedict[f] = ""
                setattr(self, files, filedict)
                
    #----------------------------------------
    # Scripts
    #---------------------------------------- 
    def add_script(self, name, script):
        """
        Add a script in the project
        
        :param name: filename of the script to add (path or str)
        :param script: to add (string)
        """
        warnings.warn("project.add_script(name, script) is deprecated. Please use project.add('scripts', name, script) instead.")
        self.add("scripts", name, script)
        
    def remove_script(self, name):
        """
        Add a script in the project
        
        Remove nothing on disk.
        
        :param name: filename of the script to remove (path or str)
        """
        warnings.warn("project.remove_script(name) is deprecated. Please use project.remove('scripts', name) instead.")
        self.remove("scripts", name)     
        
    #----------------------------------------
    # Protected 
    #---------------------------------------- 
    def _load(self, object_type):
        """
        Load files listed in self.object_type.keys()
        """
        object_type = str(object_type)
        return_object = dict()
        
        if hasattr(self, object_type):
            temp_path = self.path/self.name/object_type
            
            if not temp_path.exists():
                return return_object
                
            files = getattr(self, object_type)
            files = files.keys()
            for filename in files:
                filename = path_(filename)
                pathname = self.path/self.name/object_type/filename
                if filename.isabs():
                    # Load files that are outside project
                    pathname = filename
                Loader = get_loader("GenericLoader")
                if object_type == "controls":
                    Loader = get_loader("CPickleLoader")
                if object_type == "scene":
                    Loader = get_loader("BGEOMLoader")
                loader = Loader()
                result = loader.load(pathname)
                return_object[filename] = result
                
        # hack to add cache in namespace
        if object_type == "cache":
            for cache_name in return_object:
                self.ns[cache_name] = eval(str(return_object[cache_name]), self.ns)
            
        return return_object 
        
    def _save(self, object_type):
        object_type = str(object_type)
        object_ = getattr(self, object_type)
        temp_path = self.path/self.name/object_type
        
        # Make default directories
        if not (self.path/self.name).exists():
            os.mkdir(self.path/self.name)
        if not temp_path.exists():
            os.mkdir(temp_path)
        
        for sub_object in object_:
            filename = temp_path/sub_object
            sub_object = path_(sub_object)
            Saver = get_saver()
            if sub_object.isabs():
                # Permit to save object outside project
                filename = sub_object
            if object_type == "scene":
                # Save PlantGL objects
                Saver = get_saver("BGEOMSaver")
            elif object_type == "controls":
                Saver = get_saver("CPickleSaver")
            saver = Saver()
            saver.save(object_[sub_object], filename)
     
    def _save_scripts(self):
        warnings.warn("project._save_scripts is deprecated. Please use project._save('scripts') instead.")
        self._save("scripts")     
     
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
        
    def __repr__(self):
        return "Project named " + str(self.name) + " in path " + str(self.path) + " . Scripts: " + str(self.scripts.keys()) 

    def _set_ipython(self, shell=None):
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

    def is_project(self):
        return True
        
    def is_script(self):
        return False