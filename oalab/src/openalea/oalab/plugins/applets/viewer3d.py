from openalea.oalab.plugins.applets import PluginApplet

class Viewer3D(PluginApplet):
    name = 'Viewer3D'
    alias = 'Viewer'
    dependencies = ["PyQGLViewer", "openalea.plantgl.all"]

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.scene.view3d import Viewer
        from openalea.oalab.service.plot import register_plotter

        self._applet = self.new(self.name, Viewer, mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)
        register_plotter(self._applet)
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
