from wralea import *

metainfo={ 'version' : '',
               'license' : '',
               'authors' : '',
               'institutes' : 'INRIA',
               'description' : '',
               'url' : ''
                }

dtk_obj = dtk_Builder(PluginsPath)
dtk_obj.get_plugins()

for plugin in dtk_obj.plugins:
    package = dtk_obj.add_package(plugin, metainfo)
    #dtk_obj.add_factory(plugin, package)
    if package:
        pkgmanager.add_package(package)


