

class FullLab(object):
    name = 'full'

    def __call__(self, mainwin):
        from openalea.core.plugin.manager import PluginManager
        pm = PluginManager()
        # Load, create and place applets in mainwindow
        for plugin_class in pm.plugins('oalab.applet'):
            mainwin.add_plugin(plugin=plugin_class())
        # Initialize all applets
        mainwin.initialize()
