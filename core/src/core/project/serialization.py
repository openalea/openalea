# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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

from openalea.core.serialization import AbstractSaver
from openalea.core.path import path as Path
from configobj import ConfigObj
from openalea.core.service.interface import interface_name


class ProjectLoader(object):
    dtype = ['IProject']
    protocols = ['inode/directory']
    options = ['config_filename=oaproject.cfg', 'default_metadata']

    def load(self, path, protocol=None, **kwds):
        from openalea.core.project import Project
        project = Project(path)
        return self.update(project, path, protocol=protocol, **kwds)

    def update(self, obj, path, protocol=None, **kwds):
        project = obj
        default_metadata = kwds.pop('default_metadata', project.DEFAULT_METADATA)
        default_categories = kwds.pop('default_categories', project.DEFAULT_CATEGORIES)
        config_filename = kwds.pop('config_filename', 'oaproject.cfg')

        config = ConfigObj(path / config_filename)
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
                if interface_name(default_metadata[info].interface) == 'ISequence':
                    if isinstance(value, basestring):
                        value = value.split(',')
                setattr(project, info, value)

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

                if category in default_categories:
                    filenames = config["manifest"][old_category]
                    if not isinstance(filenames, list):
                        filenames = [filenames]
                    for filename in filenames:
                        section = '%s.path' % category
                        if section in config:
                            if filename in config[section]:
                                project._add_item(category, path=config[section][filename], mode=project.MODE_LINK)
                            else:
                                project._add_item(category, filename=filename, mode=project.MODE_COPY)
                        else:
                            project._add_item(category, filename=filename, mode=project.MODE_COPY)
        return project


class ProjectSaver(AbstractSaver):
    dtype = ['IProject']
    protocols = ['inode/directory']
    options = [
        {'name': 'mode', 'interface': 'IStr', 'value': 'all', 'values': ['all', 'metadata']}
    ]

    def save(self, obj, path, protocol=None, **kwds):
        mode = kwds.pop('mode', 'all')

        path = Path(path)
        config_filename = kwds.get('config_filename', 'oaproject.cfg')
        config_path = path / config_filename

        if mode == 'all':
            if not path.exists():
                path.makedirs()
            self._save_metadata(obj, config_path)
            lines = self._save_controls(obj)
            with open(path / 'control.py', 'w') as f:
                for line in lines:
                    f.write(line)
        elif mode == 'metadata':
            if path.exists():
                self._save_metadata(obj, config_path)
        else:
            raise NotImplementedError('mode=%s' % mode)

    def _save_metadata(self, obj, path):
        path.touch()
        from configobj import ConfigObj
        config = ConfigObj()
        if not path.isfile():
            return

        config.filename = path
        config['manifest'] = dict()
        config['metadata'] = obj.metadata

        for category in obj.DEFAULT_CATEGORIES:
            filenames_dict = getattr(obj, category)
            if filenames_dict:
                category_path = obj.path / category
                if not category_path.exists():
                    category_path.makedirs()
                config['manifest'][category] = []
                for filename in sorted(filenames_dict.keys()):
                    data = filenames_dict[filename]
                    if hasattr(data, 'save'):
                        data.save()
                        config['manifest'][category].append(data.name)

                        # If data is stored outside project, register data.path in section category.path
                        if data.path.parent != category_path:
                            section = category + ".path"
                            config.setdefault(section, {})[data.name] = data.path
        config.write()

    def _save_controls(self, obj):
        from openalea.core.control.serialization import ControlSerializer
        from openalea.core.control.manager import ControlManager
        cm = ControlManager()
        controls = cm.controls()
        if controls:
            serializer = ControlSerializer()
            lines = serializer.serialize(controls)
        else:
            lines = []
        return lines
