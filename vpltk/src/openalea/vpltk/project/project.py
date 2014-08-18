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
from openalea.vpltk.project.configobj import ConfigObj
from openalea.vpltk.project.loader import get_loader
from openalea.vpltk.project.saver import get_saver

from openalea.oalab.service.data import data
from openalea.oalab.control.control import Control
#125, 133, 136, 144, 148, 151, 160, 208, 225, 238-240, 244, 250, 253-254, 259, 261, 283-284, 296, 311, 337

class MetaData(Control):
    pass

class Project(Observed):

    metadata_keys = {
        "alias":MetaData('alias', 'IStr', 'MyProject'),
        "icon":MetaData('icon', 'IFileStr', 'icon.png'),
        "author":MetaData('author', 'ISequence', []),
        "author_email":MetaData('author_email', 'IStr'),
        "description":MetaData('description', 'IStr'),
        "long_description":MetaData('long_description', 'IStr'),
        "citation":MetaData('citation', 'IStr'),
        "url":MetaData('url', 'IStr'),
        "dependencies":MetaData('dependencies', 'ISequence'),
        "license":MetaData('license', 'IStr'),
        "version":MetaData('version', 'IStr', '0.1'),
        }

    category_keys = [
        "cache",
        "data",
        "model",
        "world",
        "startup",
        "doc",
        "lib",
        ]

    config_filename = "oaproject.cfg"

    MODE_COPY = 'copy'
    MODE_LINK = 'link'

    def __init__(self, path, **kwargs):
        Observed.__init__(self)

        self.metadata = {}
        self.categories = {}

        # listeners = kwargs['listeners'] if 'listeners' in kwargs else []
        # for listener in listeners:
        #    self.register_listener(listener)

        self.started = False
        self._path = Path(path).normlink().abspath()

        # Fill metadata
        for k in self.metadata_keys:
            if k in kwargs:
                self.metadata[k] = kwargs[k]
            else:
                self.metadata[k] = self.metadata_keys[k].value

        # Allocate category dictionaries
        for k in self.category_keys:
            self.__dict__[k] = {}

        if self.path.exists():
            self._load()
        #    self.notify_listeners(('project_loaded', (self, self.path)))
        # else:
        #    self.notify_listeners(('project_created', (self, self.path)))
        # self.notify_listeners(('project_changed', self))

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
            return object.__setattr__(self, key, value)

    def __getattr__(self, key):
        if key in self.metadata_keys:
            return object.__getattribute__(self, 'metadata')[key]
        else:
            return object.__getattribute__(self, key)

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

    def start(self,*args,**kwargs):
        self.started = True

    def add(self, category, obj=None, **kwargs):
        return self.add_item(category, obj, **kwargs)

    def get(self, category, name, **kwargs):
        return self.get_item(category, name)

    def remove(self, category, name, **kwargs):
        return self.remove_item(category, name, **kwargs)

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
                category_dict[obj.filename] = obj
            else:
                raise ValueError("data '%s' already exists in project '%s'" % (obj.filename, self.alias))
            return obj
        else:
            filename = Path(kwargs['filename']) if 'filename' in kwargs else None
            content = kwargs['content'] if 'content' in kwargs else None
            dtype = kwargs['dtype'] if 'dtype' in kwargs else None
            path = Path(kwargs['path']) if 'path' in kwargs else None

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
            if new_path.abspath() != path.abspath() and mode == self.MODE_COPY:
                try:
                    path.copyfile(new_path)
                except IOError:
                    data_obj = data(path, dtype, default_content=content)
                    content = data_obj.read()
                else:
                    content = None
            elif new_path.abspath() != path.abspath() and mode == self.MODE_LINK:
                new_path = path
            else:
                pass
                # Nothing to do, data is yet in the right place

            data_obj = data(new_path, dtype, default_content=content)
            return self._add_item(category, data_obj, **kwargs)

    def _remove_item(self, category, filename):
        if self.get(category, filename):
            files = getattr(self, category)
            del files[filename]

    def _rename_item(self, category, old, new):
        if old == new:
            return
        data = self.get_item(category, old)
        data.rename(new)
        self._remove_item(category, old)
        self._add_item(category, data)

    def add_item(self, category, obj=None, **kwargs):
        data = self._add_item(category, obj, **kwargs)
        self.notify_listeners(('data_added', (self, category, data)))
        self.notify_listeners(('project_changed', self))
        return data

    def remove_item(self, category, filename):
        self._remove_item(category, filename)
        self.notify_listeners(('data_removed', (self, category, filename)))
        self.notify_listeners(('project_changed', self))

    def rename_item(self, category, old, new):
        if old == new:
            return
        self._rename_item(category, old, new)
        self.notify_listeners(('data_renamed', (self, category, old, new)))
        self.notify_listeners(('project_changed', self))

    def delete(self):
        raise NotImplementedError

    def rename(self, new):
        dest = self.path.parent / new
        self.move(dest)

    def move(self, dest):
        src = self.path
        if src == dest:
            return
        if src.exists():
            src.move(dest)
        self._path = dest
        self.notify_listeners(('project_moved', (self, src, dest)))
        self.notify_listeners(('project_changed', self))

    def get_item(self, category, filename):
        files = getattr(self, category)
        return files.get(filename)

    def get_model(self, filename):
        return self.get('model', filename)

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
                else:
                    value = config['metadata'][info]
                setattr(self, info, value)

        if 'manifest' in config:
            # Load file names in right place (dict.keys()) but don't load entire object:
            # ie. load keys but not values
            for category in config["manifest"].keys():
                if category in self.category_keys:
                    filenames = config["manifest"][category]
                    if not isinstance(filenames, list):
                        filenames = [filenames]
                    for filename in filenames:
                        section = '%s.path' % category
                        if section in config:
                            if filename in config[section]:
                                self.add(category, path=config[section][filename], mode=self.MODE_LINK)
                            else:
                                self.add(category, filename=filename, mode=self.MODE_COPY)
                        else:
                            self.add(category, filename=filename, mode=self.MODE_COPY)

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
                for data in filenames_dict.values():
                    data.save()
                    config['manifest'][category].append(data.filename)

                    # If data is stored outside project, register data.path in section category.path
                    if data.path.parent != category_path:
                        section = category + ".path"
                        config.setdefault(section, {})[data.filename] = data.path

        config.write()

    def save_metadata(self):
        self._save_manifest()

    def save(self):
        """
        Save a manifest file on disk. It name is defined by config_filename.

        It contains **list of files** that are inside project (*manifest*) and **metadata** (author, version, ...).
        """
        if not self.path.exists():
            self.path.makedirs()
        config_path = self.path / self.config_filename
        config_path.touch()
        self._save_manifest()
        self.notify_listeners(('project_saved', self))



