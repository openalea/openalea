
import os
from openalea.core.observer import Observed
from openalea.core.path import path as Path
from openalea.vpltk.project.configobj import ConfigObj
from openalea.vpltk.project.loader import get_loader
from openalea.vpltk.project.saver import get_saver

from openalea.oalab.service.data import new_data
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
        "world",
        "startup",
        "doc",
        "lib",
        ]

    config_filename = "oaproject.cfg"

    def __init__(self, name, projectdir, **kwargs):
        Observed.__init__(self)

        self.metadata = {}
        self.categories = {}

        self.name = name
        self.projectdir = path(projectdir)

        # Fill metadata
        for k in self.metadata_keys:
            if k in kwargs:
                self.metadata[k] = kwargs[k]
            else:
                self.metadata[k] = self.metadata_keys[k].value

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
        path, filename, content, datatype
        """
        if obj:
            # TODO: Check obj follow Data or Model interface ??
            getattr(self, category)[obj.name] = obj
            return obj
        else:
            if 'filename' in kwargs
                filename = f
            new_data(category, )
            path = self.path/category


