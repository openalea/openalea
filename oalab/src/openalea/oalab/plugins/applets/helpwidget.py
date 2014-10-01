
from openalea.oalab.plugins.applets import PluginApplet

class HelpWidget(PluginApplet):

    name = 'HelpWidget'
    alias = 'Help'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.help import HelpWidget
        return HelpWidget

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self())
        self._fill_menu(mainwindow, self._applet)
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
