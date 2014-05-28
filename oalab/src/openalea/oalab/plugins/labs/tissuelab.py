
from openalea.vpltk.plugin import iter_plugins
from openalea.oalab.plugins.minilab import MiniLab


class TissueLab(MiniLab):
    name = 'tissue'
    applets = [
               'ControlPanel',
               'EditorManager',
               'HelpWidget',
               'Viewer3D',
               ]

    def __call__(self, mainwin):
        for plugin in iter_plugins('oalab.applet'):
            if plugin.name in self.applets:
                mainwin.add_plugin(plugin())
