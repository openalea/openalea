
from openalea.oalab.plugins.labs.minilab import MiniLab


class FullLab(MiniLab):
    name = 'full'

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__

        from openalea.core.plugin.manager import PluginManager
        pm = PluginManager()
        # Load, create and place applets in mainwindow
        for plugin_class in pm.plugins('oalab.applet'):
            mainwin.add_plugin(name=plugin_class.name)
        # Initialize all applets
        mainwin.initialize()

    @classmethod
    def start(cls, *args, **kwds):
        pass

    @classmethod
    def initialize(cls, *args, **kwds):
        from openalea.core.project.manager import ProjectManager
        pm = ProjectManager()

    @classmethod
    def finalize(cls, *args, **kwds):
        pass

    @classmethod
    def stop(cls, *args, **kwds):
        pass
