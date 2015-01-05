
class MiniLab(object):

    name = 'mini'
    alias = 'IPython'
    icon = 'oxygen_utilities-terminal.png'
    applets = ['EditorManager']

    # NEW LAYOUT API
    menu_names = ('File', 'Edit', 'Help')

    layout = dict(
        children={},
        parents={0: None},
        properties={
            0: {
                'widget': {
                    'properties': {'position': 0},
                    'applets': [{'name': 'ShellWidget'}]
                }
            }}
    )

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
