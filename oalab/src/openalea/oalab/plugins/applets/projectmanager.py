
from openalea.oalab.plugins.applets import PluginApplet

class ProjectManager(PluginApplet):

    name = 'ProjectManager'
    alias = 'ProjectManager'

    def __call__(self, mainwindow):
        from openalea.oalab.project.manager import ProjectManagerWidget

        self._applet = self.new(self.name, ProjectManagerWidget, parent=mainwindow)
        self._fill_menu(mainwindow, self._applet)
        mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)

