
from openalea.core.plugin.instance import PluginInstanceManager
from openalea.core.plugin.manager import PluginManager


PM = PluginManager()
PIM = PluginInstanceManager(PM)


plugin = PM.plugin
plugins = PM.plugins


register_plugin = PM.add_plugin

clear_plugin_instances = PIM.clear
debug_plugin = PIM.__call__
new_plugin_instance = PIM.new
plugin_instance = PIM.instance
plugin_function = PIM.function
plugin_instances = PIM.instances
plugin_instance_exists = PIM.has_instance
set_plugin_instance_manager = PIM.set_manager
