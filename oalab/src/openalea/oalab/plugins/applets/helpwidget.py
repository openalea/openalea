
from openalea.oalab.plugins.applets import PluginApplet

class HelpWidget(PluginApplet):

    name = 'HelpWidget'
    alias = 'Help'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.help import HelpWidget
        return HelpWidget

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        self._fill_menu(mainwindow, applet)
        mainwindow.add_applet(applet, self.alias, area='outputs')
