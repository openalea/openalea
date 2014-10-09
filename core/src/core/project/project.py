# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>, Guillaume Baty <guillaume.baty@inria.fr>
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

It stores **metadata** (alias, author, description, version, license, ...) and **data** (src, models, images, ...).

You have here the default architecture of the project saved in directory "project".


    /project
        oaproject.cfg        (Configuration file)
        /model          (Files sources, Script Python, LPy...)
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

        project = Project(path="/path/to/proj/project")
        project.add(category="model", filename="hello.py", content="print 'Hello World'")
        project.author = "John Doe"
        project.description = "This project is used to said hello to everyone"
        project.save()
"""

import os

from openalea.core.observer import Observed
from openalea.core.path import path as Path
from openalea.core.project.configobj import ConfigObj
from openalea.core.service.interface import interface_name
from openalea.core.service.data import DataFactory
from openalea.core.control import Control

from collections import OrderedDict

def _normpath(path):
    """
    Replace all symlink in path with real path and return its absolute path
    For example, if given path is "local/bin/python" and "local" is a symbolic link to "/usr/local",
    returned path will be "/usr/local/bin/python"
    """
    if hasattr(os, 'readlink'):
        parts = Path(path).splitall()
        _path = Path('')
        for p in parts:
            _path = _path / p
            if _path.islink():
                _path = _path.readlink()
        return _path.abspath()
    else:
        return path.abspath()

class MetaData(Control):
    pass

class CategoryInfo(dict):
    pass

class Project(Observed):

    metadata_keys = OrderedDict([
        ("alias", MetaData('alias', 'IStr', 'MyProject')),
        ("icon", MetaData('icon', 'IFileStr', '')),
        ("authors", MetaData('author', 'ISequence', [])),
        ("description", MetaData('description', 'IStr')),
        ("long_description", MetaData('long_description', 'IStr')),
        ("citation", MetaData('citation', 'IStr')),
        ("url", MetaData('url', 'IStr')),
        ("dependencies", MetaData('dependencies', 'ISequence')),
        ("license", MetaData('license', 'IStr')),
        ("version", MetaData('version', 'IStr', '0.1')),
        ])

    category_keys = OrderedDict([
        ("cache", CategoryInfo(title='Temporary Data')),
        ("data", CategoryInfo(title='Data')),
        ("model", CategoryInfo(title='Models')),
        ("world", CategoryInfo(title='World')),
        ("startup", CategoryInfo(title='Startup')),
        ("doc", CategoryInfo(title='Documentation')),
        ("lib", CategoryInfo(title='Libraries')),
        ])

    config_filename = "oaproject.cfg"

    MODE_COPY = 'copy'
    MODE_LINK = 'link'

    def __init__(self, path, **kwargs):
        Observed.__init__(self)

        self.metadata = OrderedDict()
        self.categories = {}

        # listeners = kwargs['listeners'] if 'listeners' in kwargs else []
        # for listener in listeners:
        #    self.register_listener(listener)

        self.started = False
        self._path = _normpath(path)

        # Fill metadata
        for k, v in self.metadata_keys.iteritems():
            self.metadata[k] = kwargs.get(k, v.value)


        # Allocate category dictionaries
        for k in self.category_keys:
            self.__dict__[k] = {}

        if self._path.exists():
            self._load()
        #    self.notify_listeners(('project_loaded', (self, self.path)))
        # else:
        #    self.notify_listeners(('project_created', (self, self.path)))
        # self.notify_listeners(('project_changed', self))

        self.ns = {}

    def __setattr__(self, key, value):
        if key in self.metadata_keys:
            old_value = self.metadata[key]
            if old_value != value:
                self.metadata[key] = value
                self.notify_listeners(('metadata_changed', (self, key, old_value, value)))
                self.notify_listeners(('project_changed', self))
        elif key in self.category_keys:
            raise NameError, "cannot change '%s' attribute" % key
        else:
            return super(Project, self).__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.metadata_keys:
            return super(Project, self).__getattribute__('metadata')[key]
        else:
            return super(Project, self).__getattribute__(key)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self.path))

    @property
    def path(self):
        return self._path

    @property
    def projectdir(self):
        return self._path.parent

    @property
    def name(self):
        return self._path.name

    @property
    def icon_path(self):
        """
        :return: the complete path of the icon. To modify it, you have to modify the path of project, the name of project and/or the self.icon.
        """
        icon_name = None
        if self.icon:
            if not self.icon.startswith(':'):
                # local icon
                icon_name = self.path / self.icon
        return icon_name

    def start(self,*args,**kwargs):
        """
        Load controls if availabe, execute all files in startup.
        """
        self._load_controls()
        self.started = True
        self.ns.clear()
        loading = [
          'import sys',
          'sys.path.insert(0, %r)' % str(self.path / 'lib')
          ]
        loading = '\n'.join(loading)
        for startup in self.startup.values():
            ns = startup.execute_in_namespace(loading, self.ns)
            self.ns.update(ns)
            ns = startup.execute_in_namespace(startup.read(), self.ns)
            self.ns.update(ns)

    def stop(self, *args, **kwargs):
        self.started = False
        self.ns.clear()
        from openalea.core.control.manager import ControlManager
        cm = ControlManager()
        cm.clear()

    def run(self, filename, *args, **kwargs):
        model = self.get_model(filename)
        model.ns.update(self.ns)
        model.run(*args, **kwargs)

    def add(self, category, obj=None, **kwargs):
        return self.add_item(category, obj, **kwargs)

    def get(self, category, name, **kwargs):
        return self.get_item(category, name)

    def remove(self, category, obj=None, **kwargs):
        return self.remove_item(category, obj=obj, **kwargs)

    def _add_item(self, category, obj=None, **kwargs):
        mode = kwargs['mode'] if 'mode' in kwargs else self.MODE_COPY
        if obj:
            # TODO: Check obj follow Data or Model interface ??
            new_path = self.path / category / obj.path.name
            if obj.path != new_path and mode == self.MODE_COPY:
                # TODO: use Data.copy instead
                return self._add_item(category, path=obj.path, **kwargs)

            category_dict = getattr(self, category)
            if obj.filename not in category_dict:
                category_dict[str(obj.filename)] = obj
            else:
                raise ValueError("data '%s' already exists in project '%s'" % (obj.filename, self.alias))
            return obj
        else:
            filename = Path(kwargs['filename']) if 'filename' in kwargs else None
            content = kwargs['content'] if 'content' in kwargs else None
            dtype = kwargs['dtype'] if 'dtype' in kwargs else None
            mimetype = kwargs['mimetype'] if 'mimetype' in kwargs else None
            path = Path(kwargs['path']) if 'path' in kwargs else None
            # If project path exists, ie project exists on disk,
            # Create category dir if necessary
            category_path = self.path / category
            if self.path.exists() and not category_path.exists():
                category_path.makedirs()

            if filename:
                new_path = self.path / category / filename.name
            elif path:
                if not path.exists():
                    raise ValueError("path '%s' doesn't exists" % path)
                filename = path.name
                new_path = self.path / category / filename
            else:
                raise ValueError("path or filename required")

            if path is None:
                path = new_path

            # If data was outside project, we try to fix it.
            # If mode is "prefer copy", we try to copy file inside project
            # If copy fails, we get original content and pass it to new data
            # If mode is "prefer link", we just keep original path (keep outside project)
            # TODO: Move to Data.copy
            data_obj = None
            if new_path.abspath() != path.abspath() and mode == self.MODE_COPY:
                try:
                    path.copyfile(new_path)
                except IOError:
                    data_obj = DataFactory(path, mimetype, dtype=dtype, default_content=content)
                    content = data_obj.read()
                else:
                    content = None
            elif new_path.abspath() != path.abspath() and mode == self.MODE_LINK:
                new_path = path
            else:
                pass
                # Nothing to do, data is yet in the right place

            data_obj = DataFactory(new_path, mimetype, dtype=dtype, default_content=content)
            return self._add_item(category, data_obj, **kwargs)

    def _remove_item(self, category, obj=None, **kwargs):
        category_dict = getattr(self, category)
        filename = kwargs['filename'] if 'filename' in kwargs else None
        if obj is None and filename is None:
            raise ValueError('You must specify a data object or a filename')
        if obj is not None:
            filename = obj.filename

        if self.get(category, filename):
            del category_dict[filename]

    def _rename_item(self, category, old, new):
        pold = Path(old)
        pnew = Path(new)
        if pold.isabs() or pnew.isabs() or pnew.name != new or pold.name != old:
            raise ValueError('You must give filename only, not path')

        new_path = self.path / category / new
        data = self.get_item(category, old)
        data.move(new_path)
        self._remove_item(category, filename=old)
        self._add_item(category, data)


    def _project_changed(self):
        self.notify_listeners(('project_changed', self))
        self._save_manifest()

    def add_item(self, category, obj=None, **kwargs):
        data = self._add_item(category, obj, **kwargs)
        self.notify_listeners(('data_added', (self, category, data)))
        self._project_changed()
        return data

    def remove_item(self, category, obj=None, **kwargs):
        if obj:
            filename = obj.filename
        elif 'filename' in kwargs:
            filename = kwargs['filename']
        self._remove_item(category, obj=obj, **kwargs)
        self.notify_listeners(('data_removed', (self, category, filename)))
        self._project_changed()

    def rename_item(self, category, old, new):
        if old == new:
            return
        self._rename_item(category, old, new)
        self.notify_listeners(('data_renamed', (self, category, old, new)))
        self._project_changed()

    def delete(self):
        raise NotImplementedError

    def rename(self, new):
        dest = self.path.parent / new
        self.move(dest)

    def move(self, dest):
        src = self.path
        dest = Path(dest).abspath()
        if src == dest:
            return
        if src.exists():
            src.move(dest)
        self._path = dest
        self.notify_listeners(('project_moved', (self, src, dest)))
        self._project_changed()

    def items(self, category, **kwds):
        return getattr(self, category)

    def get_item(self, category, filename):
        files = getattr(self, category)
        return files.get(filename)

    def get_model(self, filename):
        model = self.get_item('model', filename)
        if model is not None:
            return model
        else:
            found_models = []
            for modelname in self.model:
                if filename == Path(modelname).namebase:
                    found_models.append(self.get_item('model', modelname))

            nmodels = len(found_models)
            if nmodels == 0:
                return None
            elif nmodels == 1:
                return found_models[0]
            else:
                dic = dict(
                    NUM=nmodels,
                    BASENAME=str(Path(modelname).namebase),
                    LST=', '.join([repr(str(model.filename)) for model in found_models])
                    )
                raise ValueError('%(NUM)d model have basename %(BASENAME)r: %(LST)s' % dic)

    def _load(self):
        """
        *Partially load* a project from a manifest file.

        1. Read manifest file (oaproject.cfg).
        2. Load metadata inside project from manifest.
        3. Create Data objects for each file inside project.
        :warning: **Doesn't** load data content ! If you want to load data, please use :meth:`Data.read<openalea.oalab.model.model.Data.read>`.

        """
        config = ConfigObj(self.path / self.config_filename)
        if 'metadata' in config:
            for info in config["metadata"].keys():
                if info == 'name':
                    info = 'alias'
                    value = config['metadata']['name']
                elif info == 'author':
                    info = 'authors'
                    value = config['metadata']['author']
                elif info == 'author_email':
                    continue
                else:
                    value = config['metadata'][info]
                if interface_name(self.metadata_keys[info].interface) == 'ISequence':
                    if isinstance(value, basestring):
                        value = value.split(',')
                setattr(self, info, value)

        if 'manifest' in config:
            # Load file names in right place (dict.keys()) but don't load entire object:
            # ie. load keys but not values
            for category in config["manifest"].keys():

                # Backward compatibility
                if category == 'src':
                    category = 'model'
                    old_category = 'src'
                else:
                    old_category = category

                if category in self.category_keys:
                    filenames = config["manifest"][old_category]
                    if not isinstance(filenames, list):
                        filenames = [filenames]
                    for filename in filenames:
                        section = '%s.path' % category
                        if section in config:
                            if filename in config[section]:
                                self._add_item(category, path=config[section][filename], mode=self.MODE_LINK)
                            else:
                                self._add_item(category, filename=filename, mode=self.MODE_COPY)
                        else:
                            self._add_item(category, filename=filename, mode=self.MODE_COPY)

    def _save_manifest(self):
        config = ConfigObj()
        config_path = self.path / self.config_filename
        if not config_path.isfile():
            return

        config.filename = config_path
        config['manifest'] = dict()
        config['metadata'] = self.metadata

        for category in self.category_keys:
            filenames_dict = getattr(self, category)
            if filenames_dict:
                category_path = self.path / category
                if not category_path.exists():
                    category_path.makedirs()
                config['manifest'][category] = []
                for filename in sorted(filenames_dict.keys()):
                    data = filenames_dict[filename]
                    data.save()
                    config['manifest'][category].append(data.filename)

                    # If data is stored outside project, register data.path in section category.path
                    if data.path.parent != category_path:
                        section = category + ".path"
                        config.setdefault(section, {})[data.filename] = data.path

        config.write()

    def save_metadata(self):
        self._save_manifest()


    def _save_controls(self):
        from openalea.core.control.pyserial import save_controls
        from openalea.core.control.manager import ControlManager
        cm = ControlManager()
        if cm.controls():
            save_controls(cm.controls(), self.path / 'control.py')

    def _load_controls(self):
        control_path = self.path / 'control.py'
        if control_path.isfile():
            code = file(control_path, 'r').read()
            exec(code)

    def save(self):
        """
        Save a manifest file on disk. It name is defined by config_filename.

        It contains **list of files** that are inside project (*manifest*) and **metadata** (author, version, ...).
        """
        if not self.path.exists():
            self.path.makedirs()
        config_path = self.path / self.config_filename
        config_path.touch()
        self._save_controls()
        self._save_manifest()
        self.notify_listeners(('project_saved', self))



