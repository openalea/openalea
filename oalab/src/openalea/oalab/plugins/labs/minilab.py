from openalea.vpltk.plugin import iter_plugins


class MiniLab(object):

    name = 'mini'
    applets = ['HelpWidget', 'ControlPanel', 'Viewer3D', 'EditorManager']

    def __call__(self, mainwin):
        import sys
        for plugin in iter_plugins('oalab.applet'):
            if plugin.name in self.applets:
                mainwin.add_plugin(plugin())
