
from openalea.oalab.applets.plugin import PluginApplet

class PkgManagerWidget(PluginApplet):

    name = 'PkgManagerWidget'
    alias = 'Packages'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import (PackageViewWidget,
                                                    PackageCategorieViewWidget,
                                                    PackageSearchWidget)

        factories = []
        factories.append(('Packages', PackageViewWidget))
        factories.append(('PackageCategories', PackageCategorieViewWidget))
        factories.append(('PackageSearch', PackageSearchWidget))

        applets = []
        for name, klass in factories:
            applet = klass(session=mainwindow.session, controller=mainwindow)
            self._fill_menu(mainwindow, applet)
            mainwindow.add_applet(applet, name, area='inputs')
            applets.append(applet)
        self._applet = applets

