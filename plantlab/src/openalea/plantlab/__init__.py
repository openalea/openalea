
from openalea.oalab.plugins.applets import PluginApplet

class LPyModelGUI(object):
    name = 'LSystem'
    mimetype_data = "text/vnd-lpy"
    mimetype_model = "text/vnd-lpy"

    def __call__(self):
        from openalea.plantlab.paradigm import LPyModelController
        return LPyModelController


class Viewer3D(PluginApplet):
    name = 'Viewer3D'
    alias = 'Viewer'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.plantlab.view3d import Viewer
        return Viewer

    def graft(self, mainwindow):
        from openalea.oalab.service.plot import register_plotter

        self._applet = self.new(self.name, self(), mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)
        register_plotter(self._applet)
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
