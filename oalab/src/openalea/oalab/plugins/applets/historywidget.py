from openalea.oalab.plugins.applets import PluginApplet


class HistoryWidget(PluginApplet):
    name = 'HistoryWidget'
    alias = 'History'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.history import HistoryWidget as History
        return History

    def graft(self, mainwindow):
        from openalea.oalab.service.history import register_history_diplayer

        self._applet = self.new(self.name, self())
        register_history_diplayer(self._applet)
        self._fill_menu(mainwindow, self._applet)
        mainwindow.add_applet(self._applet, self.alias, area='shell')
