
import abc
import inspect
import pkg_resources
import site

from openalea.core.pkgmanager import UnknownPackageError
from openalea.vpltk.pluginmanager import PluginManager

from openalea.core.node import NodeFactory
from openalea.core.signature import Signature

class InterfaceFactory(NodeFactory):
    def __init__(self, interface, **kargs):
        name = interface.identifier
        description = interface.__doc__
        category='interfaces'

        if hasattr(interface, '__authors__'):
            authors = interface.__authors__
        else :
            authors = ''

        s = Signature(interface.__init__)

        super(InterfaceFactory, self).__init__(name=name,
                 description=description,
                 category=category,
                 inputs=s.parameters,
                 outputs=None,
                 authors=authors)

        self.interface = interface

    def instantiate(self):
        return self.interface


class ObjectFactory(NodeFactory):
    def __init__(self,
                 name,
                 description = '',
                 category = '',
                 interfaces=None,
                 inputs=None,
                 outputs=None,
                 nodemodule = '',
                 nodeclass = None,
                 search_path = None,
                 authors = None,
                 **kargs):
        super(ObjectFactory, self).__init__(name=name,
                 description=description,
                 category=category,
                 inputs=inputs,
                 outputs=outputs,
                 nodemodule=nodemodule,
                 nodeclass=nodeclass,
                 search_path=search_path,
                 authors=authors)

        if interfaces is None:
            self.__interfaces__ = []
        else:
            self.__interfaces__ = interfaces

class Catalog(object):
    def __init__(self, verbose=True):
        self.plugin_types = ('wralea', 'plugin')
        self.groups = set() 
        self.managers = {}


    def init(self):
        paths = site.getsitepackages()
        for path in paths:
            distribs = pkg_resources.find_distributions(path)
            for distrib in distribs :
                for group in distrib.get_entry_map():
                    self.groups.add(group)

        self.groups = [group for group in self.groups]
        self.tags = self._clean_lst(self.groups)

    def _clean_lst(self, lst):
        lst = [item for item in lst]
        for plugin_type in self.plugin_types :
            if plugin_type in lst :
                lst.remove(plugin_type)
        return lst

    def get_interfaces(self):
        all_interfaces = set()
        for pl in self.get_factories(tags=['plugin']):
            interfaces = self.interfaces(pl)
            for interface in interfaces :
                all_interfaces.add(interface)
        return all_interfaces

    def get_interface_id(self, interface):
        if isinstance(interface, basestring):
            return interface
        if isinstance(interface, InterfaceFactory):
            return self.get_interface_id(interface.instantiate())
        if hasattr(interface, 'identifier'):
            return interface.identifier
        else :
            return 'builtin:%s.%s' % (interface.__module__, interface.__name__)

    def interfaces(self, obj):
        all_interfaces = set()
        if obj is None :
            return all_interfaces

        # Check if obj is an Interface factory
        if isinstance(obj, InterfaceFactory):
            all_interfaces.add(self.get_interface_id(obj))

        # Check interfaces defined in openalea factories
        if hasattr(obj, '__interfaces__'):
            for interface in obj.__interfaces__:
                all_interfaces.add(self.get_interface_id(interface))

        if not inspect.isclass(obj):
            obj = obj.__class__

        # Check interfaces defined using traits.provides
        if hasattr(obj, '__implements__'):
            for interface in obj.__implements__.getBases():
                all_interfaces.add(self.get_interface_id(interface))

        return all_interfaces


    def is_implementation(self, obj, interface):
        if interface is None :
            return True

        if isinstance(interface, abc.ABCMeta):
            return isinstance(obj, interface)
        else :
            return self.get_interface_id(interface) in self.interfaces(obj)

    def is_implementation_old(self, obj, interface):
        # If interface is not defined, it means no constrains so return True
        if interface is None :
            return True

        if isinstance(interface, basestring):
            if interface in self.interfaces(obj):
                return True
            else:
                return False

        if isinstance(interface, InterfaceFactory):
            return self.is_implementation(obj, interface.instantiate().identifier)

        if isinstance(interface, abc.ABCMeta):
            if isinstance(obj, interface):
                return True
            else :
                if hasattr(interface, 'identifier'):
                    identifier = interface.identifier
                else :
                    identifier = 'ABCMeta:%s.%s' % (interface.__module__, interface.__name__)
                    return self.is_implementation(obj, identifier)


        # If obj is an instance, use class
        if not inspect.isclass(obj):
            obj = obj.__class__
    
    
        # Check with issubclass (Derivated from interface or defined using metaclass)
        if issubclass(obj, interface):
            return True
    
        return False

    def _getplugin(self, plugin_type, interfaces, identifier, tags):
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
                    if identifier and factory.name != identifier :
                        continue
                    if self.is_implementation(factory, interfaces):
                        lst.append(factory)
        return lst

    def get_factories(self, interfaces=None, identifier=None, tags=None):
        lst = []
        if tags is None :
            tags = self.groups

        # Scan standard entry_points : 1 entry_point = 1 object
        for tag in self._clean_lst(tags) :
            for ep in pkg_resources.iter_entry_points(tag, identifier) :
                if self.is_implementation(ep, interfaces):
                    lst.append(ep)

        # Scan openalea entry_points : 1 entry_point = n factories
        for tag in self.plugin_types:
            if tag in tags :
                lst += self._getplugin(tag, interfaces, identifier, tags)

        return lst

    def get_factory(self, interfaces=None, identifier=None, tags=None):
        lst = self.get_factories(interfaces, identifier, tags)
        if lst :
            return lst[0]

