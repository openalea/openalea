
from openalea.oalab.plugins.applets import PluginApplet

class HelpWidget(PluginApplet):

    name = 'HelpWidget'
    alias = 'Help'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.help import HelpWidget

        self._applet = self.new(self.name, HelpWidget)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='outputs')
