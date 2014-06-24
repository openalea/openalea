
from openalea.oalab.plugins.applets import PluginApplet

class ProjectWidget(PluginApplet):

    name = 'ProjectWidget'
    alias = 'Project'

    def __call__(self, mainwindow):
        from openalea.oalab.project.treeview import ProjectLayoutWidget

        self._applet = self.new(self.name, ProjectLayoutWidget, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='inputs')
