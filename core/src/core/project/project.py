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

__all__ = [
    "Project",
    "ErrorInvalidItem",
    "ErrorInvalidItemName",
    "ErrorItemExistsInProject",
]

from collections import OrderedDict
import copy
import os

from openalea.core.control import Control
from openalea.core.data import Data
from openalea.core.observer import Observed
from openalea.core.path import path as Path
from openalea.core.project.configobj import ConfigObj
from openalea.core.customexception import CustomException
from openalea.core.service.data import DataFactory
from openalea.core.service.interface import interface_name
from openalea.core.service.model import to_model, ModelFactory


class ErrorInvalidItemName(CustomException):
    title = u'Error: item name is not valid'
    message = u'%(name)r is not valid'
    desc = u"Item name must not be empty, contain punctuation (except '_')or non ascii character"

    def _kargs(self):
        return dict(
            project=self._args[0],
            category=self._args[1],
            name=self._args[2],
        )


class ErrorItemExistsInProject(CustomException):
    title = u'Error: item exists in project yet.'
    message = u'Item %(name)s is in project yet'
    desc = u"As item is in project yet, yu cannot add it again. Use replacement instead"

    def _kargs(self):
        return dict(
            project=self._args[0],
            category=self._args[1],
            name=self._args[2],
        )


class ErrorInvalidItem(CustomException):
    title = u'Error: item is invalid'
    message = u'Item is invalid: %(message)s'
    desc = u"Item is invalid"

    def _kargs(self):
        return dict(message=self._args[0])


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
                # readlink return an absolute path or relative path depending on symlink.
                # If symlink is a relative link, parent path is used to generate an absolute path
                # Default path behaviour when concatenating two absolute paths is to keep only second one:
                # path('/a/1')/path('/b/2') -> path('/b/2')
                # So, if symlink is absolute, all is ok
                _path = _path.parent / _path.readlink()
        return _path.abspath()
    else:
        return path.abspath()


class MetaData(Control):
    pass


class CategoryInfo(dict):
    pass


class Project(Observed):

    DEFAULT_METADATA = OrderedDict([
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

    DEFAULT_CATEGORIES = OrderedDict([
        ("cache", CategoryInfo(title='Temporary Data')),
        ("data", CategoryInfo(title='Data')),
        ("model", CategoryInfo(title='Model')),
        ("world", CategoryInfo(title='World')),
        ("startup", CategoryInfo(title='Startup')),
        ("doc", CategoryInfo(title='Documentation')),
        ("lib", CategoryInfo(title='Libraries')),
    ])

    config_filename = "oaproject.cfg"

    MODE_COPY = 'copy'
    MODE_LINK = 'link'

    def __init__(self, path, **kwargs):
        self.categories = kwargs.get('categories', self.DEFAULT_CATEGORIES)
        Observed.__init__(self)

        self.metadata = OrderedDict()

        # listeners = kwargs['listeners'] if 'listeners' in kwargs else []
        # for listener in listeners:
        #    self.register_listener(listener)

        self.started = False
        self._path = _normpath(path)

        # Fill metadata
        for k, v in self.DEFAULT_METADATA.iteritems():
            self.metadata[k] = kwargs.get(k, v.value)

        # Allocate category dictionaries
        for k in self.categories:
            self.__dict__[k] = {}

        if self._path.exists():
            self._load()
        #    self.notify_listeners(('project_loaded', (self, self.path)))
        # else:
        #    self.notify_listeners(('project_created', (self, self.path)))
        # self.notify_listeners(('project_changed', self))

        self.ns = {}

    def __setattr__(self, key, value):
        if key == "categories":
            return super(Project, self).__setattr__(key, value)
        elif key in self.DEFAULT_METADATA:
            old_value = self.metadata[key]
            if old_value != value:
                self.metadata[key] = value
                self.notify_listeners(('metadata_changed', (self, key, old_value, value)))
                self.notify_listeners(('project_changed', self))
        elif key in self.categories:
            raise NameError("cannot change '%s' attribute" % key)
        else:
            return super(Project, self).__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.DEFAULT_METADATA:
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
    def title(self):
        if hasattr(self, 'label'):
            return self.label
        elif hasattr(self, 'alias'):
            return self.alias
        else:
            return ' '.join(self.name.capitalize().split('_'))

    @property
    def icon_path(self):
        """
        :return: the complete path of the icon. To modify it, you have to modify the path of project,
                 the name of project and/or the self.icon.
        """
        icon_name = None
        if self.icon:
            if not self.icon.startswith(':'):
                # local icon
                icon_name = self.path / self.icon
        return icon_name

    def start(self, *args, **kwargs):
        """
        Load controls if available, execute all files in startup.
        """
        self._load_controls()
        self.started = True
        self.ns.clear()
        loading_code = [
            'import sys',
            'sys.path.insert(0, %r)' % str(self.path / 'lib')
        ]
        loading_code = '\n'.join(loading_code)
        loading = ModelFactory(mimetype='text/x-python')
        ns = loading.run_code(loading_code, self.ns)
        self.ns.update(ns)
        for startup in self.startup.values():
            model = to_model(startup)
            ns = model.run_code(startup.read(), self.ns)
            self.ns.update(ns)
        interpreter = kwargs.get('shell')
        if interpreter:
            interpreter.shell.user_ns.clear()
            interpreter.shell.init_user_ns()
            interpreter.shell.user_ns.update(self.ns)

    def stop(self, *args, **kwargs):
        self.started = False
        self.ns.clear()
        from openalea.core.control.manager import ControlManager
        cm = ControlManager()
        cm.clear()

    def run(self, filename, *args, **kwargs):
        model = self.get_runnable_model(filename)
        return self.run_model(model)

    def run_model(self, model, *args, **kwargs):
        ns = {}
        ns.update(self.ns)
        ns.update(kwargs.pop('namespace', {}))
        ns["Model"] = self.get_runnable_model
        return model.run(*args, namespace=ns, **kwargs)

    def add(self, category, obj=None, **kwargs):
        return self.add_item(category, obj, **kwargs)

    def get(self, category, name, **kwargs):
        return self.get_item(category, name)

    def remove(self, category, obj=None, **kwargs):
        return self.remove_item(category, obj=obj, **kwargs)

    def _add_item(self, category, obj=None, **kwargs):
        mode = kwargs.pop('mode', self.MODE_COPY)
        if obj and isinstance(obj, Data):
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
        elif obj:
            category_dict = getattr(self, category)
            if obj.name not in category_dict:
                category_dict[str(obj.name)] = obj
            else:
                raise ValueError("data '%s' already exists in project '%s'" % (obj.name, self.alias))
        else:
            filename = Path(kwargs.pop('filename')) if 'filename' in kwargs else None
            content = kwargs.pop('content', None)
            dtype = kwargs.pop('dtype', None)
            mimetype = kwargs.pop('mimetype', None)
            path = Path(kwargs.pop('path')) if 'path' in kwargs else None
            # If project path exists, ie project exists on disk,
            # Create category dir if necessary
            category_path = self.path / category
            if self.path.exists() and not category_path.exists():
                category_path.makedirs()

            if filename:
                new_path = self.path / category / filename.name
            elif path:
                if not path.exists():
                    raise ErrorInvalidItem("path '%s' doesn't exists" % path)
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
            obj = self._add_item(category, data_obj, **kwargs)

        obj.package = self
        return obj

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

    def valid_item_name(self, category, name):
        if not name:
            return ErrorInvalidItemName(self, category, name)

        data = self.get_item(category, name)
        if data:
            return ErrorItemExistsInProject(self, category, name)

        path = self.path / category / name
        if data is None and path.exists():
            return Warning("Data yet exists on disk. Just add it.")

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
            # Update item paths
            for category in self.categories:
                for item in self.items(category).values():
                    if hasattr(item, 'path'):
                        item.path = dest / category / item.path.name
            # Move all files
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
                    LST=', '.join([repr(str(_model.filename)) for _model in found_models])
                )
                raise ValueError('%(NUM)d model have basename %(BASENAME)r: %(LST)s' % dic)

    def get_runnable_model(self, name):
        data = self.get_model(name)
        if data:
            model = to_model(data)
            if model:
                return copy.copy(model)

    def _load(self):
        """
        *Partially load* a project from a manifest file.

        1. Read manifest file (oaproject.cfg).
        2. Load metadata inside project from manifest.
        3. Create Data objects for each file inside project.

        .. warning::

            **Doesn't** load data content ! If you want to load data,
            please use :meth:`Data.read<openalea.oalab.model.model.Data.read>`.

        """
        from .serialization import ProjectLoader
        loader = ProjectLoader()
        loader.update(self, self.path, mode='lazy')

    def _save_manifest(self):
        from .serialization import ProjectSaver
        saver = ProjectSaver()
        saver.save(self, self.path, config_filename=self.config_filename, mode='metadata')

    def save_metadata(self):
        self._save_manifest()

    def _load_controls(self):
        from openalea.core.control.serialization import ControlLoader
        from openalea.core.service.control import register_control
        control_path = self.path / 'control.py'
        loader = ControlLoader()
        controls = loader.load(control_path)
        for control in controls:
            register_control(control)

    def save(self):
        """
        Save a manifest file on disk. It name is defined by config_filename.

        It contains **list of files** that are inside project (*manifest*) and **metadata** (author, version, ...).
        """
        from .serialization import ProjectSaver
        saver = ProjectSaver()
        saver.save(self, self.path, config_filename=self.config_filename)
        self.notify_listeners(('project_saved', self))
