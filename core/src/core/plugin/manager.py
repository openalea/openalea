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

All plugin are sorted in categories, each category defining a contract.
This contract is generally described in an interface class or documentation.

If you want to use third party plugins that doesn't fit perfectly to your contract,
you can embed its in plugin proxies.
To do that, you can specify a proxy class for an entire category or for one plugin.
See :meth:`PluginManager.set_proxy` and "plugin_proxy" parameter in :meth:`PluginManager.add_plugin`.

"""

import inspect

from warnings import warn
from openalea.core.singleton import Singleton
from openalea.core import logger
from openalea.core.service.introspection import name

__all__ = ['PluginManager']


def plugin_implements(plugin, interface):
    if hasattr(plugin, 'implements') and interface in plugin.implements:
        return True
    else:
        return False


def plugin_implementations(plugin):
    if hasattr(plugin, 'implements'):
        return plugin.implements
    else:
        return []


def plugin_name(plugin):
    return plugin.name if hasattr(plugin, 'name') else plugin.__name__


class PluginManager(object):

    __metaclass__ = Singleton

    def __init__(self, plugins=None, plugin_proxy=None):
        """
        :param plugins: list of plugins you want to add manually
        :param plugin_proxy: proxy class to use by default
        """
        self._plugin = {}  # dict category -> plugin name -> Plugin class or Plugin proxy
        self._plugin_proxy = {}

        self.debug = False
        self._proxies = {}

        self.plugin_proxy = plugin_proxy

        if plugins is not None:
            self.add_plugins(plugins)

    def clear(self):
        self._plugin = {}  # dict category -> plugin name -> Plugin class or Plugin proxy
        self._plugin_loaded = {}
        self._proxies = {}

    def set_proxy(self, category, plugin_proxy):
        """
        Embed all plugin for given category in plugin_proxy.
        """
        self._plugin_proxy[category] = plugin_proxy

    def add_plugin(self, category, plugin, plugin_proxy=None, **kwds):
        """
        optional parameters:
          - identifier: 
        """
        if plugin_proxy is None and category in self._plugin_proxy:
            plugin_proxy = self._plugin_proxy[category]

        if plugin_proxy:
            plugin = plugin_proxy(plugin)

        try:
            name = plugin.name
        except AttributeError:
            try:
                name = plugin.__name__
            except AttributeError:
                name = str(plugin)

        default_id = ':'.join([plugin.__module__, plugin.__name__])
        plugin.identifier = kwds.get('identifier', default_id)
        plugin.name = name

        self._plugin.setdefault(category, {})[name] = plugin

    def add_plugins(self, plugins=None):
        if plugins is None:
            plugins = {}

        for category, plugin in plugins.iteritems():
            self.add_plugin(category, plugin)

    def _is_plugin_meta(self, obj):
        if hasattr(obj, '__plugin__'):
            return True
        else:
            return False

    def _add_plugin_from_ep(self, category, ep, plugin_class, plugin_proxy=None):
        logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
        if inspect.ismodule(plugin_class):
            plugin_classes = []
            for pl_name in dir(plugin_class):
                pl = getattr(plugin_class, pl_name)
                if self._is_plugin_meta(pl):
                    plugin_classes.append(pl)
        elif isinstance(plugin_class, list):
            plugin_classes = plugin_class
        else:
            plugin_classes = [plugin_class]

        for plugin_class in plugin_classes:
            name = plugin_class.name if hasattr(plugin_class, 'name') else plugin_class.__name__
            parts = [str(s) for s in (ep.dist.egg_name(), category, ep.module_name, ep.name, name)]
            identifier = ':'.join(parts)
            self.add_plugin(category, plugin_class, plugin_proxy=plugin_proxy, identifier=identifier)

    def _load_entry_point_plugin(self, category, entry_point, plugin_proxy=None):
        ep = entry_point
        plugin_class = None
        if self.debug:
            plugin_class = ep.load()
            logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
            self._add_plugin_from_ep(category, ep, plugin_class, plugin_proxy)
        else:
            try:
                plugin_class = ep.load()
            except KeyboardInterrupt:
                logger.error('%s: error loading %s ' % (category, ep))
            except Exception, e:
                # never want a plugin load to kill the test run
                # but we can't log here because the logger is not yet
                # configured
                warn("Unable to load plugin %s: %s" % (ep, e),
                     RuntimeWarning)
            else:
                self._add_plugin_from_ep(category, ep, plugin_class, plugin_proxy)

    def _load_plugins(self, category, plugin_proxy=None):
        from pkg_resources import iter_entry_points
        for ep in iter_entry_points(category):
            self._load_entry_point_plugin(category, ep, plugin_proxy=plugin_proxy)

    def discover(self, category):
        self._load_plugins(category)

    def plugin(self, category, name=None, interface=None):
        """
        plugin(self, group, identifier)
        -> Plugin or raises UnknownPluginError
        """
        if name is None:
            return self.plugins(category, interface=interface)
        else:
            try:
                plugins = self._plugin[category]
            except KeyError:
                self._plugin.setdefault(category, {})
                self._load_plugins(category)
                plugins = self._plugin[category]

            if name in plugins:
                return self._plugin[category][name]
            else:
                return None

    def _sorted_plugins(self, plugins):
        plugin_dict = {}
        for plugin_class in plugins:
            if hasattr(plugin_class, 'name'):
                plugin_dict[plugin_class.name] = plugin_class
            else:
                plugin_dict[str(plugin_class)] = plugin_class
        sorted_plugins = [plugin_dict[name] for name in sorted(plugin_dict.keys())]
        return sorted_plugins

    def plugins(self, category, interface=None):
        """
        plugins(self, group, tags=None, criteria=None, **kwds)
        Return a list of all plugins available for this group and matching tags and criteria.

        optional parameters:
            pass
        """
        try:
            plugins = self._plugin[category].values()
        except KeyError:
            self._plugin.setdefault(category, {})
            self._load_plugins(category)
            plugins = self._plugin[category].values()

        if interface is None:
            return self._sorted_plugins(plugins)
        else:
            final_list = []
            for plugin in plugins:
                if plugin_implements(plugin, interface):
                    final_list.append(plugin)
            return self._sorted_plugins(final_list)


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
        alias = property(fget=lambda self: self.klass.title)

    .. warning::

        You should not use this proxy because the plugin may slow down the entire application:
        all code and imports defined in module containing "RealClass" are loaded at first query or listing instead of only when used
    """
    name = property(fget=lambda self: self.klass.__name__)
    alias = property(fget=lambda self: self.name.capitalize())

    def __init__(self, klass):
        self.klass = klass

    def __call__(self):
        class PluginInstance(self.__class__):

            def __call__(self):
                return self.klass

        return PluginInstance(self.klass)
