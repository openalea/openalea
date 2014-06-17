
class PlantLab(object):
    name = 'plant'
    applets = [
        'ControlManager',
        'EditorManager',
        'HelpWidget',
        'HistoryWidget',
        'Logger',
        'ProjectManager',
        'ProjectWidget',
        'Viewer3D',
        ]


    def __call__(self, mainwin):
        from openalea.vpltk.plugin import iter_plugins
        session = mainwin.session
        for plugin in iter_plugins('oalab.applet', debug=session.debug_plugins):
            if plugin.name in self.applets:
                mainwin.add_plugin(plugin())

