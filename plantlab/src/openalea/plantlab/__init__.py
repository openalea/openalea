
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

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None
        if applet is None or mainwindow is None:
            return

        from openalea.oalab.service.plot import register_plotter

        self._fill_menu(mainwindow, applet)
        register_plotter(applet)
        mainwindow.add_applet(applet, self.alias, area='outputs')
