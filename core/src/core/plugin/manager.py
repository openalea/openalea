"""
This plugin manager is derivated from nose PluginManager(s) released under LGPL license.
You can get a full copy of this license at https://github.com/nose-devs/nose/blob/master/lgpl.txt
You can get original nose code at https://github.com/nose-devs/nose/blob/master/nose/plugins/manager.py


Plugin Manager
--------------

A plugin manager class is used to load plugins, manage the list of
loaded plugins, and proxy calls to those plugins.

The plugin managers provided with nose are:

:class:`PluginManager`
    This manager uses setuptools entrypoints to load plugins.

Writing a plugin manager
========================

If you want to load plugins via some other means, you can write a
plugin manager and pass an instance of your plugin manager class when
instantiating the :class:`nose.config.Config` instance that you pass to
:class:`TestProgram` (or :func:`main` or :func:`run`).

To implement your plugin loading scheme, implement ``loadPlugins()``,
and in that method, call ``add_plugin()`` with an instance of each plugin
you wish to make available. Make sure to call
``super(self).loadPlugins()`` as well if have subclassed a manager
other than ``PluginManager``.

"""
import logging
import weakref
from warnings import warn
from openalea.core.singleton import Singleton

__all__ = ['PluginManager']

log = logging.getLogger(__name__)


class PluginManager(object):

    """
    """
    __metaclass__ = Singleton

    def __init__(self, plugins=None, proxy_class=None):
        self._plugin = {}  # dict category -> plugin name -> Plugin class or Plugin proxy
        self._plugin_instance = {}
        self._plugin_proxy = {}
        self._plugin_loaded = {}
        self._plugin_all_instances = {}

        self._debug = []

        self._extraplugins = {}
        self._proxies = {}

        self.proxy_class = proxy_class

        if plugins is not None:
            self.add_plugins(plugins)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if value in (True, 'all', ['all']):
            self._debug = [True]
        elif value is False:
            self._debug = []
        else:
            self._debug = value

    def _debug_mode(self, category):
        return category in self.debug or True in self.debug

    def __call__(self, category, func=None, **kwds):
        func_args = kwds.pop('func_args', [])
        func_kwds = kwds.pop('func_kwds', {})
        callback = kwds.pop('callback', None)
        if self._debug_mode(category):
            return func(*func_args, **func_kwds)
        else:
            try:
                return func(*func_args, **func_kwds)
            except:
                if callback:
                    callback()

    def set_proxy(self, category, proxy_class):
        """
        Embed all plugin in category in proxy_class
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
        # plugins[:] = [p for p in plugins if getattr(p, 'name', None) != new_name]
        # plugins.append(plugin)

    def add_plugins(self, plugins=None, extraplugins=None):
        if plugins is None:
            plugins = {}
        if extraplugins is None:
            extraplugins = {}
        self._extraplugins = extraplugins

        for category, plugin in plugins.iteritems():
            self.add_plugin(category, plugin)

        for category, plugin in extraplugins.iteritems():
            self.add_plugin(category, plugin)

    def _load_entry_point_plugin(self, category, entry_point, proxy_class=None):
        ep = entry_point
        identifier = '%s:%s:%s' % (category, ep.module_name, ep.name)
        plugin_class = None
        if identifier in self._plugin_loaded:
            plugin_class = self._plugin_loaded[identifier]
        else:
            log.debug('%s load plugin %s', self.__class__.__name__, ep)
            try:
                plugin_class = ep.load()
            except KeyboardInterrupt:
                pass
            except Exception, e:
                # never want a plugin load to kill the test run
                # but we can't log here because the logger is not yet
                # configured
                warn("Unable to load plugin %s: %s" % (ep, e),
                     RuntimeWarning)
            else:
                self._plugin_loaded[identifier] = plugin_class
                self.add_plugin(category, plugin_class, proxy_class=proxy_class)

        return plugin_class

    def _load_plugins(self, category, proxy_class=None):
        from pkg_resources import iter_entry_points
        for ep in iter_entry_points(category):
            self._load_entry_point_plugin(category, ep, proxy_class=proxy_class)

        if category in self._extraplugins:
            for plugin in self._extraplugins[category]:
                self.add_plugin(category, plugin, proxy_class=proxy_class)

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

    def register(self, category, name, instance):
        """
        Add a weakref to instance in dict
        category -> name -> [list of instances]
        """
        self._plugin_all_instances.setdefault(category, {}).setdefault(name, []).append(weakref.ref(instance))

    def unregister(self, category, name, instance):
        """
        Unregistered instances won't be list by "instances" method
        """
        try:
            self._plugin_all_instances[category][name].remove(instance)
        except KeyError:
            # No instances have been registered for this plugin or this category
            pass
        except ValueError:
            # Passed instance is not registered for this plugin
            pass

    def _new(self, category, name, class_args=None, class_kwds=None):
        if category not in self._plugin:
            self._load_plugins(category)
        try:
            plugin_class = self._plugin[category][name]
        except KeyError:
            pass
        else:
            plugin = plugin_class()
            if class_args is None:
                class_args = []
            if class_kwds is None:
                class_kwds = {}
            klass = plugin()
            instance = klass(*class_args, **class_kwds)
            self.register(category, name, instance)
            return instance

    def new(self, category, name, class_args=None, class_kwds=None):
        """
        Create a new instance and register it.
        You can get all created instances with instances method.
        """
        if self._debug_mode(category):
            return self._new(category, name, class_args, class_kwds)
        else:
            try:
                return self._new(category, name, class_args, class_kwds)
            except:
                return None

    def instance(self, category, name, class_args=None, class_kwds=None):
        """
        Use this function if you always want the same instance:
        If plugin has never been called, create a new instance else return first created one.
        """
        if name in self._plugin_instance.get(category, {}):
            obj = self._plugin_instance[category][name]()
            if obj:
                return obj  # return actual value instead of weakref
            else:
                # Object is no more reachable, remove it and generate new one
                del self._plugin_instance[category][name]
                return self.instance(category, name, class_args, class_kwds)
        else:
            instance = self.new(category, name, class_args, class_kwds)
            if instance is None:
                return
            self._plugin_instance.setdefault(category, {})[name] = weakref.ref(instance)
            return instance

    def instances(self, category, name=None, class_args=None, class_kwds=None):
        """
        Return all existing instances corresponding to this plugin
        """
        valid_instances = []
        if name is None:
            for plugin_name in self._plugin_all_instances[category]:
                instances = list(self._plugin_all_instances[category][plugin_name])
                for weakref in instances:
                    obj = weakref()
                    if obj is None:
                        self._plugin_all_instances[category][plugin_name].remove(weakref)
                    else:
                        valid_instances.append(obj)
        else:
            try:
                # return actual value instead of weakref
                valid_instances = []
                for weakref in self._plugin_all_instances[category][name]:
                    obj = weakref()
                    if obj is None:
                        self._plugin_all_instances[category][name].remove(weakref)
                    else:
                        valid_instances.append(obj)
            except KeyError:
                pass
        return valid_instances

    def implementations(self, interface, **kwds):
        """
        Return all instances implementing this interface
        """
        raise NotImplementedError


class Proxy(object):

    """
    Plugin approach used in OpenAlea is :
    entry_point --(load)--> plugin_class --(instantiate)--> plugin --call--> RealClass

    If you want to use third party plugins that follow approach:
    entry_point --(load)--> RealClass

    You can use this class as a proxy.
    RealClass is now embeded in a Proxy and can be reached with "klass" attribute.
    Plugin is now compatible with pluginmanager.

    Then, you can define meta-information, generally generated from RealClass attributes.
    By default, plugin name is "RealClass" name

    class ThirdPartyProxy(Proxy):
        alias = property(fget=lambda self: self.klass.title)

    .. warning::

        You should not use this Proxy because the plugin may slow down the entire application:
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
    pm.set_proxy('oalab.model', Proxy)

    w1 = pm.instance('oalab.model', 'PythonModel')
    w2 = pm.instance('oalab.model', 'PythonModel')
    w3 = pm.instance('oalab.model', 'PythonModel')
    w4 = pm.new('oalab.model', 'PythonModel')
    assert w1 is w2 is w3
    assert w1 is not w4

    assert len(pm.instances('oalab.model', 'PythonModel')) == 2
