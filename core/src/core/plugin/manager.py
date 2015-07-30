"""
This plugin manager is inspired by nose PluginManager(s) released under LGPL license.
You can get a full copy of this license on nosetest repository:`lgpl.txt <https://github.com/nose-devs/nose/blob/master/lgpl.txt>`_
You can get original nose code on `github <https://github.com/nose-devs/nose/blob/master/nose/plugins/manager.py>`_


Plugin Manager
--------------

A plugin manager class is used to load plugins, search among it and manage the list of loaded plugins.
Plugins are loaded from entry points or can be added dynamically to manager.
  - To *list* plugins, see :meth:`PluginManager.plugin` and :meth:`PluginManager.plugins`.
  - To *add* plugins dynamically, see :meth:`PluginManager.add_plugin` and :meth:`PluginManager.add_plugins`.

All plugin are sorted in categories, each group defining a contract.
This contract is generally described in an interface class or documentation.

If you want to use third party plugins that doesn't fit perfectly to your contract,
you can embed its in plugin proxies.
To do that, you can specify a proxy class for an entire group or for one plugin.
See :meth:`PluginManager.set_proxy` and "plugin_proxy" parameter in :meth:`PluginManager.add_plugin`.

"""

import inspect

from warnings import warn
from openalea.core.singleton import Singleton
from openalea.core import logger
from openalea.core.service.introspection import name
from openalea.core.util import camel_case_to_lower

from openalea.core.plugin.plugin import PluginDef

__all__ = ['PluginManager']


class UnknownPluginError(Exception):
    pass


def get_implementation(plugin):
    if hasattr(plugin, 'modulename') and hasattr(plugin, 'objectname'):
        modulename = plugin.modulename
        objectname = plugin.objectname

        module = __import__(modulename, fromlist=[objectname])
        return getattr(module, objectname)
    else:
        return plugin()


def plugin_name(plugin):
    return plugin.name if hasattr(plugin, 'name') else plugin.__class__.__name__


def drop_plugin(name):
    try:
        idx = name.lower().index('plugin')
    except ValueError:
        pass
    else:
        name = name[0:idx] + name[idx + 6:]
    return name


def generate_plugin_name(plugin):
    try:
        name = plugin.name
    except AttributeError:
        try:
            name = plugin.__class__.__name__
        except AttributeError:
            name = str(plugin.__class__)

        if hasattr(plugin, 'name_conversion'):
            if plugin.name_conversion == PluginDef.UNCHANGED:
                return name
            elif plugin.name_conversion == PluginDef.DROP_PLUGIN:
                return drop_plugin(name)

        return camel_case_to_lower(drop_plugin(name))
    return name


def generate_plugin_id(plugin):
    return ':'.join([plugin.__class__.__module__, plugin.__class__.__name__])


class PluginManager(object):

    __metaclass__ = Singleton

    def __init__(self, plugins=None, plugin_proxy=None):
        """
        :param plugins: list of plugins you want to add manually
        :param plugin_proxy: proxy class to use by default
        """
        self._plugin = {}  # dict group -> plugin name -> Plugin class or Plugin proxy
        self._plugin_proxy = {}

        self.debug = False
        self._proxies = {}

        self.plugin_proxy = plugin_proxy

        if plugins is not None:
            self.add_plugins(plugins)

    def clear(self):
        self._plugin = {}  # dict group -> plugin name -> Plugin class or Plugin proxy
        self._plugin_loaded = {}
        self._proxies = {}

    def set_proxy(self, group, plugin_proxy):
        """
        Embed all plugin for given group in plugin_proxy.
        """
        self._plugin_proxy[group] = plugin_proxy

    def patch_ep_plugin(self, plugin, ep):
        pass

    def patch_plugin(self, plugin):
        if not hasattr(plugin, "identifier"):
            plugin.identifier = generate_plugin_id(plugin)
        if not hasattr(plugin, "name"):
            plugin.name = generate_plugin_name(plugin)
        if not hasattr(plugin, "label"):
            plugin.label = plugin.name.replace('_', ' ').capitalize()
        if not hasattr(plugin, "tags"):
            plugin.tags = []
        if not hasattr(plugin, "implementation"):
            plugin.__class__.implementation = property(fget=get_implementation)
        if not hasattr(plugin, "name_conversion"):
            plugin.name_conversion = 2

    def add_plugin(self, group, plugin, plugin_proxy=None, **kwds):
        """
        """
        if inspect.isclass(plugin):
            plugin = plugin()
        else:
            raise NotImplementedError

        if plugin_proxy is None and group in self._plugin_proxy:
            plugin_proxy = self._plugin_proxy[group]

        if plugin_proxy:
            plugin = plugin_proxy(plugin)

        self.patch_plugin(plugin)
        self._plugin.setdefault(group, {})[plugin.identifier] = plugin
        return plugin

    def add_plugins(self, plugins=None):
        if plugins is None:
            plugins = {}

        for group, plugin in plugins.iteritems():
            self.add_plugin(group, plugin)

    def _is_plugin_class(self, obj):
        if hasattr(obj, '__plugin__'):
            return True
        elif hasattr(obj, 'modulename') and hasattr(obj, 'objectname'):
            return True
        else:
            return False

    def _add_plugin_from_ep(self, group, ep, plugin_class, plugin_proxy=None):
        logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
        if inspect.ismodule(plugin_class):
            plugin_classes = []
            for pl_name in dir(plugin_class):
                pl = getattr(plugin_class, pl_name)
                if self._is_plugin_class(pl):
                    plugin_classes.append(pl)
        elif isinstance(plugin_class, list):
            plugin_classes = plugin_class
        else:
            plugin_classes = [plugin_class]

        for plugin_class in plugin_classes:
            name = plugin_class.name if hasattr(plugin_class, 'name') else plugin_class.__name__
            parts = [str(s) for s in (ep.dist.egg_name(), group, ep.module_name, ep.name, name)]
            identifier = ':'.join(parts)
            self.add_plugin(group, plugin_class, plugin_proxy=plugin_proxy, identifier=identifier)

    def _load_entry_point_plugin(self, group, entry_point, plugin_proxy=None):
        ep = entry_point
        plugin_class = None
        if self.debug:
            plugin_class = ep.load()
            logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
            self._add_plugin_from_ep(group, ep, plugin_class, plugin_proxy)
        else:
            try:
                plugin_class = ep.load()
            except KeyboardInterrupt:
                logger.error('%s: error loading %s ' % (group, ep))
            except Exception, e:
                # never want a plugin load to kill the test run
                # but we can't log here because the logger is not yet
                # configured
                warn("Unable to load plugin %s: %s" % (ep, e),
                     RuntimeWarning)
            else:
                self._add_plugin_from_ep(group, ep, plugin_class, plugin_proxy)

    def _load_plugins(self, group, plugin_proxy=None):
        from pkg_resources import iter_entry_points
        for ep in iter_entry_points(group):
            self._load_entry_point_plugin(group, ep, plugin_proxy=plugin_proxy)

    def discover(self, group):
        self._load_plugins(group)

    def plugin(self, group, identifier):
        """
        plugin(self, group, identifier)
        -> Plugin or raises UnknownPluginError

        plugin(self, group, name)
        -> return first plugin matching name, if not found, raises UnknownPluginError
        """
        plugins = self.plugins(group)
        if identifier in self._plugin[group]:
            return self._plugin[group][identifier]
        else:
            for pl in plugins:
                if pl.name == identifier:
                    return pl
            raise UnknownPluginError

    def _sorted_plugins(self, plugins):
        plugin_dict = {}
        for plugin in plugins:
            if hasattr(plugin, 'name'):
                plugin_dict[plugin.name] = plugin
            else:
                plugin_dict[plugin_name(plugin)] = plugin
        sorted_plugins = [plugin_dict[name] for name in sorted(plugin_dict.keys())]
        return sorted_plugins

    def plugins(self, group, tags=None, criteria=None, **kwds):
        """
        plugins(self, group, tags=None, criteria=None, **kwds)
        Return a list of all plugins available for this group and matching tags and criteria.

        optional parameters:
            pass
        """
        try:
            plugins = self._plugin[group].values()
        except KeyError:
            self._plugin.setdefault(group, {})
            self._load_plugins(group)
            plugins = self._plugin[group].values()

        if criteria is None:
            criteria = {}

        valid_plugins = []
        for pl in plugins:
            # Check tags. If one tag dont match, ignore this plugin
            if tags is not None and all(tag in pl.tags for tag in tags) is False:
                continue

            # Check all criteria. If one criteria dont match, ignore plugin
            if not all(hasattr(pl, criterion) and getattr(pl, criterion) == criteria[criterion] for criterion in criteria):
                continue

            valid_plugins.append(pl)
        return valid_plugins


class SimpleClassPluginProxy(object):

    """
    Plugin approach used in OpenAlea is :
    entry_point --(load)--> plugin_class --(instantiate)--> plugin --call--> RealClass

    If you want to use third party plugins that follow approach:
    entry_point --(load)--> RealClass

    You can use this class as a proxy.
    RealClass is now embeded in a SimpleClassPluginProxy and can be reached with "klass" attribute.
    Plugin is now compatible with pluginmanager.

    Then, you can define meta-information, generally generated from RealClass attributes.
    By default, plugin name is "RealClass" name

    class ThirdPartyProxy(SimpleClassPluginProxy):
        label = property(fget=lambda self: self.klass.title)

    .. warning::

        You should not use this proxy because the plugin may slow down the entire application:
        all code and imports defined in module containing "RealClass" are loaded at first query or listing instead of only when used
    """
    __plugin__ = True

    def __init__(self, klass):
        self.klass = klass
        self.name = klass.name if hasattr(klass, "name") else klass.__class__.__name__

    def __call__(self):
        return self

    def implementation(self):
        return self.klass
