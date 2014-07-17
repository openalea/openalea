
class PlantLab(object):
    name = 'plant'
    applets = [
#         'ProjectManager',
#         'ProjectWidget',
        'ProjectManager2',
        'ControlManager',
        'PkgManagerWidget',
        'EditorManager',
        'Viewer3D',
        'HelpWidget',
        'Logger',
        'HistoryWidget',
        'World',
        'Plot2d',
        ]


    def __call__(self, mainwin):
        from openalea.vpltk.plugin import iter_plugins
        session = mainwin.session

        # 1. Load applets
        plugins = {}
        for plugin in iter_plugins('oalab.applet', debug=session.debug_plugins):
            if plugin.name in self.applets:
                plugins[plugin.name] = plugin()

        # 2. Place applet following given order,
        # this is important to order tabs correctly
        for name in self.applets:
            if name in plugins:
                mainwin.add_plugin(plugins[name])

        # 3. Once all applets loaded, init them (link between applets, loading default values, ...)
        mainwin.initialize()
