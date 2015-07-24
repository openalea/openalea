

import weakref
from openalea.core.singleton import Singleton
from openalea.core.plugin.manager import PluginManager, get_implementation
from openalea.core.plugin.plugin import plugin_name, plugin_implement, plugin_implementation
from openalea.core import logger


def enhanced_error(error, **kwds):
    """
    Add plugin information to given exception.
    By default, if a plugin fails, for example because a dependency cannot be imported,
    user get error message "ImportError: No module named mydep". This message is useless because we don't know
    which plugin has failed. 

    Once enhanced, error message become:
    "MyLab (mypackage.lab.mylab): ImportError: No module named mydep"

    kwds:

        - plugin: plugin instance
        - plugin_class: plugin class

    """
    plugin = kwds.pop('plugin', None)
    plugin_class = kwds.pop('plugin_class', None)
    if plugin:
        plugin_class = kwds.pop('plugin_class', plugin.__class__)
        path = '%s.%s' % (plugin_class.__module__, plugin_class.__name__)
        message = '%s (%s): %s' % (plugin.name, path, error.message)
        return error.__class__(message)
    elif plugin_class:
        path = '%s.%s' % (plugin_class.__module__, plugin_class.__name__)
        message = '%s: %s' % (path, error.message)
        return error.__class__(message)
    else:
        return error


class PluginInstanceManager(object):
    __metaclass__ = Singleton

    def __init__(self, plugins=None, proxy_class=None):
        self._plugin_instances = {}
        self._debug = []
        self.pm = PluginManager()

    def clear(self):
        self._plugin_instances = {}

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
        return category in self.debug or True in self.debug or 'all' in self.debug

    def __call__(self, category, func=None, **kwds):
        """
        Use this method to launch a function in debug mode.
        If debug is enabled for this category, errors are raised,
        else debug is disable, errors pass silently.
        """
        func_args = kwds.pop('func_args', [])
        func_kwds = kwds.pop('func_kwds', {})
        callback = kwds.pop('callback', None)
        if self._debug_mode(category):
            return func(*func_args, **func_kwds)
        else:
            try:
                return func(*func_args, **func_kwds)
            except:
                logger.error('%s: error calling %s ' % (category, func))
                if callback:
                    callback()

    def register(self, category, name, instance):
        """
        Add a weakref to instance in dict
        category -> name -> [list of instances]
        """
        self._plugin_instances.setdefault(category, {}).setdefault(name, []).append(weakref.ref(instance))

    def unregister(self, category, name, instance):
        """
        Unregistered instances won't be list by "instances" method
        """
        try:
            self._plugin_instances[category][name].remove(instance)
        except KeyError:
            # No instances have been registered for this plugin or this category
            pass
        except ValueError:
            # Passed instance is not registered for this plugin
            pass

    def _function(self, category, name):
        if category not in self.pm._plugin:
            self.pm._load_plugins(category)
        try:
            plugin_class = self.pm._plugin[category][name]
        except KeyError:
            pass
        else:
            try:
                plugin = plugin_class()
            except TypeError, e:
                raise enhanced_error(e, plugin_class=plugin_class)

            try:
                function = get_implementation(plugin)
            except TypeError, e:
                raise enhanced_error(e, plugin=plugin, plugin_class=plugin_class)

            return function

    def _new(self, category, name, class_args=None, class_kwds=None):
        if category not in self.pm._plugin:
            self.pm._load_plugins(category)
        try:
            plugin_class = self.pm._plugin[category][name]
        except KeyError:
            pass
        else:
            try:
                plugin = plugin_class()
            except TypeError, e:
                raise enhanced_error(e, plugin_class=plugin_class)

            if class_args is None:
                class_args = []
            if class_kwds is None:
                class_kwds = {}

            try:
                klass = get_implementation(plugin)
            except TypeError, e:
                raise enhanced_error(e, plugin=plugin, plugin_class=plugin_class)
            try:
                instance = klass(*class_args, **class_kwds)
            except TypeError, e:
                raise enhanced_error(e, plugin_class=klass)
            self.register(category, name, instance)
            return instance

    def function(self, category, name):
        if self._debug_mode(category):
            return self._function(category, name)
        else:
            try:
                return self._function(category, name)
            except:
                return None

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

    def has_instance(self, category, name):
        return name in self._plugin_instances.get(category, {})

    def instance(self, category, name, class_args=None, class_kwds=None):
        """
        Use this function if you always want the same instance:
        If plugin has never been called, create a new instance else return first created one.
        """
        if name in self._plugin_instances.get(category, {}):
            instances = self._plugin_instances[category][name]
            if instances:
                obj = instances[0]()
            else:
                obj = None
            if obj:
                return obj  # return actual value instead of weakref
            else:
                # Object is no more reachable, remove it and generate new one
                del self._plugin_instances[category][name]
                return self.instance(category, name, class_args, class_kwds)
        else:
            instance = self.new(category, name, class_args, class_kwds)
            if instance is None:
                return
            self._plugin_instances.setdefault(category, {})[name] = [weakref.ref(instance)]
            return instance

    def instances(self, category, name=None, class_args=None, class_kwds=None):
        """
        Return all existing instances corresponding to this plugin
        """
        valid_instances = []
        if name is None:
            for plugin_name in self._plugin_instances.get(category, []):
                instances = list(self._plugin_instances[category][plugin_name])
                for weakref in instances:
                    obj = weakref()
                    if obj is None:
                        self._plugin_instances[category][plugin_name].remove(weakref)
                    else:
                        valid_instances.append(obj)
        else:
            try:
                # return actual value instead of weakref
                valid_instances = []
                for weakref in self._plugin_instances[category][name]:
                    obj = weakref()
                    if obj is None:
                        self._plugin_instances[category][name].remove(weakref)
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

PM = PluginManager()
PIM = PluginInstanceManager()


plugins = PM.plugins
# plugins

plugin_class = PM.plugin
register_plugin = PM.add_plugin

clear_plugin_instances = PIM.clear
debug_plugin = PIM.__call__
new_plugin_instance = PIM.new
plugin_instance = PIM.instance
plugin_function = PIM.function
plugin_instances = PIM.instances
plugin_instance_exists = PIM.has_instance
