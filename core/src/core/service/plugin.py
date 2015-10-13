
from openalea.core.plugin.instance import PluginInstanceManager
from openalea.core.plugin.manager import PluginManager


PM = PluginManager()
PIM = PluginInstanceManager(PM)


def debug_plugins(debug='all'):
    PM.debug = debug
    PIM.debug = debug


def register_plugin(plugin, group=None):
    PM.discover(group)
    return PM.add(plugin, group)

plugin = PM.item
plugins = PM.items


clear_plugin_instances = PIM.clear
debug_plugin = PIM.__call__
new_plugin_instance = PIM.new
plugin_instance = PIM.instance
plugin_function = PIM.function
plugin_instances = PIM.instances
plugin_instance_exists = PIM.has_instance
set_plugin_instance_manager = PIM.set_manager


def default_plugin_manager():
    return PM
