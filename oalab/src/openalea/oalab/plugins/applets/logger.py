
from openalea.oalab.applets.plugin import PluginApplet

class Logger(PluginApplet):

    name = 'Logger'
    alias = 'Logger'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.logger import Logger as LoggerWidget

        self._applet = LoggerWidget(session=mainwindow.session, controller=mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='shell')