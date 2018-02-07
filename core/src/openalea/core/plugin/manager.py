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

from openalea.core import logger
from openalea.core.manager import GenericManager
from openalea.core.plugin.plugin import PluginDef
from openalea.core.service.introspection import name
from openalea.core.util import camel_case_to_lower

from pkg_resources import iter_entry_points

__all__ = ['PluginManager']


class UnknownItemError(Exception):
    pass


def get_criteria(plugin):
    criteria = {}
    for criterion in dir(plugin):
        if criterion.startswith('_'):
            continue
        elif criterion in ('implementation', 'name_conversion', 'identifier', 'tags', 'criteria'):
            continue
        criteria[criterion] = getattr(plugin, criterion)
    return criteria


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


class PluginManager(GenericManager):

    @classmethod
    def generate_item_name(cls, item):
        try:
            name = item.name
        except AttributeError:
            try:
                name = item.__class__.__name__
            except AttributeError:
                name = str(item.__class__)

        if hasattr(item, 'name_conversion'):
            if item.name_conversion == PluginDef.UNCHANGED:
                return name
            elif item.name_conversion == PluginDef.DROP_PLUGIN:
                return drop_plugin(name)
            else:
                return camel_case_to_lower(drop_plugin(name))
        else:
            return name

    def generate_item_id(self, plugin):
        return ':'.join([plugin.__class__.__module__, plugin.__class__.__name__])

    def discover(self, group=None, item_proxy=None):
        if "entry_points" in self._autoload:
            for ep in iter_entry_points(group):
                self._load_entry_point_plugin(group, ep, item_proxy=item_proxy)

    def instantiate(self, item):
        if inspect.isclass(item):
            return item()
        else:
            raise NotImplementedError

    def patch_item(self, item):
        if not hasattr(item, "name_conversion"):
            item.name_conversion = 2
        if not hasattr(item, "criteria"):
            item.__class__.criteria = property(fget=get_criteria)

        GenericManager.patch_item(self, item)

        # Look in class dict instead of hasattr(item, 'implementation') to avoid loading implementation
        if not hasattr(item.__class__, 'implementation'):
            item.__class__.implementation = property(fget=get_implementation)

    def patch_ep_plugin(self, plugin, ep):
        plugin.plugin_ep = ep.name
        plugin.plugin_modulename = ep.module_name
        plugin.plugin_dist = ep.dist

    def _is_plugin_class(self, obj):
        if hasattr(obj, '__plugin__'):
            return True
        elif hasattr(obj, 'modulename') and hasattr(obj, 'objectname'):
            return True
        else:
            return False

    def _add_plugin_from_ep(self, group, ep, plugin_class, plugin_proxy=None):
        logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
        from time import time
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
            item = self.add(plugin_class, group, item_proxy=plugin_proxy, identifier=identifier)
            self.patch_ep_plugin(item, ep)

    def _load_entry_point_plugin(self, group, entry_point, item_proxy=None):
        ep = entry_point
        plugin_class = None
        if self.debug:
            plugin_class = ep.load()
            logger.debug('%s load plugin %s' % (self.__class__.__name__, ep))
            self._add_plugin_from_ep(group, ep, plugin_class, item_proxy)
        else:
            try:
                plugin_class = ep.load()
            except Exception:
                logger.error('%s: error loading %s ' % (group, ep))
            else:
                self._add_plugin_from_ep(group, ep, plugin_class, item_proxy)


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
