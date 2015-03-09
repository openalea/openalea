from openalea.oalab.plugins.applets import PluginApplet


class HistoryWidget(PluginApplet):
    name = 'HistoryWidget'
    alias = 'History'
    icon = 'Crystal_Clear_app_clock.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.history import HistoryWidget as History
        return History

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None
        if applet is None or mainwindow is None:
            return

        from openalea.oalab.service.history import register_history_displayer
        register_history_displayer(applet)
        self._fill_menu(mainwindow, applet)
        mainwindow.add_applet(applet, self.alias, area='shell')
