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
"""
---------------------------------------
Project and Project Manager Quick Start
---------------------------------------

You can create load or save a *project* thanks to the *project manager*.

.. code-block:: python

    from openalea.vpltk.project.manager import ProjectManager
    # Instanciate ProjectManager
    project_manager = ProjectManager()
    # Discover available projects
    project_manager.discover()
    print project_manager.projects

    # Create project in default directory or in specific one
    p1 = project_manager.create('project1')
    p2 = project_manager.create('project2', '/path/to/project')
    # Load project from default directory or in specific one
    p3 = project_manager.load('project3')
    p4 = project_manager.load('project4', '/path/to/project')

To search projects that are not located inside default directories:

.. code-block:: python

    project_manager.find_links.append('path/to/search/projects')
    project_manager.discover()
    print project_manager.projects

You can then manipulate *proj* and these attributes (name, description, scripts, startup)

.. code-block:: python

    # Metadata
    p1.rename("project", "project1", "numpy_project")
    p1.authors = "OpenAlea Consortium and me"
    p1.description = "Test project concept with numpy"
    p1.long_description = '''This project import numpy.
    Then, it create and display a numpy eye.
    We use it to test concept of Project.'''

    # Data management
    p1.add("startup", "begin_numpy.py", "import numpy as np")
    p1.add("scripts", "eye.py", "print np.eye(2)")
    p1.rename("scripts", "eye.py", "eye_numpy.py")
    print p1.get("scripts", "eye_numpy.py")

    # Save
    p1.save()

    # Load
    p2 = project_manager.load("numpy_project")
    # Run startup
    p2.start()
    # Run script
    p2.run_script("eye_numpy.py")

"""

import os
import warnings
from openalea.core.path import path as path_
from openalea.vpltk.project.configobj import ConfigObj
from openalea.vpltk.project.loader import get_loader
from openalea.vpltk.project.saver import get_saver


class Project(object):
    """
    The Project is a structure which permit to manage different objects.

    It store **metadata** (name, authors, description, version, license, ...) and **data** (scripts, models, images, ...).

    You have here the default architecture of the project named "project_name",
    stored in your computer.

    /project_name
        oaproject.cfg        (Configuration file)
        /scripts          (Files sources, Script Python, LPy...)
        /controls       (Controls, like color map or curve)
        /scene          (scene, scene 3D)
        /cache          (Intermediary saved objects)
        /data           (Data files like images, .dat, ...)
        /startup          (Preprocessing scripts)
            *.py            (Preprocessing scripts)
            *import*.py     (Libs and packages to import in preprocessing)

    :use:
        .. code-block:: python

            project1 = Project(project_name="mynewproj", project_path="/path/to/proj")
            project1.start()
            project1.add(category="scripts", name"hello.py", value="print 'Hello World'")
            project1.authors = "John Doe"
            project1.description = "This project is used to said hello to everyone"
            project1.save()
    """

    _to_save_in_manifest = ['scripts', 'controls', 'scene', 'cache', 'startup']
    _to_save_in_metadata = ['name', 'icon', 'authors', 'description', 'version', 'license', 'dependencies',
                            'long_description']
    def __init__(self, project_name, project_path):
        """
        :param project_name: name of the project to create or load
        :param project_path: path of the project to create or load
        """
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
        # Abstract this part as self.folders
        self.scripts = dict()
        self.controls = dict()
        self.cache = dict()
        self.data = dict()
        self.scene = dict()
        self.startup = dict()

        #
        self._ns = dict()
        self._shell = None
        self._set_ipython()

    #----------------------------------------
    # Public API
    #----------------------------------------    
    def create(self):
        """
        Do the same thing that start method.

        .. seealso:: :func:`start` :func:`load` :func:`load_manifest`
        """
        self.start()

    def start(self):
        """
        1. :func:`load` objects into project.
        2. Import startup.
        3. Run preprocessing.

        .. seealso:: :func:`load` :func:`load_manifest`
        """
        # Load in object
        self.load()
        # Load in shell
        self._startup_import()
        self._startup_run()

    def load(self):
        """
        Realize a total loading of project (contrary to :func:`load_manifest`).

        1. Load manifest :func:`load_manifest`
        2. Read data files listed in manifest and fill project object.

        .. seealso:: :func:`start` :func:`load_manifest`
        """
        self.load_manifest()
        for category in self._to_save_in_manifest:
            obj = self._load(str(category))
            setattr(self, category, obj)

    def save(self):
        """
        Save project on disk.

        1. Save **data** files.
        2. Save **metadata** and **list on previously saved data** into a manifest file (*oaproject.cfg*).

        .. seealso:: :func:`save_manifest`
        """
        for category in self._to_save_in_manifest:
            self._save(str(category))
        self.save_manifest()

    def get(self, category, name):
        """
        Search an object inside project and return it.

        :param category: category of object to get
        :param name: name of object to get
        :return: object named *name* in the category *category* if it exists. Else, None.

        :use: >>> get(category="scripts", name="myscript.py")

        .. seealso:: :func:`add`
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

        .. seealso:: :func:`get` :func:`remove`
        """
        if not hasattr(self, category):
            setattr(self, category, dict())
        cat = getattr(self, category)
        cat[name] = value

    def remove(self, category, name):
        """
        Remove an object in the project
        
        Remove nothing on disk.
        
        :param category: category of object to remove ("scripts", "control", "scene", ...) (str)
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
        Rename a script, a scene or a control in the project.
        If category is project, rename the entire project.
        
        :param category: Can be "script", "control", "scene" or "project" (str)
        :param old_name: current name of thing to rename (str)
        :param new_name: future name of thing to rename (str)
        """
        if (category == "project"):
            self.name = new_name
            self.save()
            if (self.path/old_name).exists():
                try:
                    (self.path / old_name).removedirs()
                except IOError:
                    pass
        else:
            if hasattr(self, category):
                cat = getattr(self, category)
                # Rename in project
                cat[str(new_name)] = cat[str(old_name)]
                # Remove inside project
                self.remove(category, old_name)
                # Remove on disk
                temp_path = self.path / self.name / category / old_name
                if temp_path.exists():
                    try:
                        path_(temp_path).removedirs()
                    except IOError:
                        pass

    #----------------------------------------
    # Manifest
    #---------------------------------------- 
    def save_manifest(self):
        """
        Save a manifest file on disk. His name is "*oaproject.cfg*".

        It contains **list of files** that are inside project (*manifest*) and **metadata** (authors, version, ...).

        .. seealso:: :func:`load_manifest`
        """
        config = ConfigObj()
        config.filename = self.path / self.name / "oaproject.cfg"

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
        *Partially load* a project from a manifest file.

        1. Read manifest file (oaproject.cfg).
        2. Load metadata inside project from manifest.
        3. Load **filenames** of data files inside project from manifest.
        4. **Not** load data ! If you want to load data, please use :func:`load`.
        
        :warning: load metadata and list of filenames but does not load files

        .. seealso:: :func:`save_manifest` :func:`load`
        """
        config = ConfigObj(self.path / self.name / "oaproject.cfg")
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

        :deprecated: replace by :func:`add` method
        :param name: filename of the script to add (path or str)
        :param script: to add (string)

        .. seealso:: :func:`add`
        """
        warnings.warn(
            "project.add_script(name, script) is deprecated. Please use project.add('scripts', name, script) instead.")
        self.add("scripts", name, script)

    def remove_script(self, name):
        """
        Add a script in the project
        
        Remove nothing on disk.

        :deprecated: replace by :func:`remove` method
        :param name: filename of the script to remove (path or str)

        .. seealso:: :func:`remove`
        """
        warnings.warn("project.remove_script(name) is deprecated. Please use project.remove('scripts', name) instead.")
        self.remove("scripts", name)

    def run_script(self, name):
        """
        Try to run the script named *name* into current shell

        """
        script = self.get("scripts", name)
        exec(script, self._ns)

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
            temp_path = self.path / self.name / object_type

            if not temp_path.exists():
                return return_object

            files = getattr(self, object_type)
            files = files.keys()
            for filename in files:
                filename = path_(filename)
                pathname = self.path / self.name / object_type / filename
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
                self._ns[cache_name] = eval(str(return_object[cache_name]), self._ns)

        return return_object

    def _save(self, object_type):
        object_type = str(object_type)
        object_ = getattr(self, object_type)
        temp_path = self.path / self.name / object_type

        # Make default directories if necessary
        if not (self.path / self.name).exists():
            os.mkdir(self.path / self.name)
        if not temp_path.exists():
            os.mkdir(temp_path)

        for sub_object in object_:
            filename = temp_path / sub_object
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
                exec (self.startup[s], self._ns)
                if use_ip:
                    self._shell.runcode(self.startup[s])

    def _startup_run(self):
        use_ip = self.use_ipython()

        for s in self.startup:
            if s.find('import') == -1:
                exec (self.startup[s], self._ns)
                if use_ip:
                    self._shell.runcode(self.startup[s])

    def __repr__(self):
        return "Project named " + str(self.name) + " in path " + str(self.path) + " . Scripts: " + str(
            self.scripts.keys())

    def _set_ipython(self, shell=None):
        if not self.use_ipython():
            try:
                # Try to get automatically current IPython shell
                shell = get_ipython()
            except:
                shell = None
        self._shell = shell

    def use_ipython(self):
        """
        :return: True if project is instaciated with a shell IPython. Else, return False.
        """
        if self._shell == None:
            return False
        else:
            return True

    def get_scene(self):
        """
        :return: self.scene (dict)
        """
        return self.scene

    def is_project(self):
        """
        :return: True
        """
        return True

    def is_script(self):
        """
        :return: False
        """
        return False

    @property
    def ns(self):
        return self._ns
    
    