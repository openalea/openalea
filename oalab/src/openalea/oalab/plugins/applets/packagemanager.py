
from openalea.oalab.plugins.applets import PluginApplet

class PkgManagerWidget(PluginApplet):

    name = 'PkgManagerWidget'
    alias = 'VisualeaPkg'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import PackageManagerTreeView
        return PackageManagerTreeView

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self(), session=mainwindow.session, controller=mainwindow)
        mainwindow.add_applet(self._applet, self.alias, area='inputs')
