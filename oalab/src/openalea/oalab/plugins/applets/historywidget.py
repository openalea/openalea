from openalea.oalab.plugins.applets import PluginApplet


class HistoryWidget(PluginApplet):
    name = 'HistoryWidget'
    alias = 'History'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.history import HistoryWidget as History
        from openalea.oalab.service.history import register_history_diplayer

        self._applet = self.new(self.name, History)
        register_history_diplayer(self._applet)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='shell')
