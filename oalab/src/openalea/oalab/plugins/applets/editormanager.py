
from openalea.oalab.plugins.applets import PluginApplet

class EditorManager(PluginApplet):

    name = 'EditorManager'
    alias = 'EditorManager'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.container import ParadigmContainer
        return ParadigmContainer

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self(), mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)
        mainwindow.add_applet(self._applet, self.alias, area='central')
        return self._applet
