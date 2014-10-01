
class MiniLab(object):

    name = 'mini'
    applets = ['EditorManager']

    def __call__(self, mainwin):
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
