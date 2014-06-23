
class PlantLab(object):
    name = 'plant'
    applets = [
        'ProjectManager',
        'ProjectWidget',
        'ControlManager',
        'PkgManagerWidget',
        'EditorManager',
        'Viewer3D',
        'HelpWidget',
        'Logger',
        'HistoryWidget',
        ]


    def __call__(self, mainwin):
        from openalea.vpltk.plugin import iter_plugins
        session = mainwin.session

        plugins = {}
        for plugin in iter_plugins('oalab.applet', debug=session.debug_plugins):
            if plugin.name in self.applets:
                plugins[plugin.name] = plugin()

        # Keep order, this is important to order tabs correctly
        for name in self.applets:
            if name in plugins:
                mainwin.add_plugin(plugins[name])

