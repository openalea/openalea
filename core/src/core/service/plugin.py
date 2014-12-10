
__all__ = ['PluginManager']

import weakref
from openalea.core.singleton import Singleton
from openalea.core.plugin.manager import PluginManager
from openalea.core import logger


class PluginInstanceManager(object):
    __metaclass__ = Singleton

    def __init__(self, plugins=None, proxy_class=None):
        self._plugin_instance = {}
        self._plugin_all_instances = {}
        self._debug = []
        self.pm = PluginManager()

    def clear(self):
        self._plugin_instance = {}
        self._plugin_all_instances = {}

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
        if category not in self.pm._plugin:
            self.pm._load_plugins(category)
        try:
            plugin_class = self.pm._plugin[category][name]
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

PIM = PluginInstanceManager()


clear_plugin_instances = PIM.clear
new_plugin_instance = PIM.new
plugin_implementations = PIM.implementations
plugin_instance = PIM.instance
plugin_instances = PIM.instances
