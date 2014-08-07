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
The Project is a structure which permits to manage different objects.

It stores **metadata** (name, author, description, version, license, ...) and **data** (src, models, images, ...).

You have here the default architecture of the project named "name",
stored in your computer.


    /name
        oaproject.cfg        (Configuration file)
        /src          (Files sources, Script Python, LPy...)
        /control       (Control, like color map or curve)
        /world          (scene, scene 3D)
        /cache          (Intermediary saved objects)
        /data           (Data files like images, .dat, ...)
        /lib            (Contains python modules and packages)
        /startup          (Preprocessing scripts)
            *.py            (Preprocessing scripts)
            *import*.py     (Libs and packages to import in preprocessing)

:use:
    .. code-block:: python

        project1 = Project(name="mynewproj", projectdir="/path/to/proj")
        project1.start()
        project1.add(category="model", name="hello.py", value="print 'Hello World'")
        project1.author = "John Doe"
        project1.description = "This project is used to said hello to everyone"
        project1.save()
"""

import os
from openalea.core.path import path as path_
from openalea.vpltk.project.configobj import ConfigObj
from openalea.vpltk.project.loader import get_loader
from openalea.vpltk.project.saver import get_saver
from openalea.core.observer import Observed

from openalea.vpltk.plugin import iter_plugins

def _model_factories():
    models = {}
    for model in iter_plugins('oalab.model'):
        models[model.extension] = model
        models[model.default_name] = model
    return models


def remove_extension(filename):
    filename_split = filename.split(".")
    if len(filename_split) > 1:
        return ".".join(filename_split[:-1])
    else:
        return filename_split[0]


def safe_remove(dirpath):
    """
    Try to remove directories *dirpath*
    :param dirpath: path of directory to remove
    :return: True if success, else False
    """
    dirpath = path_(dirpath)
    if dirpath.isdir():
        if dirpath.exists():
            try:
                dirpath.removedirs()
            except IOError:
                pass
            except OSError:
                pass
            else:
                return True
    return False


class Project(Observed):
    """
    :param name: name of the project to create or load
    :param path: path of the project to create or load
    """
    model_klasses = _model_factories()

    def __init__(self, name, projectdir,
                 icon="", author="OpenAlea Consortium", author_email="",
                 description="", long_description="", citation="", url="", dependencies=[], license="CeCILL-C",
                 version="0.1"):
        Observed.__init__(self)
        # Metadata
        self._projectdir = path_(projectdir)
        self.metadata = {
            "name": str(name),
            "icon": path_(icon),
            "author": str(author),
            "author_email": str(author_email),
            "description": str(description),
            "long_description": str(long_description),
            "citation": str(citation),
            "url": str(url),
            "dependencies": dependencies,
            "license": str(license),

            "version": str(version),
        }
        self.config_file = "oaproject.cfg"

        # Data
        self.files = {
            "cache": dict(),
            "data": dict(),
            "world": dict(),
            "startup": dict(),
            "doc": dict(),
            "lib": dict()
        }

        self._model = dict()
        self._control = None
        self._control_name = ["ctrls"]
        self._dirty = {'project':False}
        self.notify_listeners(('project_change', self))
        self.state = 'Not loaded' # partially loaded, loaded
        self.started = False

    #----------------------------------------
    # Public API
    #----------------------------------------
    def start(self, shell=None, namespace={}):
        """
        1. :func:`load` objects into project.
        2. Import startup.
        3. Run preprocessing.

        :param shell: shell to run startup. Has to have the method "runcode(code)". Default, None.
        :param namespace: dict used to run the sources. Default, empty dict.

        .. seealso:: :func:`load` :func:`load_manifest`
        """
        # Algorithm
            # Change dir and save current dir
            # Read ressources: introspection
            # import (startup)


        # Load in object
        # Lazy Load
        self.load_manifest()
        self.load()
        # Load in shell
        self._startup(shell, namespace)
        self.started = True

    def categories(self):
        return ['model'] + self.files.keys()

    def load(self):
        """
        Realize a total loading of project (contrary to :func:`load_manifest`).

        1. Load manifest :func:`load_manifest`
        2. Read data files listed in manifest and fill project object.

        .. seealso:: :func:`start` :func:`load_manifest`
        """
        self.load_manifest()
        for category in self.files:
            obj = self._load(str(category))
            setattr(self, category, obj)
            
        # Lazy load
        """
        visualea_models = []
        for model_name in self._model_names:
            # Hack to fix a bug:
            # if a visualea model use an other model that is not loaded, the project crash.
            # To fix it, we load visualea models at the end.
            # To really fix it: fix inside ModelNode (Visualea)
            # TODO: Fix this hack
            if str(model_name).split(".")[-1] == "wpy":
                visualea_models.append(model_name)            
            # Load all scripts models
            else:
                self._load("model", str(model_name))
        # Load visualea models       
        for model_name in visualea_models:
            self._load("model", str(model_name))"""

        self.state = 'loaded'
        self.notify_listeners(('project_change', self))

    def save(self):
        """
        Save project on disk.

        1. Save **data** files.
        2. Save **metadata** and **list on previously saved data** into a manifest file (*oaproject.cfg*).

        .. seealso:: :func:`save_manifest`
        """
        for category in self.files.keys():
            self._save(str(category))
        self._save("model")
        self.save_manifest()
        self.notify_listeners(('project_change', self))

    def save_as(self, projectdir, name):
        """ save project in a new folder """
        projectdir = path_(projectdir)
        
        # copy project folder content
        self.path.copytree(projectdir/name, symlinks=True)
        
        # save project
        self.projectdir = projectdir
        self.name = name
        self.save()
            
    def get(self, category, name):
        """
        Search an object inside project and return it.

        :param category: category of object to get
        :param name: name of object to get
        :return: object named *name* in the category *category* if it exists. Else, None.

        .. seealso:: :func:`add`
        """
        if category == "model":
            return self.get_model(name)
        elif hasattr(self, category):
            cat = getattr(self, category)
            if name in cat:
                return cat[name]
        return None

    def add(self, category, name, value, dtype=None):
        """
        Add an object in the project

        :param category: *type* of object to add ("src", "control", "world", ...)
        :param name: filename of the object to add with extension (path or str)
        :param value: to add (string)

        .. seealso:: :func:`get` :func:`remove`
        """
        self._dirty[category] = True
        if category == "model":
            success = self.new_model(name=name, code=value, dtype=dtype)
        else:
            if not hasattr(self, category):
                setattr(self, category, dict())
            cat = getattr(self, category)
            cat[name] = value
            success = True

        if success:
            self._save(category)
            self.save_manifest()
            self.notify_listeners(('project_change', self))
            return success

    def add_model(self, model):
        """
        Add an existing model to the project.

        :param model: model to add to the project (have to exists)

        .. seealso:: :func:`get` :func:`new_model`
        """
        self._model[model.name] = model
        self.notify_listeners(('project_change', self))

    def new_model(self, name, code="", filepath="", inputs=[], outputs=[], dtype=None):
        """
        Create a model and add it to the project.

        :param name: name of model to create with extension
        :param code: object that will be manipulated as model
        :param filepath: path where model will be saved
        :param inputs: list of inputs of the model
        :param outputs: list of outputs of the model

        :return: True if added with success

        .. seealso:: :func:`get` :func:`add_model`
        """
        self._dirty['model'] = True
        filename = path_(name)
        if dtype is None:
            dtype = filename.ext[1:]
        if not filepath:
            filepath = filename
        if dtype in self.model_klasses:
            # add model to existing models
            model = self.model_klasses[dtype](name=name, code=code, filepath=filepath, inputs=inputs, outputs=outputs)
            self.add_model(model)
            return True
        return False

    def new(self, category, name, dtype=None, value=""):
        # TODO: rewrite this hackish method
        if category == 'model':
            for model_class in iter_plugins('oalab.model'):
                if model_class.default_name == dtype:
                    model = model_class(name=name, code=value)
                    self.add_model(model)
        else:
            self.add(category, name, value)

    def remove(self, category, name):
        """
        Remove an object in the project

        Remove on disk too.

        :param category: category of object to remove ("src", "control", "world", ...) (str)
        :param name: filename of the src to remove (path or str)
        """
        category = str(category)
        filename = path_(name)

        if category == "model":
            if name in self._model:
                del self._model[name]
        elif hasattr(self, category):
            cat = getattr(self, category)
            if filename in cat:
                del cat[filename]
        # Try to remove on disk
        temp_path = self.path / category / name
        safe_remove(temp_path)
        self.save_manifest()
        self.notify_listeners(('project_change', self))

    def rename(self, category, old_name, new_name):
        """
        Rename a *model*, a *world*, a *control*, ... in the project.
        If category is *project*, rename the entire project.


        :param category: Can be "model", "control", "world" or "project" (str)
        :param old_name: current name of thing to rename (str)
        :param new_name: future name of thing to rename (str)
        """
        old_name = str(old_name)
        new_name = str(new_name)

        if old_name == new_name:
            return

        self._dirty[category] = True
        category = str(category).lower()

        # rename project
        if category == "project":
            self.name = new_name
            self.save()
            safe_remove(self.projectdir / old_name)

        # rename a part of project
        else:
            if category in ["model", "models"]:
                old_model = self._model[old_name]
                old_model.name = new_name
                if old_model.extension :
                    old_model.filepath = path_('%s.%s' % (new_name, old_model.extension))
                else:
                    old_model.filepath = path_(new_name)
                self._model[new_name] = old_model
                self._save(category)
                self.remove(category, old_name)
            elif hasattr(self, category):
                cat = getattr(self, category)
                cat[new_name] = cat[old_name]
                self._save(category)
                self.remove(category, old_name)
            self.save_manifest()

        self.notify_listeners(('project_change', self))

    #----------------------------------------
    # Manifest
    #----------------------------------------
    def save_manifest(self):
        """
        Save a manifest file on disk. His name is "*oaproject.cfg*".

        It contains **list of files** that are inside project (*manifest*) and **metadata** (author, version, ...).

        .. seealso:: :func:`load_manifest`
        """
        config = ConfigObj()

        proj_path = self.path
        config.filename = proj_path / self.config_file

        if not proj_path.exists():
            proj_path.makedirs()

        config['metadata'] = dict()
        config['manifest'] = dict()

        config['metadata'] = self.metadata

        for category in self.files:
            filenames_dict = getattr(self, category)

            if filenames_dict:
                config['manifest'][category] = list(filenames_dict)

        modelnames = []
        for model in self._model:
            if self._model[model] is None:
                modelnames.append(model)
            else:
                modelnames.append(self._model[model].name + '.' + self._model[model].extension)

        config['manifest']["model"] = modelnames

        if self.control:
            # @GBY
            # Only used for introspection
            config['manifest']["control"] = self._control_name

        config.write()
        self.notify_listeners(('project_change', self))

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
        config = ConfigObj(self.path / self.config_file)
        if 'metadata' in config:
            for info in config["metadata"].keys():
                setattr(self, info, config['metadata'][info])

        if 'manifest' in config:
            # Load file names in good place (dict.keys()) but don't load entire object:
            # ie. load keys but not values
            for files in config["manifest"].keys():
                if files == "model":
                    model_names = config["manifest"]["model"]
                    if not isinstance(model_names, list):
                        model_names = [model_names]
                    for model_name in model_names:
                        self._model[model_name] = None
                elif files == "control":
                    # @GBY
                    # Only used for introspection
                    self._control_name = config["manifest"]["control"]
                else:
                    # Hack to stay backward compatible with first versions of projects
                    if files == "src":
                        for mod_name in config["manifest"]["src"]:
                            if path_(mod_name).isabs():
                                self._model[mod_name] = None
                            else:
                                mod_name2 = (self.path / "src" / mod_name)
                                self._model[mod_name2] = None
                    else:
                        filedict = dict()
                        for f in config['manifest'][files]:
                            filedict[f] = ""
                        setattr(self, files, filedict)
        self.state = 'partially loaded'

    #----------------------------------------
    # model
    #----------------------------------------
    def _solve_model_name(self, name):
        """
        Search to solve the name (conflict with or without extension...)
        
        :param name: name of the model to solve
        :return: the name of the model corresponding to the name in self._model.keys(). If nothing is found, return None.
        """
        if name in self.list_models():
            return name
        else:
            name_without_ext = remove_extension(name)
            if name_without_ext in self.list_models():
                return name_without_ext
            elif name in self.list_models_without_extension():
                for n in self.list_models():
                    if remove_extension(n) == name:
                        return n
            elif name_without_ext in self.list_models_without_extension():
                for n in self.list_models():
                    if remove_extension(n) == name_without_ext:
                        return n    
        return None
    
    def get_model(self, name):
        """
        Get one or various instances of models from this project.
        :param name: name of the file in self.src to convert into model. Can pass various names split by spaces. Can pass "*".
        :return: model object corresponding to the source named *name* in self.src. If various values, return a list of models. If failed, return None.

        .. seealso:: :func:`get_models`
        """
        # GBY: what happens if model name contain spaces ?!?
        if hasattr(name, "split"):
            names = name.split()
        else:
            names = [str(name)]
        return_models = []

        if "*" in names and len(names) == 1:
            names = self.list_models()

        if not isinstance(names, list):
            names = [names]

        for name in names:
            name_without_ext = remove_extension(name)
            list_models = self.list_models() + self.list_models_without_extension()
            if name in list_models or name_without_ext in list_models:
                new_name = self._solve_model_name(name) # change get_model
                if new_name is None:
                    raise Exception("Model with name " + name + " doesn't exist in project " + self.name)
                model = self._model[new_name]
                if model is None:
                    # if manifest is loaded but not models: load model
                    model = self._load("model", new_name)
                name = model.name
                return_models.append(model)               
            else:
                print "Model ", name, " doesn't exist in project ", self.name
                return
        # If only one model, don't return a list
        if len(return_models) == 1:
            return return_models[0]
        return return_models
        
    def list_models(self):
        return self._model.keys()
        
    def list_models_without_extension(self):
        return [remove_extension(modelname) for modelname in self.list_models()]
        
    def get_models(self):
        """
        :return: all models

        .. seealso:: :func:`get_model`
        """
        return self.get_model("*")
        
    # TODO : remove models and model
    def models(self):
        print "method project.models() is deprecated. Please use project.get_models()"
        return self.get_models()
        
    def model(self, name):
        print "method project.model(name) is deprecated. Please use project.get_model(name)"
        return self.get_model(name)

    #----------------------------------------
    # Protected
    #----------------------------------------
    def _load(self, object_type, object_name="", namespace={}):
        """
        Load files listed in self.object_type.keys()

        :param namespace: dict used to run the sources. Default, empty dict.
        """
        # TODO: use service to know how to load objects
        object_type = str(object_type)
        return_object = dict()

        if object_type == "model":
            code = ''
            if path_(object_name).isabs():
                filepath = path_(object_name)

                new_filepath = (self.path / "src").relpathto(filepath)
            else:
                filepath = self.path / "model" / object_name
                new_filepath = (self.path / "model").relpathto(filepath)
            try:
                f = open(filepath, "r")
                code = f.read()
                f.close()
            except Exception, e:
                raise e
            ext = path_(new_filepath).ext[1:]
            filename_without_ext = remove_extension(new_filepath)
            if ext in self.model_klasses:
                # add model to existing models
                mod = self.model_klasses[ext](name=filename_without_ext, code=code, filepath=new_filepath)
                if object_name in self._model:
                    # remove old model name
                    del self._model[object_name]
                self._model[filename_without_ext] = mod
                return self._model[filename_without_ext]
            else:
                raise Exception("Extension " + ext + " not found! Can't open model " + object_name)
                
        elif object_type == "control":
            # @GBY: 3 following lines
            from openalea.oalab.service.control import load_controls
            filepath = self.path / object_type / self._control_name
            self.control = load_controls(filepath)

        else:
            if hasattr(self, object_type):
                temp_path = self.path / object_type

                if not temp_path.exists():
                    return return_object

                files = getattr(self, object_type)
                files = files.keys()
                for filename in files:
                    filename = path_(filename)
                    pathname = self.path / object_type / filename
                    if filename.isabs():
                        # Load files that are outside project
                        pathname = filename
                    Loader = get_loader("GenericLoader")
                    if object_type == "control":
                        # TODO: to remove:
                        Loader = get_loader("CPickleLoader")
                    elif object_type == "world":
                        Loader = get_loader("BGEOMLoader")
                    elif object_type == "data":
                        Loader = get_loader("BinaryLoader")
                    loader = Loader()
                    result = loader.load(pathname)
                    return_object[filename] = result

            # hack to add cache in namespace
            if object_type == "cache":
                for cache_name in return_object:
                    namespace[cache_name] = eval(str(return_object[cache_name]), namespace)

            return return_object

    def _save(self, object_type):
        # TODO: use service to know how to save objects
        object_type = str(object_type)
        if object_type == "model":
            for model in self._model.itervalues():
                self.save_model(model)

        elif object_type == "control":
            # @GBY: 4 following lines
            from openalea.oalab.service.control import save_controls
            ctrls = self.control
            filepath = self.path / object_type / self._control_name
            save_controls(ctrls, filepath)

        else:
            object_ = getattr(self, object_type)
            if object_:
                temp_path = self.path / object_type

                # Make default directories if necessary
                if not (self.path).exists():
                    os.mkdir(self.path)
                if not temp_path.exists():
                    os.mkdir(temp_path)

                for sub_object in object_:
                    filename = temp_path / sub_object
                    sub_object = path_(sub_object)
                    Saver = get_saver()
                    if sub_object.isabs():
                        # Permit to save object outside project
                        filename = sub_object
                    if object_type == "world":
                        # Save PlantGL objects
                        Saver = get_saver("BGEOMSaver")
                    elif object_type == "control":
                        # TODO: to remove:
                        Saver = get_saver("CPickleSaver")
                    elif object_type == "data":
                        Saver = get_saver("BinarySaver")
                    saver = Saver()
                    saver.save(object_[sub_object], filename)

        if object_type in self._dirty:
            self._dirty[object_type] = False

    def save_model(self, model):
        if model is not None:
            filepath = model.abspath(parentdir=self.path / "model")

            Saver = get_saver()
            saver = Saver()
            saver.save(model.repr_code(), filepath)


    def _startup(self, shell=None, namespace={}):
        """
        :param shell: shell to run startup. Has to have the method "runcode(code)". Default, None.
        :param namespace: dict used to run the sources. Default, empty dict.
        """
        if not shell:
            shell = self.use_ipython()

        for s in self.startup:
            if shell:
                shell.run_cell(self.startup[s], silent=False)

        self.started = True

    def __str__(self):
        txt = "Project named " + str(self.name) + " in path " + str(self.projectdir) + """.
"""
        for metada in self.metadata:
            if self.metadata[metada]:
                txt = txt + metada + " : " + str(self.metadata[metada]) + ". "
        return txt


    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.projectdir)

    def use_ipython(self):
        """
        :return: the ipython shell if it exists. Else, return None.
        """
        shell = None
        try:
            # Try to get automatically current IPython shell
            shell = get_ipython()
        except NameError:
            pass

        return shell

    def get_scene(self):
        """
        :return: self.world (dict)
        """
        return self.get_world()

    def get_world(self):
        """
        :return: self.world (dict)
        """
        return self.world

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

    # Metadata
    @property
    def name(self):
        return self.metadata["name"]

    @name.setter
    def name(self, value):
        self.metadata["name"] = value
        self.notify_listeners(('project_change', self))

    @property
    def icon(self):
        return self.metadata["icon"]

    @icon.setter
    def icon(self, value):
        self.metadata["icon"] = value
        self.notify_listeners(('project_change', self))

    @property
    def author(self):
        return self.metadata["author"]

    @author.setter
    def author(self, value):
        self.metadata["author"] = value
        self.notify_listeners(('project_change', self))

    @property
    def author_email(self):
        return self.metadata["author_email"]

    @author_email.setter
    def author_email(self, value):
        self.metadata["author_email"] = value
        self.notify_listeners(('project_change', self))

    @property
    def description(self):
        return self.metadata["description"]

    @description.setter
    def description(self, value):
        self.metadata["description"] = value
        self.notify_listeners(('project_change', self))

    @property
    def long_description(self):
        return self.metadata["long_description"]

    @long_description.setter
    def long_description(self, value):
        self.metadata["long_description"] = value
        self.notify_listeners(('project_change', self))

    @property
    def citation(self):
        return self.metadata["citation"]

    @citation.setter
    def citation(self, value):
        self.metadata["citation"] = value
        self.notify_listeners(('project_change', self))

    @property
    def url(self):
        return self.metadata["url"]

    @url.setter
    def url(self, value):
        self.metadata["url"] = value
        self.notify_listeners(('project_change', self))

    @property
    def dependencies(self):
        return self.metadata["dependencies"]

    @dependencies.setter
    def dependencies(self, value):
        self.metadata["dependencies"] = value
        self.notify_listeners(('project_change', self))

    @property
    def license(self):
        return self.metadata["license"]

    @license.setter
    def license(self, value):
        self.metadata["license"] = value
        self.notify_listeners(('project_change', self))

    @property
    def version(self):
        return self.metadata["version"]

    @version.setter
    def version(self, value):
        self.metadata["version"] = value
        self.notify_listeners(('project_change', self))

    @property
    def control(self):
        return self._control

    @control.setter
    def control(self, value):
        self._control = value
        self.notify_listeners(('project_change', self))

    @property
    def cache(self):
        return self.files["cache"]

    @cache.setter
    def cache(self, value):
        self.files["cache"] = value
        self.notify_listeners(('project_change', self))

    @property
    def data(self):
        return self.files["data"]

    @data.setter
    def data(self, value):
        self.files["data"] = value
        self.notify_listeners(('project_change', self))

    @property
    def scene(self):
        return self.files["world"]

    @scene.setter
    def scene(self, value):
        self.files["world"] = value
        self.notify_listeners(('project_change', self))

    @property
    def world(self):
        return self.files["world"]

    @world.setter
    def world(self, value):
        self.files["world"] = value
        self.notify_listeners(('project_change', self))

    @property
    def startup(self):
        return self.files["startup"]

    @startup.setter
    def startup(self, value):
        self.files["startup"] = value
        self.notify_listeners(('project_change', self))

    @property
    def doc(self):
        """
        :return: the documentation of the project (str)
        """
        return self.files["doc"]

    @doc.setter
    def doc(self, value):
        self.files["doc"] = value
        self.notify_listeners(('project_change', self))

    @property
    def lib(self):
        return self.files["lib"]

    @lib.setter
    def lib(self, value):
        self.files["lib"] = value
        self.notify_listeners(('project_change', self))

    @property
    def path(self):
        return self.projectdir / self.name

    @property
    def projectdir(self):
        return self._projectdir

    @projectdir.setter
    def projectdir(self, projectdir):
        if str(projectdir) == '/Users/gbaty/prog/openalea/vplants-trunk/oalab':
            print
        self._projectdir = projectdir


    @property
    def icon_path(self):
        """
        :return: the complete path of the icon. To modify it, you have to modify the path of project, the name of project and/or the self.icon.
        """
        icon_name = None
        if self.icon:
            if not self.icon.startswith(':'):
                # local icon
                icon_name = path_(self.projectdir) / self.name / self.icon
        return icon_name

    @property
    def src(self):
        return self._model

    @property
    def dirty(self):
        for dirty in self._dirty:
            if dirty is True:
                return dirty
        return False
