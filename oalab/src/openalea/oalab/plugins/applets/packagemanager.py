
from openalea.oalab.applets.plugin import PluginApplet

class PkgManagerWidget(PluginApplet):

    name = 'PkgManagerWidget'
    alias = 'Packages'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import PackageManagerTreeView
        self._applet = PackageManagerTreeView(session=mainwindow.session, controller=mainwindow)
        mainwindow.add_applet(self._applet, self.alias, area='inputs')


