
from openalea.oalab.applets.plugin import PluginApplet

class Viewer3D(PluginApplet):

    name = 'Viewer3D'
    alias = 'Viewer'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.scene.view3d import Viewer

        self._applet = Viewer(mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='outputs')
