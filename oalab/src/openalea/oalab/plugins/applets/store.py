
from openalea.oalab.plugins.applets import PluginApplet


class Store(PluginApplet):

    name = 'Store'
    alias = 'Store'

    def __call__(self):
        from openalea.oalab.gui.store import Store
        return Store

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        self._fill_menu(mainwindow, applet)
        mainwindow.add_applet(applet, self.alias, area='inputs')
