
from openalea.oalab.plugins.applets import PluginApplet

class PkgManagerWidget(PluginApplet):

    name = 'PkgManagerWidget'
    alias = 'VisualeaPkg'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import PackageManagerTreeView
        return PackageManagerTreeView

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='inputs')
