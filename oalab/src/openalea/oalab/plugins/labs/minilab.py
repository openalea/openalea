from openalea.vpltk.plugin import iter_plugins


class MiniLab(object):

    name = 'mini'
    applets = ['ControlPanel', 'EditorManager', 'ProjectManager']
    applets.extend(['HelpWidget', 'Viewer3D', 'PkgManagerWidget', 'ProjectWidget', 'Logger', 'FileBrowser', 'World', 'HistoryWidget'])
    # applets.extend(['Store'])

    def __call__(self, mainwin):
        for plugin in iter_plugins('oalab.applet'):
            if plugin.name in self.applets:
                mainwin.add_plugin(plugin())
