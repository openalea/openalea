
from openalea.oalab.plugins.applets import PluginApplet

class Store(PluginApplet):

    name = 'Store'
    alias = 'Store'

    def __call__(self):
        from openalea.oalab.gui.store import Store as StoreWidget
        return StoreWidget

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self(), mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='inputs')
