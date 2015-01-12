
from openalea.oalab.plugins.labs.default import DefaultLab


class PlantLab(DefaultLab):
    name = 'plant'
    alias = 'Plant'
    applets = DefaultLab.applets
    icon = 'icon_plantlab.png'

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
