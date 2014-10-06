# -*- python -*-
#
#       Plugin System for vpltk
#
#       OpenAlea.VPLTk: Virtual Plants Lab Toolkit
#
#       Copyright 2013 INRIA - CIRAD - INRA
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

import abc
import inspect
import pkg_resources
import site
import sys

from openalea.core.pkgmanager import UnknownPackageError
from openalea.oalab.legacy.catalog.pluginmanager import PluginManager
from openalea.core.singleton import Singleton
from openalea.core.interface import IInterface

# TODO
# Write a short description of what do methods

class Catalog(object):

    __metaclass__ = Singleton

    def __init__(self, verbose=True):
        self.plugin_types = ('wralea', 'plugin', 'adapters', 'interfaces')
        self.groups = set()
        self.managers = {}

        self._services = {}
        self._interfaces = {}
        self._lowername = {}

        # list all path supporting python modules
        paths = site.getsitepackages()
        usersite = site.getusersitepackages()
        if isinstance(usersite, basestring):
            paths.append(usersite)
        elif isinstance(usersite, (tuple, list)):
            paths += list(usersite)
        paths += sys.path

        # scan all entry_point and list different groups
        for path in set(paths):
            distribs = pkg_resources.find_distributions(path)
            for distrib in distribs :
                for group in distrib.get_entry_map():
                    self.groups.add(group)

        self.groups = [group for group in self.groups]
        self.tags = self._clean_lst(self.groups)

        self._load_interfaces()

    def _clean_lst(self, lst):
        lst = [item for item in lst]
        for plugin_type in self.plugin_types :
            if plugin_type in lst :
                lst.remove(plugin_type)
        return lst

    def _load_interfaces(self):
        # load all interfaces defined in __plugin__.py files.
        for pl in self.factories(tags=['plugin', 'interfaces']):
            if inspect.isclass(pl) and issubclass(pl, IInterface):
                interface = pl
                for parent in inspect.getmro(interface):
                    if hasattr(parent, 'name'):
                        self._interfaces[parent.name] = parent
                        self._lowername[parent.name.lower()[1:]] = parent.name

    def interface(self, name):
        interface_id = self.interface_id(name)
        return self._interfaces.get(interface_id)

    def interface_id(self, interface):
        if isinstance(interface, basestring):
            return interface
        elif inspect.isclass(interface) and issubclass(interface, IInterface):
            if hasattr(interface, 'name'):
                return interface.name
            else :
                return 'builtin:%s.%s' % (interface.__module__, interface.__name__)
        elif inspect.isclass(interface) :
            return interface.__name__
        else:
            raise NotImplementedError


    def interfaces(self, obj=None):
        if obj is None :
            return self._interfaces
        all_interfaces = set()

        # Check interfaces defined in openalea factories
        if hasattr(obj, '__interfaces__'):
            for interface in obj.__interfaces__:
                # Currently, interfaces can be defined as "string identifier" or directly using interface class
                # If interface class is used, get its "string identifier".
                interface_id = self.interface_id(interface)
                if interface_id in self._interfaces: # check if interface_id is yet known by Catalog
                    # Search parent interfaces
                    interface = self._interfaces[interface_id]
                    for parent in inspect.getmro(interface):
                        parent_id = self.interface_id(parent)
                        all_interfaces.add(parent_id)
                else :
                    # Cannot reach real interface class, so add it directly
                    all_interfaces.add(self.interface_id(interface))

        if not inspect.isclass(obj):
            obj = obj.__class__

        # Check interfaces defined using traits.provides
        if hasattr(obj, '__implements__'):
            for interface in obj.__implements__.getBases():
                all_interfaces.add(self.interface_id(interface))

        return all_interfaces


    def is_implementation(self, obj, interface):
        if interface is None :
            return True

        if isinstance(interface, abc.ABCMeta):
            return isinstance(obj, interface)
        else :
            return self.interface_id(interface) in self.interfaces(obj)

    def _getplugin(self, plugin_type, interfaces, name, tags):
        lst = []

        if plugin_type not in self.managers :
            manager = PluginManager(plugin_type=plugin_type)
            manager.init()
            self.managers[plugin_type] = manager
        else:
            manager = self.managers[plugin_type]

        for pkgname in manager.iterkeys() :
            try:
                factories = manager[pkgname]
            except UnknownPackageError :
                pass
            else:
                for factory in factories.itervalues():
                    if name and factory.name != name :
                        continue
                    if self.is_implementation(factory, interfaces):
                        lst.append(factory)

        return lst

    def factories(self, interfaces=None, name=None, tags=None, exclude_tags=None):
        """
        :param exclude_tags: if tags is not specified, scan all tags except one defined in exclude_tags
        :param interfaces: by default do not check interfaces so return all factories

        TODO: tags and exclude_tags need to be clarified
        """
        lst = []
        if tags and exclude_tags:
            print 'tags and exclude_tags are mutually exclusive'
        if exclude_tags is None:
            exclude_tags = ['wralea']

        if tags is None :
            tags = self.groups
            for tag in exclude_tags :
                if tag in tags :
                    tags.remove(tag)

        # Scan standard entry_points : 1 entry_point = 1 object
        for tag in self._clean_lst(tags) :
            for ep in pkg_resources.iter_entry_points(tag, name) :
                if self.is_implementation(ep, interfaces):
                    lst.append(ep)

        # Scan openalea entry_points : 1 entry_point = n factories (scan)
        for tag in self.plugin_types:
            if tag in tags :
                lst += self._getplugin(tag, interfaces, name, tags)

        return lst

    def factory(self, interfaces=None, name=None, tags=None, exclude_tags=None):
        """
        get factories matching given criteria (interfaces, name, tags).
        criterion=None means criterion is not used.
        If all criteria are None (default) it returns all factories.
        """
        lst = self.factories(interfaces, name, tags, exclude_tags)
        if lst :
            return lst[0]

    def create_service(self, object_factory, *args, **kargs):
        """
        Create a service from object_factory. If object_factory is None, returns None.
        If this factory is called for the first time, instantiate it with args and kargs.
        Else, use previous instance.
        """
        if object_factory is None :
            return None

        if object_factory in self._services :
            service = self._services[object_factory]
        else :
            service = object_factory.instantiate(*args, **kargs)
            self._services[object_factory] = service
        return service


    def service(self, interfaces=None, name=None, tags=None, exclude_tags=None, args=None, kargs=None):
        """
        args and kargs are not currently used but defined for future additional filters.
        For example "author='John Doe'".

        TODO: tags and exclude_tags need to be clarified
        """
        if args is None :
            args = []
        if kargs is None :
            kargs = {}
        if exclude_tags is None :
            exclude_tags = ['wralea']
        object_factory = self.factory(interfaces, name, tags, exclude_tags)
        return self.create_service(object_factory)

    def services(self, interfaces=None, name=None, tags=None, exclude_tags=None, args=None, kargs=None):
        """
        See :meth:`Catalog.service <openalea.vpltk.catalog.Catalog.service>`.
        """
        if args is None :
            args = []
        if kargs is None :
            kargs = {}
        if exclude_tags is None :
            exclude_tags = ['wralea']
        object_factories = self.factories(interfaces, name, tags, exclude_tags)
        services = []
        for object_factory in object_factories :
            services.append(self.create_service(object_factory, *args, **kargs))
        return services

    suppliers = services
    supplier = service
