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
from openalea.core import settings
import cPickle
from configobj import ConfigObj

def check_unicity(name, all_names):
    """
    Check if an object with the name 'name' is already registered
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
        self.path = path_(project_path)
        self.icon = ""
        self.authors = ""
        self.description = ""
        self.version = "0.1"
        self.license = "CeCILL-C"
        self.dependencies = []
        self.citation = ""
        
        self.localized = True # Set to False if you want to work with files that are outside project
        # REVIEW: localized generally references localization (see l10n, http://en.wikipedia.org/wiki/Software_localization)
        # maybe "embedded" or "local_files" ?
        self.shell = None
        self.set_ipython()
        
        self.ns = dict()
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
        self.start()
        
    def start(self):
        # Load in object
        self._load("startup")
        # Load in shell
        self._startup_import()
        self._startup_run()
        
        self.load()
        
    def save(self):
        root = path_(self.path)/self.name
        if not root.exists():
            os.mkdir(root)
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
            except NameError:
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
    # Get
    #----------------------------------------    
    def get(self, category, name):
        """
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
        
    #----------------------------------------
    # Add
    #----------------------------------------        
    def add_script(self, name, script):
        """
        Add a script in the project
        
        :param name: filename of the script to add (path or str)
        :param script: to add (string)
        """
        filename = path_(name)
        
        self.add("scripts", filename, script)
        
    def add(self, category, name, value):
        """
        Add a script in the project
        
        :param name: filename of the script to add (path or str)
        :param script: to add (string)
        """
        if not hasattr(self, category):
            setattr(self, category, dict())
        cat = getattr(self, category)
        cat[name] = value
        
    #----------------------------------------
    # Remove
    #----------------------------------------        
    def remove_script(self, name):
        """
        Add a script in the project
        
        Remove nothing in disk.
        
        :param name: filename of the script to remove (path or str)
        """
        filename = path_(name)
        
        if self.scripts.has_key(filename):
            # Remove in project
            del self.scripts[filename]        
        
    #----------------------------------------
    # Rename
    #---------------------------------------- 
    def rename(self, category, old_name, new_name):
        """
        Rename a script, a scene or a control in the project. Can rename the project too.
        
        :param category: Can be "script", "control", "scene" or "project" (str)
        :param old_name: current name of thing to rename (str)
        :param new_name: futur name of thing to rename (str)
        """
        if (category == "script") or (category == "scripts") or (category == "Models"):
            if not new_name:
                self.remove_script(old_name)
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
            
    def load(self):
        self._load_manifest()
        
        self.scripts = self._load("scripts")
        self.controls = self._load("controls")
        self.cache = self._load("cache")
        self.scene = self._load("scene")
        self.startup = self._load("startup")
        
    #----------------------------------------
    # Protected 
    #---------------------------------------- 
    def _load(self, object_type):
        """
        Load files listed in self.object_type.keys()
        """
        
        object_type = str(object_type)
        if object_type == "scene":
            return self._load_scene()
        
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
                if object_type == "scripts":
                    if filename.isabs():
                        pathname = filename
                return_object[filename] = open(pathname, 'rU').read()
                
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
        
            if hasattr(self, object_type):
                temp_path = self.path/self.name/object_type
                if not temp_path.exists():
                    return return_object
                files = getattr(self,object_type)
                files = files.keys()
            
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
        object_ = getattr(self, object_type)
        temp_path = self.path/self.name/object_type
        
        if not (self.path/self.name).exists():
            os.mkdir(self.path/self.name)
        
        if not temp_path.exists():
            os.mkdir(temp_path)
        
        # Hack to save plantgl object
        # REVIEW: PlantGL must not appear in vpltk
        if object_type == "scene":
            for sub_object in object_:
                name = str("%s/%s" %(temp_path,sub_object))
                object_[sub_object].save(name, "BGEOM")
        elif object_type == "scripts":  
            for sub_object in object_:
                sub_object = path_(sub_object)
                if sub_object.isabs():
                    file_ = open(sub_object, "w")
                    # try, except IOError
                else:
                    file_ = open(temp_path/sub_object, "w")
                code = str(object_[sub_object])
                code_enc = code.encode("utf8","ignore") 
                file_.write(code_enc)
                file_.close()
        else:
            for sub_object in object_:
                file_ = open(temp_path/sub_object, "w")
                # Hack to save controls with cPickle
                if object_type == "controls":
                    cPickle.dump(object_[sub_object],file_,0)
                else:
                    code = str(object_[sub_object])
                    code_enc = code.encode("utf8","ignore") 
                    file_.write(code_enc)
                file_.close()
     
    def _save_manifest(self):
        """
        Save in a manifest file what is present inside a project
        """
        config = ConfigObj()
        config.filename = self.path/self.name/"oaproject.cfg"
        
        config['metadata'] = dict()
        config['manifest'] = dict()
        
        for info in ['name', 'icon', 'authors', 'description', 'version', 'license', 'dependencies']:
            config['metadata'][info] = getattr(self, info)
            
        for files in ['scripts', 'controls', 'scene', 'cache', 'startup']:
            filenames = getattr(self, files)
            if filenames.keys():
                config['manifest'][files] = filenames.keys()

        config.write()
        
    def _load_manifest(self):
        """
        Load a project from a manifest file
        
        :warning: load metadata and list of filenames but does not load files
        """
        config = ConfigObj(self.path/self.name/"oaproject.cfg")
        if config.has_key('metadata'):
            for info in ['name', 'icon', 'authors', 'description', 'version', 'license', 'dependencies']:
                if config['metadata'].has_key(info):
                    setattr(self, info, config['metadata'][info])

        if config.has_key('manifest'):
            # Load file names in good place (dict.keys()) but don't load entire object:
            # ie. load keys but not values
            for files in ['scripts', 'controls', 'scene', 'cache', 'startup']:
                if config['manifest'].has_key(files):
                    filedict = dict()
                    for f in config['manifest'][files]:
                        filedict[f] = ""
                    setattr(self, files, filedict)

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
        return "Project named " + str(self.name) + " in path " + str(self.path) + " . Scripts: " + str(self.scripts.keys()) + " . Controls: " + str(self.controls.keys()) + " . Scene: " + str(self.scene.keys())


