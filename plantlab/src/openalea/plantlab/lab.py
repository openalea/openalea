
from openalea.oalab.plugins.labs.default import DefaultLab


class PlantLab(DefaultLab):
    name = 'plant'
    applets = DefaultLab.applets

    def __call__(self, mainwin):
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
