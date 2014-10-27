"""
This plugin manager is inspired by nose PluginManager(s) released under LGPL license.
You can get a full copy of this license at https://github.com/nose-devs/nose/blob/master/lgpl.txt
You can get original nose code at https://github.com/nose-devs/nose/blob/master/nose/plugins/manager.py


Plugin Manager
--------------

A plugin manager class is used to load plugins, manage the list of
loaded plugins, and proxy calls to those plugins.

The plugin managers provided with nose are:

:class:`PluginManager`
    This manager uses setuptools entrypoints to load plugins.
"""

from warnings import warn
from openalea.core.singleton import Singleton
from openalea.core import logger

__all__ = ['PluginManager']


class PluginManager(object):

    __metaclass__ = Singleton

    def __init__(self, plugins=None, proxy_class=None):
        """
        :param plugins: list of plugins you want to add manually
        :param proxy_class: proxy class to use by default
        """
        self._plugin = {}  # dict category -> plugin name -> Plugin class or Plugin proxy
        self._plugin_proxy = {}
        self._plugin_loaded = {}

        self.debug = False
        self._proxies = {}

        self.proxy_class = proxy_class

        if plugins is not None:
            self.add_plugins(plugins)

    def clear(self):
        self._plugin = {}  # dict category -> plugin name -> Plugin class or Plugin proxy
        self._plugin_loaded = {}
        self._proxies = {}

    def set_proxy(self, category, proxy_class):
        """
        Embed all plugin for given category in proxy_class.
        """
        self._plugin_proxy[category] = proxy_class

    def add_plugin(self, category, plugin, proxy_class=None):
        if proxy_class is None and category in self._plugin_proxy:
            proxy_class = self._plugin_proxy[category]

        if proxy_class:
            plugin = proxy_class(plugin)

        try:
            name = plugin.name
        except AttributeError:
            name = plugin.__name__
        self._plugin.setdefault(category, {})[name] = plugin

    def add_plugins(self, plugins=None):
        if plugins is None:
            plugins = {}

        for category, plugin in plugins.iteritems():
            self.add_plugin(category, plugin)

    def _load_entry_point_plugin(self, category, entry_point, proxy_class=None):
        ep = entry_point
        identifier = '%s:%s:%s' % (category, ep.module_name, ep.name)
        plugin_class = None
        if identifier in self._plugin_loaded:
            plugin_class = self._plugin_loaded[identifier]
        else:
            if self.debug:
                plugin_class = ep.load()
                logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
                self._plugin_loaded[identifier] = plugin_class
                self.add_plugin(category, plugin_class, proxy_class=proxy_class)
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
                    logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
                    self._plugin_loaded[identifier] = plugin_class
                    self.add_plugin(category, plugin_class, proxy_class=proxy_class)

        return plugin_class

    def _load_plugins(self, category, proxy_class=None):
        from pkg_resources import iter_entry_points
        for ep in iter_entry_points(category):
            self._load_entry_point_plugin(category, ep, proxy_class=proxy_class)

    def plugin(self, category, name=None):
        """
        Return a list of all plugins available for this category.
        """
        if name is None:
            return self.plugins(category)
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

    def plugins(self, category):
        """
        Return a list of all plugins available for this category.
        """
        try:
            plugins = self._plugin[category].values()
        except KeyError:
            self._plugin.setdefault(category, {})
            self._load_plugins(category)
            return list(self._plugin[category].values())
        else:
            return list(plugins)


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


if __name__ == '__main__':

    # TODO: move to test
    pm = PluginManager()
    pm.set_proxy('oalab.model', SimpleClassPluginProxy)

    w1 = pm.instance('oalab.model', 'PythonModel')
    w2 = pm.instance('oalab.model', 'PythonModel')
    w3 = pm.instance('oalab.model', 'PythonModel')
    w4 = pm.new('oalab.model', 'PythonModel')
    assert w1 is w2 is w3
    assert w1 is not w4

    assert len(pm.instances('oalab.model', 'PythonModel')) == 2
