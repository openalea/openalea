
import abc
import inspect
import pkg_resources
import site
import sys

from openalea.core.pkgmanager import UnknownPackageError
from openalea.vpltk.pluginmanager import PluginManager

from openalea.core.node import NodeFactory
from openalea.core.singleton import Singleton
from openalea.core.signature import Signature
from _pyio import __metaclass__

#TODO: review code for optimizations
#TODO: split in several modules

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

    def classobj(self):
        # The module contains the node implementation.
        module = self.get_node_module()
        classobj = module.__dict__.get(self.nodeclass_name, None)

        if classobj is None:
            raise Exception("Cannot instantiate '" + \
                self.nodeclass_name + "' from " + str(module))
        return classobj

    def instantiate(self, *args, **kargs):
        classobj = self.classobj()
        return classobj(*args, **kargs)

class Catalog(object):

    __metaclass__ = Singleton

    def __init__(self, verbose=True):
        self.plugin_types = ('wralea', 'plugin')
        self.groups = set() 
        self.managers = {}

        self._services = {}
        self._interfaces = {}

        paths = site.getsitepackages()
        usersite = site.getusersitepackages()
        if isinstance(usersite, basestring):
            paths.append(usersite)
        elif isinstance(usersite, (tuple, list)):
            paths += list(usersite)
        paths += sys.path

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
        for pl in self.get_factories(tags=['plugin']):
            if isinstance(pl, InterfaceFactory):
                interface = pl.instantiate()
                for parent in inspect.getmro(interface):
                    if hasattr(parent, 'identifier'):
                        self._interfaces[parent.identifier] = parent

    def get_interface_class(self, interface):
        interface_id = self.get_interface_id(interface)
        return self._interfaces.get(interface_id)

    def get_interfaces(self):
        return self._interfaces.iterkeys()

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

        # Check interfaces defined in openalea factories
        if hasattr(obj, '__interfaces__'):
            for interface in obj.__interfaces__:
                interface_id = self.get_interface_id(interface)
                if interface_id in self._interfaces:
                    # Search parent interfaces
                    interface = self._interfaces[interface_id]
                    for parent in inspect.getmro(interface):
                        parent_id = self.get_interface_id(parent)
                        all_interfaces.add(parent_id)
                else :
                    # Cannot reach real interface class, so add it directly
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

    def get_factories(self, interfaces=None, identifier=None, tags=None, exclude_tags=None):
        """
        exclude_tags: if tags is not specified, scan all tags except one defined in exclude_tags
        """
        lst = []
        if tags and exclude_tags:
            print 'tags and exclude_tags are mutually exclusive'
        if exclude_tags is None:
            exclude_tags = []

        if tags is None :
            tags = self.groups
            for tag in exclude_tags :
                if tag in tags :
                    tags.remove(tag)

        # Scan standard entry_points : 1 entry_point = 1 object
        for tag in self._clean_lst(tags) :
            for ep in pkg_resources.iter_entry_points(tag, identifier) :
                if self.is_implementation(ep, interfaces):
                    lst.append(ep)

        # Scan openalea entry_points : 1 entry_point = n factories (scan)
        for tag in self.plugin_types:
            if tag in tags :
                lst += self._getplugin(tag, interfaces, identifier, tags)

        return lst

    def get_factory(self, interfaces=None, identifier=None, tags=None, exclude_tags=None):
        lst = self.get_factories(interfaces, identifier, tags, exclude_tags)
        if lst :
            return lst[0]

    def service(self, object_factory):
        return self._services[object_factory] if object_factory in self._services else None

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


    def get_service(self, interfaces=None, identifier=None, tags=None, exclude_tags=None, args=None, kargs=None):
        if args is None :
            args = []
        if kargs is None :
            kargs = {}
        if exclude_tags is None :
            exclude_tags = ['wralea']
        object_factory = self.get_factory(interfaces, identifier, tags, exclude_tags)
        return self.create_service(object_factory)

    def get_services(self, interfaces=None, identifier=None, tags=None, exclude_tags=None, args=None, kargs=None):
        if args is None :
            args = []
        if kargs is None :
            kargs = {}
        if exclude_tags is None :
            exclude_tags = ['wralea']
        object_factories = self.get_factories(interfaces, identifier, tags, exclude_tags)
        services = []
        for object_factory in object_factories :
            services.append(self.create_service(object_factory, *args, **kargs))
        return services


def color_interface_line(interface_id):
        catalog = Catalog()
        interface = catalog.get_interface_class(interface_id)
        hierarchy = [cl.__name__ for cl in reversed(inspect.getmro(interface)) if cl in catalog._interfaces.values()]
        hierarchy = ' > '.join(hierarchy)
        return '\033[93m%s\033[91m   (%s)\033[0m' % (interface_id, hierarchy)

def list_interfaces():
    catalog = Catalog()

    print '=========='
    print 'Interfaces'
    print '=========='

    for interface_id in sorted(catalog.get_interfaces()):
        interface = catalog.get_interface_class(interface_id)
        print color_interface_line(interface_id)
        print '       defined in:', interface.__module__
        print
    print

def list_implementations():
    catalog = Catalog()

    print '==============='
    print 'Implementations'
    print '==============='

    for interface_id in catalog.get_interfaces():
        print color_interface_line(interface_id)
        for factory in catalog.get_factories(interfaces=interface_id):
            print '  *', factory.name
        print

