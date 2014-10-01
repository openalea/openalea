
from openalea.oalab.plugins.applets import PluginApplet

class Logger(PluginApplet):

    name = 'Logger'
    alias = 'Logger'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.logger import Logger as LoggerWidget
        return LoggerWidget

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self(), session=mainwindow.session, controller=mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='shell')
