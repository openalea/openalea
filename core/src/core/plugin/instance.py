import logging

import weakref

from openalea.core import logger
from openalea.core.plugin.plugin import plugin_name


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
    plugin_class = kwds.pop('plugin_class', plugin)
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

    def __init__(self, manager, plugins=None, proxy_class=None):
        self._plugin_instances = {}
        self._debug = []
        self.set_manager(manager)

    def set_manager(self, manager):
        self.pm = manager

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

    def _debug_mode(self, group):
        return group in self.debug or True in self.debug or 'all' in self.debug

    def __call__(self, group, func=None, **kwds):
        """
        Use this method to launch a function in debug mode.
        If debug is enabled for this group, errors are raised,
        else debug is disable, errors pass silently.
        """
        func_args = kwds.pop('func_args', [])
        func_kwds = kwds.pop('func_kwds', {})
        callback = kwds.pop('callback', None)
        if self._debug_mode(group):
            return func(*func_args, **func_kwds)
        else:
            try:
                return func(*func_args, **func_kwds)
            except:
                logger.error('%s: error calling %s ' % (group, func))
                if callback:
                    callback()

    def register(self, group, name, instance):
        """
        Add a weakref to instance in dict
        group -> name -> [list of instances]
        """
        self._plugin_instances.setdefault(group, {}).setdefault(name, []).append(weakref.ref(instance))

    def unregister(self, group, name, instance):
        """
        Unregistered instances won't be list by "instances" method
        """
        try:
            self._plugin_instances[group][name].remove(instance)
        except KeyError:
            # No instances have been registered for this plugin or this group
            pass
        except ValueError:
            # Passed instance is not registered for this plugin
            pass

    def _function(self, group, name):
        plugin = self.pm.item(name, group)
        try:
            function = plugin.implementation
        except TypeError as e:
            raise enhanced_error(e, plugin=plugin, plugin_class=plugin.__class__)

        return function

    def _new(self, group, name, class_args=None, class_kwds=None):
        plugin = self.pm.item(name, group)

        logger = logging.getLogger("core::plugin::PluginInstanceManager::_new")
        logger.warning(plugin)

        if class_args is None:
            class_args = []
        if class_kwds is None:
            class_kwds = {}

        try:
            klass = plugin.implementation
        except TypeError as e:
            raise enhanced_error(e, plugin=plugin, plugin_class=plugin.__class__)

        logger.warning(klass)
        instance = klass(*class_args, **class_kwds)
        logger.warning("toto")
        try:
            instance = klass(*class_args, **class_kwds)
        except TypeError as e:
            raise enhanced_error(e, plugin=plugin, plugin_class=klass)
        self.register(group, name, instance)
        return instance

    def function(self, group, name):
        if self._debug_mode(group):
            return self._function(group, name)
        else:
            try:
                return self._function(group, name)
            except:
                return None

    def new(self, group, name, class_args=None, class_kwds=None):
        """
        Create a new instance and register it.
        You can get all created instances with instances method.
        """
        return self._new(group, name, class_args, class_kwds)
        if self._debug_mode(group):
            return self._new(group, name, class_args, class_kwds)
        else:
            try:
                return self._new(group, name, class_args, class_kwds)
            except:
                return None

    def has_instance(self, group, name):
        return name in self._plugin_instances.get(group, {})

    def instance(self, group, name, class_args=None, class_kwds=None):
        """
        Use this function if you always want the same instance:
        If plugin has never been called, create a new instance else return first created one.
        """


        logger = logging.getLogger("core::plugin::PluginInstanceManager::instance")
        logger.warning(group)
        logger.warning(name)

        if name in self._plugin_instances.get(group, {}):
            instances = self._plugin_instances[group][name]

            logger.warning(instances)

            if instances:
                obj = instances[0]()
            else:
                obj = None
            if obj:
                return obj  # return actual value instead of weakref
            else:
                # Object is no more reachable, remove it and generate new one
                del self._plugin_instances[group][name]
                return self.instance(group, name, class_args, class_kwds)
        else:
            logger.warning("New plugin instance")
            instance = self.new(group, name, class_args, class_kwds)

            logger.warning(instance)

            if instance is None:
                return
            self._plugin_instances.setdefault(group, {})[name] = [weakref.ref(instance)]
            return instance

    def instances(self, group, name=None, class_args=None, class_kwds=None):
        """
        Return all existing instances corresponding to this plugin
        """
        valid_instances = []
        if name is None:
            for plugin_name in self._plugin_instances.get(group, []):
                instances = list(self._plugin_instances[group][plugin_name])
                for weakref in instances:
                    obj = weakref()
                    if obj is None:
                        self._plugin_instances[group][plugin_name].remove(weakref)
                    else:
                        valid_instances.append(obj)
        else:
            try:
                # return actual value instead of weakref
                valid_instances = []
                for weakref in self._plugin_instances[group][name]:
                    obj = weakref()
                    if obj is None:
                        self._plugin_instances[group][name].remove(weakref)
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
