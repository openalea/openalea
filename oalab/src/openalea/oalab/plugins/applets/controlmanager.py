
from openalea.oalab.plugins.applets import PluginApplet
from openalea.deploy.shared_data import shared_data
import openalea.oalab



class ControlManager(PluginApplet):

    name = 'ControlManager'
    alias = 'Controls'
    icon = 'controlmanager.png'

    def __call__(self):
        from openalea.oalab.gui.control.manager import ControlManagerWidget
        return ControlManagerWidget

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='inputs')
