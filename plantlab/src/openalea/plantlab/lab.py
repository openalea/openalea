
class PlantLab(object):
    name = 'plant'
    applets = [
        'ProjectManager',
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
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
