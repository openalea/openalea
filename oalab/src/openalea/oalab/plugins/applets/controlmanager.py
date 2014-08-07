
from openalea.oalab.plugins.applets import PluginApplet

class ControlManager(PluginApplet):

    name = 'ControlManager'
    alias = 'Controls'

    def __call__(self, mainwindow):
        from openalea.oalab.gui.control.manager import ControlManagerWidget

        self._applet = self.new(self.name, ControlManagerWidget)
        mainwindow.add_applet(self._applet, self.alias, area='inputs')
#         self._fill_menu(mainwindow, self._applet)
#         mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)
