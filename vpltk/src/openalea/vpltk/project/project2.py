
import os
from openalea.core.observer import Observed
from openalea.core.path import path as Path
from openalea.vpltk.project.configobj import ConfigObj
from openalea.vpltk.project.loader import get_loader
from openalea.vpltk.project.saver import get_saver

from openalea.oalab.service.data import data
from openalea.oalab.control.control import Control


class MetaData(Control):
    pass

class Project(Observed):

    metadata_keys = {
#         "name":MetaData('name', 'IStr', 'MyProject'),
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

    def __init__(self, name, projectdir, **kwargs):
        Observed.__init__(self)

        self.metadata = {}
        self.categories = {}

        self.name = name
        self.projectdir = Path(projectdir)

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

    def __setattr__(self, key, value):
        if key in self.metadata_keys:
            old_value = self.metadata[key]
            if old_value != value:
                self.metadata[key] = value
                self.notify_listeners(('project_changed', self))
                self.notify_listeners(('metadata_changed', (self, key, old_value, value)))
        elif key in self.category_keys:
            raise NameError, 'cannot change %s attribute' % key
        else:
            return object.__setattr__(self, key, value)

    def __getattr__(self, key):
        if key in self.metadata_keys:
            return object.__getattribute__(self, 'metadata')[key]
        else:
            return object.__getattribute__(self, key)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.projectdir)

    @property
    def path(self):
        return self.projectdir / self.name

    def add(self, category, obj=None, **kwargs):
        """
        path, filename, content, dtype
        """
        mode = kwargs['mode'] if 'mode' in kwargs else self.MODE_COPY
        if obj:
            # TODO: Check obj follow Data or Model interface ??
            new_path = self.path / category / obj.path.name
            if obj.path != new_path and mode == self.MODE_COPY:
                # TODO: use Data.copy instead
                return self.add(category, path=obj.path, **kwargs)

            category_dict = getattr(self, category)
            if obj.filename not in category_dict:
                category_dict[obj.filename] = obj
            else:
                raise ValueError("data '%s' already exists in project '%s'" % (obj.filename, self.name))
            return obj
        else:
            filename = Path(kwargs['filename']) if 'filename' in kwargs else None
            content = kwargs['content'] if 'content' in kwargs else None
            dtype = kwargs['dtype'] if 'dtype' in kwargs else None
            path = Path(kwargs['path']) if 'path' in kwargs else None

            if filename:
                new_path = self.path / category / filename.name
                name = filename.namebase
            elif path:
                if not path.exists():
                    raise ValueError("path '%s' doesn't exists" % path)
                filename = path.name
                name = filename.namebase
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
                    data_obj = data(path, name, dtype, default_content=content)
                    content = data_obj.read()
                else:
                    content = None
            elif new_path.abspath() != path.abspath() and mode == self.MODE_LINK:
                new_path = path
            else:
                pass
                # Nothing to do, data is yet in the right place

            data_obj = data(new_path, name, dtype, default_content=content)
            return self.add(category, data_obj, **kwargs)

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
                setattr(self, info, config['metadata'][info])

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

    def save(self):
        """
        Save a manifest file on disk. It name is defined by config_filename.

        It contains **list of files** that are inside project (*manifest*) and **metadata** (author, version, ...).
        """
        config = ConfigObj()

        config.filename = self.path / self.config_filename

        if not self.path.exists():
            self.path.makedirs()

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
        self.notify_listeners(('project_saved', self))

